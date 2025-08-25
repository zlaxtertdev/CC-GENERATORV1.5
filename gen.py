# ==========> PLEASE DONT CHANGE THIS
#   SCRIPT   : CC GENERATOR 
#   VERSION  : 1.5
#   AUTHOR   : ZLAXTERT
#   TEAM     : DARKXCODE
#   TELEGRAM : https://t.me/zlaxtert/
# ==========> END

import requests
import json
import os
from datetime import datetime
import concurrent.futures
import time
import configparser
import random

class CCGenerator:
    def __init__(self, apikey):
        self.apikey = apikey
        self.base_url = "https://api.darkxcode.site/other/cc-generator/V1.5/"
        self.results_dir = "result"
        self.create_results_dir()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    
    def create_results_dir(self):
        """Creates a results folder if it doesn't exist yet."""
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
    
    def generate_filename(self):
        """Create a result file name"""
        return f"result.txt"
    
    def save_to_file(self, data, filename):
        """Save data to a file in txt format"""
        filepath = os.path.join(self.results_dir, filename)
        
        # Format: date|cc|month|year|cvv|scheme
        save_data = f"{data['date']}|{data['cc']}|{data['month']}|{data['year']}|{data['cvv']}|{data['scheme']}"
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(save_data + '\n')
    
    def generate_cc(self, count, cc_type, bin_number=None):
        """Generate credit card data"""
        params = {
            'submit': 1,
            'count': count,
            'type': cc_type,
            'apikey': self.apikey
        }
        
        if cc_type.upper() == "CUSTOM" and bin_number:
            params['BIN'] = bin_number
        
        try:
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(0.1, 0.5))
            
            response = self.session.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            # Try parsing JSON
            try:
                return response.json()
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON response - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            return None
    
    def process_single_request(self, index, total_count, cc_type, bin_number=None):
        """Process single API requests with multithreading"""
        try:
            result = self.generate_cc(1, cc_type, bin_number)
            
            if result and 'data' in result:
                data_info = result.get('data', {})
                
                if data_info.get('code') == 200:
                    data = data_info.get('info', {})
                    msg = data.get('msg', '')
                    
                    if msg == "SUCCESS GENERATE CREDIT CARD!":
                        # Format output
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        output = f"[{index}/{total_count}][{current_time}] SUCCESS => {data.get('cc', 'N/A')}|{data.get('month', 'N/A')}|{data.get('year', 'N/A')}|{data.get('cvv', 'N/A')}|{data.get('scheme', 'N/A')} | BY DARKXCODE V1.5"
                        print(output)
                    
                        # Save to file
                        filename = self.generate_filename()
                        self.save_to_file(data, filename)
                    
                        return data
                    else:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        output = f"[{index}/{total_count}][{current_time}] FAILED => {msg.upper()} | BY DARKXCODE V1.5"
                        print(output)
                        return None
                else:
                    error_msg = data_info.get('status', 'UNKNOWN_ERROR')
                    print(f"[{index}/{total_count}] ERROR: {error_msg}")
                    return None
            else:
                print(f"[{index}/{total_count}] ERROR: Invalid API response format")
                return None
                
        except Exception as e:
            print(f"[{index}/{total_count}] Unexpected error: {e}")
            return None

def load_apikey():
    """Load API key from settings.ini file"""
    config = configparser.ConfigParser()
    
    if not os.path.exists('settings.ini'):
        # Create a settings.ini file if it doesn't exist.
        config['SETTINGS'] = {'APIKEY': 'PASTE YOUR APIKEY HERE'}
        with open('settings.ini', 'w') as configfile:
            config.write(configfile)
        print("[!] File settings.ini created. Please add your API key first!")
        exit()
    
    try:
        config.read('settings.ini')
        apikey = config['SETTINGS']['APIKEY']
        
        if apikey == 'PASTE YOUR APIKEY HERE' or not apikey.strip():
            print("[!] Please update your API key in settings.ini file!")
            exit()
            
        return apikey
    except (KeyError, configparser.Error):
        print("[!] Error reading settings.ini file!")
        exit()

def get_card_type():
    """Displays the menu and gets the card type."""
    print("\n" + "="*50)
    print("        [!] TYPE [!]")
    print("1. VISA         2. MASTERCARD")
    print("3. JCB          4. AMEX")
    print("5. DISCOVER     6. RANDOM")
    print("7. CUSTOM       99. EXIT")
    print("="*50)
    
    while True:
        try:
            choice = input("[+] Choose number >> ").strip()
            
            if not choice:
                print("[!] Please enter a choice!")
                continue
                
            choice = int(choice)
            
            type_mapping = {
                1: "VISA",
                2: "MASTERCARD",
                3: "JCB",
                4: "AMEX",
                5: "DISCOVER",
                6: "RANDOM",
                7: "CUSTOM",
                99: "EXIT"
            }
            
            if choice in type_mapping:
                if choice == 99:
                    print("[+] Goodbye!")
                    exit()
                return type_mapping[choice]
            else:
                print("[!] Invalid choice! Please choose 1-7 or 99 to exit.")
        except ValueError:
            print("[!] Please enter a valid number!")

def get_bin_number():
    """Get BIN number for CUSTOM type"""
    while True:
        bin_input = input("[+] Please input BIN >> ").strip()
        
        if not bin_input:
            print("[!] BIN cannot be empty!")
            continue
            
        #Remove spaces and non-digit characters
        bin_input = ''.join(filter(str.isdigit, bin_input))
            
        if len(bin_input) < 6:
            print("[!] BIN must be at least 6 digits!")
            continue
            
        return bin_input

def get_threads():
    """Gets the number of threads"""
    while True:
        try:
            threads = input("[+] Please input threads (min 1 & max 10) >> ").strip()
            
            if not threads:
                print("[!] Threads cannot be empty!")
                continue
                
            threads = int(threads)
            
            if 1 <= threads <= 10:
                return threads
            else:
                print("[!] Threads must be between 1 and 10!")
        except ValueError:
            print("[!] Please enter a valid number!")

def get_count():
    """Get the count number"""
    while True:
        try:
            count = input("[+] Please input count (min 1 & max 1000) >> ").strip()
            
            if not count:
                print("[!] Count cannot be empty!")
                continue
                
            count = int(count)
            
            if 1 <= count <= 1000:
                return count
            else:
                print("[!] Count must be between 1 and 1000!")
        except ValueError:
            print("[!] Please enter a valid number!")

def main():
    # Load API key from settings.ini
    apikey = load_apikey()
    
    print(f"\n{'='*60}")
    print("                 DARKXCODE CC GENERATOR V1.5")
    print(f"{'='*60}")
    
    # Get user inputs
    card_type = get_card_type()
    
    bin_number = None
    if card_type == "CUSTOM":
        bin_number = get_bin_number()
    
    count = get_count()
    threads = get_threads()
    
    # Generator initialization
    generator = CCGenerator(apikey)
    
    print(f"\n{'='*60}")
    print("GENERATION SETTINGS:")
    print(f"{'='*60}")
    print(f"Type: {card_type}")
    if card_type == "CUSTOM":
        print(f"BIN: {bin_number}")
    print(f"Count: {count}")
    print(f"Threads: {threads}")
    print(f"{'='*60}\n")
    
    # Confirm before starting
    confirm = input("[+] Press Enter to start or 'n' to cancel: ").strip().lower()
    if confirm == 'n':
        print("[+] Operation cancelled!")
        return
    
    start_time = time.time()
    successful_count = 0
    
    # Using ThreadPoolExecutor for multithreading
    print(f"\nStarting generation with {threads} threads...\n")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # Make a list of futures
        futures = []
        for i in range(1, count + 1):
            future = executor.submit(
                generator.process_single_request, 
                i, count, card_type, bin_number
            )
            futures.append(future)
            # Add a small delay between requests
            time.sleep(0.1)
        
        # Collecting results
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    successful_count += 1
            except Exception as e:
                print(f"Error processing result: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"\n{'='*60}")
    print("GENERATION COMPLETED!")
    print(f"{'='*60}")
    print(f"Total requests: {count}")
    print(f"Successful: {successful_count}")
    print(f"Failed: {count - successful_count}")
    print(f"Success rate: {(successful_count/count)*100:.2f}%")
    print(f"Time taken: {total_time:.2f} seconds")
    print(f"Results saved in: {generator.results_dir}/")
    print(f"{'='*60}")

if __name__ == "__main__":

    main()
