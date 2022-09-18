import requests
import sys
import argparse
import os

# parsing args
parser = argparse.ArgumentParser(add_help=True, description="Tool to enum DNS records")
parser.add_argument("--server", help="specify target server to enumerate", required=True)
parser.add_argument("--wordlist", help="specify wordlist to use", required=True)
parser.add_argument("--output", help="specify ouput filename for found subdomains", required=True)
args = parser.parse_args()
# list
domain = args.server
wordlist = args.wordlist
file_output = args.output
print(f"Will enum {domain} domain by using {wordlist}, writing into {file_output}")

# Read wordlist lines
wordlist = open(wordlist)
subdomains = wordlist.read().splitlines()

# Write found subdomains into a "subdomains_found.txt"
sub_found = open(file_output, "w+")

# Length of wordlist/subdomains to test
sub_length = len(subdomains)
count = 0

for subdomain in subdomains:
    url = f"https://{subdomain}.{domain}"
    try:
        requests.get(url,timeout=2)
        print("[+] ", count, "/", sub_length, "Subdomain found on : ", url)
        sub_found.write("[+] Subdomain found : " + url + "\n")
        count += 1
        continue
    except requests.Timeout:
        print("[-] ", count, "/", sub_length, f"Error: Timeout error encountered when trying {url}")
        pass
    except ConnectionError as e:
        print("[-] ", count, "/", sub_length, f"Error: Connection error encountered when trying {url}")
        print(e)
        pass
    # Must be here in case of no errors up here
    except Exception as e:
        #print(e)
        continue