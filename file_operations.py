import os
from termcolor import colored
import time
import re
import json


def file_exists(filename):
    if os.path.exists(filename):
        if os.path.isfile(filename):
            return True
        else:
            return False
    else:
        return False


def read_dorks(filename):
    dorks = []
    try:
        with open(filename, "r",encoding='utf-8') as dork_file:
            for line in dork_file:
                dorks.append(line.strip())  # Strip whitespace and add to the list
        return dorks
    except FileNotFoundError as file_not_found:
        print(colored(f"[-] Error: {file_not_found}","light_red"))
        exit()
    except Exception as e:
        print(colored(f"[-] Error: {e}","light_red"))
        exit()



def write_output(output_filename, data):
    # Ensure data is a string; convert to JSON if it's a dictionary
    if isinstance(data, dict):
        data = json.dumps(data, indent=4)
    if not output_filename or output_filename == None:
        current_time = time.time()
        # Convert current_time to a string and extract the integer part before the decimal
        unique = re.match(r"^(\d+)", str(current_time))
        if unique:
            output_filename = f"{unique.group(1)}_google_dorks.json"
    try:
        with open(output_filename, "w") as output_file:
            output_file.write(data)
            print("")
            print(colored(f"[+] Output successfully saved to {output_filename}.","light_green"))
    except IOError as err:
        print(colored(f"[-] Error: {err}","light_red"))
        exit()
