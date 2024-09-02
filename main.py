import requests
from colorama import Fore, init
from random import choices
import time

init(autoreset=True)

def write_to_file(username):
    filename = 'Available.txt'
    with open(filename, 'a') as file:
        file.write(f"{username}\n")

def check(username_length):
    print(Fore.CYAN + f"[!] Checking usernames with {username_length} characters...\n")
    
    retry_attempt = 0
    max_retries = 5

    while True:
        username = ''.join(choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=username_length))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        url = f'https://api.mojang.com/users/profiles/minecraft/{username}'

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"{Fore.RED}[-] {username} Taken")
                retry_attempt = 0
            elif response.status_code in {204, 404}:  # Handle both 204 and 404 as available
                print(f"{Fore.GREEN}[+] {username} Available")
                write_to_file(username)
                retry_attempt = 0
            elif response.status_code == 429:
                print(Fore.YELLOW + "[!] Rate limit exceeded. Retrying after delay...")
                retry_attempt += 1
                if retry_attempt > max_retries:
                    print(Fore.RED + "[!] Max retries exceeded. Exiting...")
                    break
                time.sleep(2 ** retry_attempt)
            else:
                print(f"{Fore.YELLOW}[!] Unexpected Status Code: {response.status_code}. Response content: {response.text}")
                retry_attempt = 0
                
        except requests.RequestException as err:
            print(f"{Fore.RED}[!] Error occurred: {err}")
            retry_attempt = 0

        time.sleep(1)

def main_menu():
    banner = """
                         _       _     ____                     _ 
                        | |     | |   / / _|                   | |
  __ _ _   _ _ __  ___  | | ___ | |  / / |_ _ __ __ _  ___   __| |
 / _` | | | | '_ \/ __| | |/ _ \| | / /|  _| '__/ _` |/ _ \ / _` |
| (_| | |_| | | | \__ \_| | (_) | |/ / | | | | | (_| | (_) | (_| |
 \__, |\____|_| |_|___(_)_|\___/|_/_/  |_| |_|  \____|\___/ \____|
  __/ |                                                           
 |___/                                                            
    """
    print(Fore.MAGENTA + banner)
    print(Fore.CYAN + "--- Minecraft Username Generator ---\n")
    print("1. Start generating usernames")
    print("2. Exit\n")

    while True:
        choice = input(Fore.CYAN + "Enter your choice (1 or 2): ").strip()

        if choice == '1':
            while True:
                try:
                    username_length = int(input(Fore.CYAN + "Enter the number of characters for the usernames (2-20): ").strip())
                    if 2 <= username_length <= 20:
                        check(username_length)
                    else:
                        print(Fore.RED + "[!] Please enter a number between 2 and 20.")
                except ValueError:
                    print(Fore.RED + "[!] Invalid input. Please enter a valid number.")
        elif choice == '2':
            print(Fore.CYAN + "\n[!] Exiting the program. Goodbye!")
            break
        else:
            print(Fore.RED + "[!] Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n[!] Program stopped by user.")
