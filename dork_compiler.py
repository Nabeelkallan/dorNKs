import os
import re
import urllib.parse

# Function to print the banner with specified colors
def print_banner():
    RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    
    print(f"""{RED}
     _            _   _ _  __    
    | |          | \\ | | |/ /    
  {WHITE}__| | ___  _ __|  \\| | ' / ___ 
 / _ |/ _ \\| '__| .  |  < / __| 
| (_| | (_) | |  | |\\  | . \\__ \\ 
 \\__,_|\\___/|_|  |_| \\_|_|\\_\\___/ 
{RESET}
""")

# Function to check the file size
def check_file_size(file_path):
    file_size = os.path.getsize(file_path)
    if file_size > 10 * 1024 * 1024:  # 10MB limit
        print(f"Warning: The file {file_path} is larger than 10MB. This may slow down processing.")

# Function to extract the domain from a URL
def extract_domain(url):
    return re.sub(r'^https?://(www\.)?|/$', '', url).strip()

# Function to append .com to companies without a valid TLD
def add_dot_com_if_needed(company):
    if not re.search(r'\.[a-zA-Z]{2,}$', company):  # If no valid TLD is found
        company += '.com'  # Add .com if it's not there
    return company

# Function to extract relevant parts of the dork
def extract_relevant_info(dork):
    parts = []
    if "inurl" in dork:
        parts.append(re.search(r'inurl:[^\s]+', dork).group(0))
    if "filetype" in dork:
        parts.append(re.search(r'filetype:[^\s]+', dork).group(0))
    if "intitle" in dork:
        parts.append(re.search(r'intitle:[^\s]+', dork).group(0))
    if "intext" in dork:
        parts.append(re.search(r'intext:[^\s]+', dork).group(0))
    return parts

# Function to truncate the button text if it's too long
def truncate_text(text, max_length=15):
    return text if len(text) <= max_length else text[:max_length - 3] + '...'

# Function to compile dorks based on companies
def compile_dorks(companies, dorks):
    compiled_dorks = []
    for company in companies:
        for dork in dorks:
            dork = re.sub(r'site:[^\s]+', '', dork)  # Remove any site: filters
            compiled_dork = f"site:{company} {dork.strip()}"
            compiled_dorks.append((company, compiled_dork))
    return compiled_dorks

# Function to write results to a text file (result.txt)
def write_results_to_file(output_file, compiled_dorks):
    with open(output_file, 'w') as outfile:
        for company, compiled_dork in compiled_dorks:
            outfile.write(compiled_dork + '\n')

# Function to generate the HTML header
def generate_html_header():
    return '''<html>
<head>
    <title>Dork Compilation Results</title>
    <style>
        body { background-color: #1e1e1e; font-family: Arial, sans-serif; color: #fff; text-align: center; }
        .button-container { display: flex; flex-wrap: wrap; justify-content: center; margin: 20px 0; }
        .glow-on-hover { width: 230px; height: 70px; border: none; outline: none; color: #fff; background: #111; cursor: pointer; position: relative; z-index: 0; border-radius: 30px; margin: 5px; font-size: 18px; }
        .glow-on-hover:before { content: ''; background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000); position: absolute; top: -2px; left:-2px; background-size: 400%; z-index: -1; filter: blur(5px); width: calc(100% + 4px); height: calc(100% + 4px); animation: glowing 20s linear infinite; opacity: 0; transition: opacity .3s ease-in-out; border-radius: 30px; }
        .glow-on-hover:active { color: #000; }
        .glow-on-hover:hover:before { opacity: 1; }
        .glow-on-hover:after { z-index: -1; content: ''; position: absolute; width: 100%; height: 100%; background: #111; left: 0; top: 0; border-radius: 30px; }
        @keyframes glowing { 0% { background-position: 0 0; } 50% { background-position: 400% 0; } 100% { background-position: 0 0; } }
        .medium-button { width: 220px; height: 60px; font-size: 17px; }  /* Slightly larger button style for default dorks */
    </style>
</head>
<body>
'''

# Function to generate HTML footer
def generate_html_footer():
    return '</body></html>'

# Function to generate HTML for user dorks
def generate_user_dorks_html(companies, user_dorks):
    user_dorks_html = ""
    
    for company in companies:
        relevant_dorks = [dork for c, dork in user_dorks if c == company]
        
        # Use subdomain for heading
        subdomain = extract_domain(company)
        user_dorks_html += f'<h2>{subdomain.upper()}</h2>\n'  # Display company name in uppercase

        user_dorks_html += '<div class="button-container">\n'  # Start button container
        button_count = 0
        for user_dork in relevant_dorks:
            clean_user_dork = re.sub(r'site:[^\s]+', '', user_dork).strip()  # Remove site: filter
            encoded_user_dork = urllib.parse.quote_plus(clean_user_dork)  # Encode the cleaned dork
            search_url = f'https://www.google.com/search?q=site:{subdomain} {encoded_user_dork}'
            button_text = truncate_text(clean_user_dork, max_length=15)  # Truncate text if too long
            user_dorks_html += f'<button class="glow-on-hover" onclick="window.open(\'{search_url}\', \'_blank\');">{button_text.lower()}</button>\n'
            button_count += 1
            
            if button_count >= 7:  # Limit to 7 buttons per company
                user_dorks_html += '</div><div class="button-container">\n'  # Create a new button container
                button_count = 0  # Reset button count for new container

        user_dorks_html += '</div>\n'  # End button container
        user_dorks_html += '<br><br>'  # Add line break after button and before new heading

    return user_dorks_html

# Function to generate HTML for default dorks
def generate_default_dorks_html(companies, default_dorks):
    default_dorks_html = '<br><br><h2 style="font-size: 36px;">DEFAULT DORKS</h2>\n<br>'
    
    for company in companies:
        default_dorks_html += f'<h3>{extract_domain(company).upper()}</h3>\n'  # Display subdomain in uppercase
        default_dorks_html += '<div class="button-container">\n'

        button_count = 0
        for default_dork in default_dorks:
            encoded_default_dork = urllib.parse.quote_plus(default_dork)
            search_url = f'https://www.google.com/search?q=site:{extract_domain(company)} {encoded_default_dork}'
            button_text = truncate_text(default_dork, max_length=15)  # Truncate text if too long
            default_dorks_html += f'<button class="glow-on-hover medium-button" onclick="window.open(\'{search_url}\', \'_blank\');">{button_text.lower()}</button>\n'  # Use medium button class
            button_count += 1

            if button_count >= 8:  # Limit to 8 buttons per company
                default_dorks_html += '</div><div class="button-container">\n'  # Create a new button container
                button_count = 0  # Reset button count for new container

        default_dorks_html += '</div>\n<br>'  # Add line breaks after default dork buttons

    return default_dorks_html

# Function to generate the complete HTML file (dorks.html)
def generate_html_file(html_file, companies, user_dorks, default_dorks):
    with open(html_file, 'w') as html_file_handle:
        html_file_handle.write(generate_html_header())
        html_file_handle.write(generate_user_dorks_html(companies, user_dorks))
        html_file_handle.write(generate_default_dorks_html(companies, default_dorks))
        html_file_handle.write(generate_html_footer())

# Main function to execute the program
def main():
    print_banner()
    
    companies_file = 'companies.txt'
    dorks_file = 'dorks.txt'
    output_file = 'results.txt'
    html_file = 'dorks.html'
    
    check_file_size(companies_file)
    check_file_size(dorks_file)

    with open(companies_file, 'r') as file:
        companies = [add_dot_com_if_needed(line.strip()) for line in file.readlines()]

    with open(dorks_file, 'r') as file:
        user_dorks = [line.strip() for line in file.readlines()]

    compiled_dorks = compile_dorks(companies, user_dorks)
    write_results_to_file(output_file, compiled_dorks)
    generate_html_file(html_file, companies, compiled_dorks, default_dorks)

if __name__ == "__main__":
    default_dorks = [
        'filetype:env "DB_PASSWORD"',
    'filetype:log inurl:"/logs/"',
    'intitle:"index of" inurl:backup filetype:sql',
    'filetype:conf "apache" inurl:config',
    'filetype:pem intext:"PRIVATE KEY"',
    'filetype:php inurl:wp-config',
    'inurl:"server-status" "Apache Server Status"',
    'intext:"credit card number" filetype:xls OR filetype:csv',
    'intext:"api_key" OR intext:"apikey" filetype:json',
    'intext:"wallet private key" filetype:txt',
    'filetype:yaml inurl:"docker-compose"',
    'filetype:log intext:"transaction" intext:"approved"',
    'filetype:log intext:"payment failed"',
    'filetype:log intext:"bitcoin" intext:"node"',
    'filetype:sql intext:"CREATE TABLE"',
    'filetype:conf intext:"secret_key"',
    'filetype:json intext:"client_secret"',
    'filetype:json intext:"api_key"',
    'filetype:txt intext:"API_SECRET"',
    'filetype:xml intext:"payment_config"',
    'filetype:log intext:"payment_debug"',
    'filetype:json intext:"user_auth"',
    'filetype:json intext:"user_profile" intext:"email"',
    'filetype:csv intext:"user_password"',
    'filetype:json intext:"auth_token" intext:"user"',
    'filetype:xml intext:"user_credentials"',
    'filetype:log intext:"access_token" intext:"user"',
    'filetype:sql intext:"user_table"',
    'filetype:json intext:"encrypted_password"',
    'filetype:txt intext:"api_key" intext:"user"',
    'filetype:conf intext:"db_password" intext:"user"',
    'filetype:xml intext:"user_key"',
    'filetype:log intext:"user_activity"',
    'filetype:json intext:"user_data" intext:"api_secret"',
    'filetype:txt intext:"user_authentication"',
    'filetype:xml intext:"api_secret"',
    ]
    main()
