# dorNKs (dork_compiler)

Google Dork Compilation Tool
A simple Python tool to generate Google dorks by combining company names with custom dorks.

How to Use

1. Prepare Files
companies.txt: A text file with company names (one per line).
dorks.txt: A text file with custom Google dorks. Use abcd.com as a placeholder for the company name.

Example Files:

companies.txt
example.com
test.com
mycompany.com


dorks.txt
site:abcd.com inurl:admin
site:abcd.com filetype:pdf


2. Run the Script
In the terminal, navigate to the folder where the Python script and the files are located, and

run:  python3 dork_compiler.py --companies companies.txt --dorks dorks.txt --output result.txt --html dorks.html


4. Output
result.txt: Contains the combined dorks.
dorks.html: Contains clickable Google search links.

6. Example Command

python3 dork_compiler.py --companies companies.txt --dorks dorks.txt
This will generate result.txt and dorks.html by default.

Troubleshooting
If you get a "Permission denied" error, run the script with sudo:

sudo python3 dork_compiler.py --companies companies.txt --dorks dorks.txt
