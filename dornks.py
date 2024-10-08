import os
import subprocess

# Get the path to the dork_compiler.py file
script_path = os.path.join(os.path.dirname(__file__), 'dork_compiler.py')

# Run the dork_compiler.py script
subprocess.run(['python', script_path])
