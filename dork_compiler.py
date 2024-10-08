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
    | |          | \ | | |/ /    
  {WHITE}__| | ___  _ __|  \| | ' / ___ 
 / _ |/ _ \| '__| .  |  < / __| 
| (_| | (_) | |  | |\  | . \\__ \\ 
 \__,_|\___/|_|  |_| \_|_|\_\___/ 
{RESET}
""")

# Function to check the file size
def check_file_size(file_path):
    file_size = os.path.getsize(file_path)
    if file_size > 10 * 1024 * 1024:  # 10MB limit
        print(f"Warning: The file {file_path} is larger than 10MB. This may slow down processing.")

# Function to append .com to companies without valid TLD
def add_dot_com_if_needed(company):
    if not re.search(r'\.[a-zA-Z]{2,}$', company):  # If no valid TLD is found
        company += '.com'  # Add .com if it's not there
    return company

# Function to extract relevant parts of the dork
def extract_relevant_info(dork):
    if "inurl" in dork:
        return re.search(r'inurl:[^\s]+', dork).group(0)
    elif "filetype" in dork:
        return re.search(r'filetype:[^\s]+', dork).group(0)
    elif "intitle" in dork:
        return re.search(r'intitle:[^\s]+', dork).group(0)
    elif "intext" in dork:
        return re.search(r'intext:[^\s]+', dork).group(0)
    else:
        return dork.split(' ')[0]

# Function to truncate the button text if it's too long
def truncate_text(text, max_length=15):
    return text if len(text) <= max_length else text[:max_length - 3] + '...'

def main():
    print_banner()  # Print the banner

    # Default file paths
    companies_file = 'companies.txt'
    dorks_file = 'dorks.txt'
    output_file = 'result.txt'
    html_file = 'dorks.html'

    try:
        # Check file sizes
        check_file_size(companies_file)
        check_file_size(dorks_file)

        # Ensure the company and dork files exist
        if not os.path.isfile(companies_file):
            print(f"Input file not found: {companies_file}. Please provide a valid file.")
            return
        if not os.path.isfile(dorks_file):
            print(f"Input file not found: {dorks_file}. Please provide a valid file.")
            return

        # Read company names and append '.com' where needed
        with open(companies_file, 'r') as companies_file_handle:
            companies = [add_dot_com_if_needed(company.strip()) for company in companies_file_handle.readlines() if company.strip()]

        # Read dorks
        with open(dorks_file, 'r') as dorks_file_handle:
            dorks = [dork.strip() for dork in dorks_file_handle.readlines()]

        # New default dorks
        default_dorks = [
            'inurl:"/login.php" intitle:"admin"',
            'intitle:"index of" intext:"login.php"',
            'intitle:"index of" "login.php.txt"',
            'intitle:"index of" database.properties',
            'inurl:"/database.json"',
            'intitle:"Index of /databases"',
            'intitle:index.of./.database',
            'inurl:/libraries/joomla/database/',
            'intitle:"index of" "database.sql"',
            'intitle:"index of /database/migrations"',
            'intitle:database ext:sql',
            'intitle:"index of" "database.py"',
            'phpmyadmin/server_databases.php'
        ]

        # Use default dorks if no user dorks are found
        if not dorks:
            print("No user dorks found. Using default dorks.")
            dorks = default_dorks

        # Compile the dorks
        compiled_dorks = []
        for company in companies:
            for dork in dorks:
                compiled_dork = f"{dork} site:{company}"
                compiled_dorks.append((company, compiled_dork))

        # Write compiled dorks to result.txt
        with open(output_file, 'w') as outfile:
            for company, compiled_dork in compiled_dorks:
                outfile.write(compiled_dork + '\n')

        # Create an HTML file
        with open(html_file, 'w') as html_file_handle:
            html_file_handle.write('<html><head><title>Dork Compilation Results</title>')
            html_file_handle.write('<style>')
            html_file_handle.write('body { background-color: black; font-family: Arial, sans-serif; color: white; }')  # Black background
            html_file_handle.write('h2 { color: white; font-weight: bold; text-align: center; font-size: 2.5em; text-transform: uppercase; margin-top: 30px; }')
            html_file_handle.write('h3 { color: white; font-weight: bold; font-size: 1.5em; margin-bottom: 5px; text-transform: uppercase; }')
            html_file_handle.write('.btn, .btn2 { width: 200px; height: 70px; font-size: 20px; text-align: center; line-height: 70px; color: rgba(255,255,255,0.9); border-radius: 50px; background: linear-gradient(-45deg, #FFA63D, #FF3D77, #338AFF, #3CF0C5); background-size: 600%; animation: anime 16s linear infinite; margin: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }')  # Same button size
            html_file_handle.write('.btn2 { position: absolute; margin-top: -70px; z-index: -1; filter: blur(30px); opacity: 0.8; }')
            html_file_handle.write('div { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; margin-bottom: 20px; }')
            html_file_handle.write('.company-name { width: 15%; text-align: left; margin-left: 12.5%; font-weight: bold; text-transform: uppercase; }')  # New class for company names in 2/8 position
            html_file_handle.write('@keyframes anime { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }')
            html_file_handle.write('</style></head><body>\n')

            # Output for user companies
            for company in companies:
                html_file_handle.write(f'<h2>{company}</h2>\n')
                relevant_dorks = [dork for comp, dork in compiled_dorks if comp == company]
                html_file_handle.write('<div>\n')

                # Create buttons for each relevant dork (6 buttons per line)
                for i, dork in enumerate(relevant_dorks):
                    if i > 0 and i % 6 == 0:  # New line after every 6 buttons
                        html_file_handle.write('</div><div>\n')
                    encoded_dork = urllib.parse.quote_plus(dork)
                    search_url = f'https://www.google.com/search?q={encoded_dork}'
                    button_text = truncate_text(extract_relevant_info(dork), max_length=15)  # Truncate text if too long
                    html_file_handle.write(f'<a class="btn" href="{search_url}" target="_blank">{button_text}</a>\n')

                html_file_handle.write('</div>\n')

            # Line break before default dorks section
            html_file_handle.write('<br>\n\n')

            # Output for default dorks
            html_file_handle.write('<h2 class="default-dorks">Default Dorks</h2>\n\n')

            # Iterate through companies and display their corresponding dorks
            for company in companies:
                html_file_handle.write(f'<h3 class="company-name">{company}</h3>\n')  # Company name in the 2nd column (2/8 position)
                html_file_handle.write('<div>\n')  # Start div for buttons

                # Create buttons for default dorks (7 buttons per line)
                for i, dork in enumerate(default_dorks):
                    if i > 0 and i % 7 == 0:  # New line after every 7 buttons
                        html_file_handle.write('</div><div>\n')
                    encoded_dork = urllib.parse.quote_plus(dork)
                    search_url = f'https://www.google.com/search?q={encoded_dork}'
                    button_text = truncate_text(dork, max_length=15)  # Truncate text if too long
                    html_file_handle.write(f'<a class="btn" href="{search_url}" target="_blank">{button_text}</a>\n')

                html_file_handle.write('</div>\n')  # Close div for buttons

                # Add a line break before the next company
                html_file_handle.write('<br>\n')

            html_file_handle.write('</body></html>\n')  # Close body and HTML tags

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
