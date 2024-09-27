import argparse

def main():
    parser = argparse.ArgumentParser(description='Google Dork Compilation Tool')
    parser.add_argument('--companies', type=str, help='Input file with company names')
    parser.add_argument('--dorks', type=str, help='Input file with custom dorks')
    parser.add_argument('--output', type=str, default='result.txt', help='Output file to save compiled dorks')
    parser.add_argument('--html', type=str, default='dorks.html', help='Output HTML file with clickable links')
    args = parser.parse_args()

    if args.companies and args.dorks:
        try:
            # Read company names
            with open(args.companies, 'r') as companies_file:
                companies = [company.strip() for company in companies_file.readlines()]

            # Read dorks
            with open(args.dorks, 'r') as dorks_file:
                dorks = [dork.strip() for dork in dorks_file.readlines()]

            compiled_dorks = []

            # Combine each company with each dork
            for company in companies:
                for dork in dorks:
                    compiled_dork = dork.replace("abcd.com", company)
                    compiled_dorks.append(compiled_dork)

            # Write the output to the specified output file (default is result.txt)
            with open(args.output, 'w') as outfile:
                for compiled_dork in compiled_dorks:
                    outfile.write(compiled_dork + '\n')

            # Create an HTML file with clickable links
            with open(args.html, 'w') as html_file:
                html_file.write('<html><body>\n')
                for dork in compiled_dorks:
                    # Ensure dork starts with 'http://' or 'https://'
                    if not dork.startswith('http://') and not dork.startswith('https://'):
                        dork = 'https://www.google.com/search?q=' + dork  # Convert dork to a Google search link
                    link = f'<a href="{dork}" target="_blank">{dork}</a><br>\n'
                    html_file.write(link)
                html_file.write('</body></html>\n')

            print(f"Compiled {len(compiled_dorks)} dorks saved to {args.output}")
            print(f"Clickable links saved to {args.html}")

        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
    else:
        print("Please provide input files for companies and dorks")

if __name__ == "__main__":
    main()
