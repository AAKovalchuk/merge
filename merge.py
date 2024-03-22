#!/usr/bin/python 

import os
import subprocess
import re

from rich.progress import Progress
from rich.console import Console
from rich.table import Table

directory_path = '.'
file_dict = {}
output_path = input("Specify the path to save the results: ")
season = input("Season? : ")
pattern = r'\b(\d{2})\b'   #If the series has 3 digits, then change the constant

#Search for files with the same number
for filename in os.listdir(directory_path):
    if os.path.isfile(os.path.join(directory_path, filename)):
        match = re.search(pattern, filename)
        if match:
            number = match.group(1)
            file_dict.setdefault(number, []).append(filename)

#Checking and creating an output folder
if not os.path.exists(output_path):
    os.makedirs(output_path)

#Beautiful result output
table = Table(title="Result")
table.add_column("No.", style="cyan", no_wrap=True)
table.add_column("File Name", style="magenta")
table.add_column("Status", justify="center", style="green")

#Main program
with Progress() as progress:                                                    
    task_id = progress.add_task("[green]Processing...", total=len(file_dict))   

    for number, filenames in file_dict.items():
        if len(filenames) > 1:
            files_to_merge = [os.path.join(directory_path, filename) for filename in filenames]
            output_file = os.path.join(output_path, f'output_S0{season}E{number}.mkv')
            cmd = ['mkvmerge', '-q', '-o', output_file] + files_to_merge
            subprocess.run(cmd)

            table.add_row(f'{number}', f'{output_file}', "✅")
            progress.advance(task_id)

console = Console()
console.print(table)

subprocess.run(["chown", "-R", "plex:plex", output_path])
print("Directory owner has been changed to PLEX")
