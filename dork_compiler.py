import os
import re
import urllib.parse

def print_banner():
    os.system('toilet -f big --gay dorNKs')

def check_file_size(file_path):
    file_size = os.path.getsize(file_path)
    if file_size > 10 * 1024 * 1024:  # 10MB
        print(f"Warning: The file {file_path} is larger than 10MB. This may slow down processing.")

def is_valid_domain(domain):
    pattern = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, domain)

def extract_relevant_info(dork):
    # Extracts the relevant parts of the dork
    if "inurl" in dork:
        return re.search(r'inurl:[^\s]+', dork).group(0)  # Gets the inurl part
    elif "filetype" in dork:
        return re.search(r'filetype:[^\s]+', dork).group(0)  # Gets the filetype part
    elif "intitle" in dork:
        return re.search(r'intitle:[^\s]+', dork).group(0)  # Gets the intitle part
    elif "intext" in dork:
        return re.search(r'intext:[^\s]+', dork).group(0)  # Gets the intext part
    else:
        return dork.split(' ')[0]  # Fallback to the first part of the dork

def main():
    print_banner()  # Print the banner when the program starts

    # Default file paths and search engine
    companies_file = 'companies.txt'
    dorks_file = 'dorks.txt'
    output_file = 'result.txt'
    html_file = 'dorks.html'
    search_engine = 'google'

    try:
        # Check file sizes
        check_file_size(companies_file)
        check_file_size(dorks_file)

        # Check if company and dork files exist
        if not os.path.isfile(companies_file):
            print(f"Input file not found: {companies_file}. Please provide a valid file.")
            return
        if not os.path.isfile(dorks_file):
            print(f"Input file not found: {dorks_file}. Please provide a valid file.")
            return

        # Read company names
        with open(companies_file, 'r') as companies_file_handle:
            companies = [company.strip() for company in companies_file_handle.readlines() if is_valid_domain(company.strip())]

        # Read dorks
        with open(dorks_file, 'r') as dorks_file_handle:
            dorks = [dork.strip() for dork in dorks_file_handle.readlines()]

        # Fallback to default dorks if none are provided
        default_dorks = ['inurl:"admin"', 'intitle:"login"', 'filetype:pdf']
        if not dorks:
            print("No dorks found. Using default dorks.")
            dorks = default_dorks

        compiled_dorks = []
        for company in companies:
            for dork in dorks:
                # Include the company name in the search query
                compiled_dork = f"{dork} site:{company}"
                compiled_dorks.append((company, compiled_dork))

        # Write the output to result.txt
        with open(output_file, 'w') as outfile:
            for company, compiled_dork in compiled_dorks:
                outfile.write(compiled_dork + '\n')

        # Create HTML file
        with open(html_file, 'w') as html_file_handle:
            html_file_handle.write('<html><head><title>Dork Compilation Results</title>')
            html_file_handle.write('<style>')
            html_file_handle.write('body { font-family: Arial, sans-serif; background-color: white; color: black; }')
            html_file_handle.write('h2 { color: black; font-weight: bold; text-align: center; font-size: 3.5em; text-transform: uppercase; margin-top: 50px; }')  # Larger heading and centered
            html_file_handle.write('a { display: inline-block; width: 30%; height: 50px; padding: 10px; background: linear-gradient(to right, #1e90ff, #00bfff); color: white; text-align: center; text-decoration: none; border-radius: 5px; margin: 10px; line-height: 50px; }')  # Gradient blue button
            html_file_handle.write('div { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; }')
            html_file_handle.write('</style></head><body>\n')

            for company in companies:
                html_file_handle.write(f'<h2>{company}</h2>\n')  # Centered and capitalized company name heading
                relevant_dorks = [dork for comp, dork in compiled_dorks if comp == company]
                html_file_handle.write('<div>\n')

                # Create buttons for each relevant dork
                for dork in relevant_dorks:
                    encoded_dork = urllib.parse.quote_plus(dork)
                    search_url = f'https://www.google.com/search?q={encoded_dork}'
                    button_text = extract_relevant_info(dork)
                    html_file_handle.write(f'<a href="{search_url}" target="_blank">{button_text}</a>\n')

                html_file_handle.write('</div>\n')

            html_file_handle.write('</body></html>\n')

        print(f"Compiled dorks saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
