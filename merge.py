#!/usr/bin/python 

import os
import subprocess
import re

directory_path = '.'

file_dict = {}

pattern = r'\b(\d{2})\b'

for filename in os.listdir(directory_path):
    if os.path.isfile(os.path.join(directory_path, filename)):
        match = re.search(pattern, filename)
        if match:
            number = match.group(1)
            file_dict.setdefault(number, []).append(filename)

output_path = input("Specify the path to save the results: ")

season = input("Season? : ")

if not os.path.exists(output_path):
    os.makedirs(output_path)

for number, filenames in file_dict.items():
    if len(filenames) > 1:
        files_to_merge = [os.path.join(directory_path, filename) for filename in filenames]

        output_file = os.path.join(output_path, f'output_S0{season}E{number}.mkv')

        cmd = ['mkvmerge', '-o', output_file] + files_to_merge

        subprocess.run(cmd)

        print(f"File {output_file} created with number {number} from the next files:")
        for filename in filenames:
            print(filename)

subprocess.run("chown", "-R", "plex:plex", output_path)
print("Directory owner has been changed to PLEX")
