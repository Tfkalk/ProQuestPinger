import requests
from bs4 import BeautifulSoup
import sys
from urllib3.exceptions import InsecureRequestWarning
import time

# Suppress only the specific InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def check_urls(input_file, output_file):
    # Read URLs from input file
    try:
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    unavailable_urls = []
    total_urls = len(urls)
    
    print(f"Processing {total_urls} URLs...")
    
    # Process each URL
    for i, url in enumerate(urls, 1):
        try:
            # Add http:// prefix if missing
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            # Send request with a timeout and verify=False for SSL issues
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            
            # Parse the content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print(response.text)
            
            # Check if "Document Unavailable" is in the page
            if "We're sorry, your institution doesn't have access to this article through ProQuest" in response.text:
                unavailable_urls.append(url)
                print(f"[{i}/{total_urls}] Found unavailable document: {url}")
            else:
                print(f"[{i}/{total_urls}] Document available: {url}")
                
            # Be nice to servers
            time.sleep(1)
            
        except Exception as e:
            print(f"[{i}/{total_urls}] Error processing {url}: {str(e)}")
            # Add to list with a note about the error
            unavailable_urls.append(f"{url} # Error: {str(e)}")
    
    # Write unavailable URLs to output file
    with open(output_file, 'w') as f:
        for url in unavailable_urls:
            f.write(url + '\n')
    
    print(f"\nCompleted! Found {len(unavailable_urls)} unavailable documents.")
    print(f"Results written to '{output_file}'")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_file.txt output_file.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    check_urls(input_file, output_file)
