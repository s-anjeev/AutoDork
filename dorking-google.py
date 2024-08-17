import sys
import argparse
from termcolor import colored
import requests
import config
import time
from file_operations import file_exists, read_dorks, write_output

results_dict = {}

def custom_parser_error(message):
    # Define custom behavior for parsing errors
    sys.stderr.write(colored(f"Error: {message}\n", "light_red"))
    sys.exit(2)

def parse_args():
    # Parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -D site:example.com -Q inurl:login")
    parser.error = custom_parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-D', '--domain', help="Domain name for Google Dorking.", required=True)
    parser.add_argument('-Q', '--query', help="Single Google dork for the domain.")
    parser.add_argument('-F', '--file', help="File containing Google dork for the domain.")
    parser.add_argument('-O', '--output', help="File name to store the dorks result (This feature is not yet implemented).")
    parser.add_argument('-T', '--threads', help='Number of threads to use for subbrute bruteforce (This feature is not yet implemented).', type=int, default=5)
    return parser.parse_args()

def fetch_api_key():
    global results_dict
    API_Keys = config.API_Key
    CSE_Ids = config.CSE_Id

    if API_Keys and CSE_Ids:
        API_key = API_Keys.pop(0)
        CSE_Id = CSE_Ids.pop(0)
        return API_key, CSE_Id
    else:
        print(colored("[-] No more API keys or CSE IDs available.", "light_red"))
        write_output(data = results_dict,output_filename=None)
        exit()

def google_search(domain, API_key, CSE_Id, num_results=100, query=None):
    if query:  # Only append query if it's not None or an empty string
        domain = f"{domain} {query}"

    api_key = API_key
    cse_id = CSE_Id
    response = ""
    links = []
    start = 1
    print()
    print(colored(f"[$] {domain}", "grey"))
    
    while start <= num_results:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': domain,
            'start': start,
            'num': 10  # Number of results per page (10 is the maximum allowed)
        }
        try:
            response = requests.get(url, params=params)
            # print(response.json())
            
            if response.status_code == 429:
                print(colored("[-] 429 Rate limit exceeded.", "light_red"))
                API_key, CSE_Id = fetch_api_key()
                if API_key:
                    print(colored("[+] Continuing with a new API key.", "light_blue"))
                    api_key = API_key
                    cse_id = CSE_Id
                    start = 1
                    continue

            if response.status_code == 403 and "userRateLimitExceeded" in response.json():
                print(colored("[-] 403 Too Many Requests. Pausing...", "light_red"))
                time.sleep(150)
                continue
        
            if response.status_code == 200:
                response.raise_for_status()
                results = response.json()
                new_links = [item['link'] for item in results.get('items', [])]
                links.extend(new_links)
                
                if not new_links:
                    break
                
                start += 10
        except requests.exceptions.RequestException as e:
            print(colored(f"[-] Error during API request: {e}.", "light_red"))
            break

    return links

def start_dorking(args, dorks=None):
    global results_dict
    try:
        API_key, CSE_Id = fetch_api_key()
        results_dict ={}
        if dorks:
            for dork in dorks:
                current_query = f"{args.query} {dork}" if args.query else dork
                links = google_search(args.domain, API_key, CSE_Id, query=current_query)
                results_dict[current_query] = links
                if links:
                    print(colored("-----------------------------------------------------", "light_blue"))
                    for link in links:
                        print(colored(f"[+] {link}", "light_green"))
                    print(colored("-----------------------------------------------------", "light_blue"))
                    print("")
                else:
                    print(colored("[-] No results found for query.", "light_red"))
                    
        else:
            links = google_search(args.domain, API_key, CSE_Id, query=args.query)
            # all_links.extend(links)
            # Save the query and its links to the dictionary
            results_dict[args.query] = links
            if links:
                print(colored("-----------------------------------------------------", "light_blue"))
                for link in links:
                    print(colored(f"[+] {link}", "light_green"))
                print(colored("-----------------------------------------------------", "light_blue"))
                print("")
            else:
                print(colored("[-] No results found for query.", "light_red"))
        write_output(data = results_dict,output_filename=None)
    except RuntimeError as err:
        print(colored(f"[-] Error: {err}","light_red"))
        write_output(data = results_dict,output_filename=None)


def main():
    global results_dict
    try:
        print("")
        print(colored("# Dorking King...", "light_cyan"))
        print("")
        print(colored("#####################################################", "light_yellow"))
        args = parse_args()
        print(colored("Let's go...", "light_blue"))
        print("")

        if args.query and args.file:
            print(colored("[-] Cannot use both query and file arguments simultaneously.", "light_red"))
            exit()

        if args.file and file_exists(args.file):
            dorks = read_dorks(args.file)
            if dorks:
                start_dorking(args, dorks)
        else:
            start_dorking(args)

    except KeyboardInterrupt:
        write_output(data = results_dict,output_filename=None)
        print(colored("\n[!] Script execution interrupted by user. Exiting...", "light_red"))
        sys.exit(0)

if __name__ == "__main__":
    main()