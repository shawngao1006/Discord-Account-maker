import undetected_chromedriver as uc

import os
import time 
import requests
import random
import string
import sys
import threading
import queue
import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from colorama import Fore, Style, init 
from bs4 import BeautifulSoup as soup
from sys import stdout
from src import UI
from src import GmailnatorRead, GmailnatorGet, dfilter_email, pfilter_email, find_email_type

init(convert=True)

lock = threading.Lock()

def password_gen(length=8, chars= string.ascii_letters + string.digits + string.punctuation):
        return ''.join(random.choice(chars) for _ in range(length))  

# def minute_timer():
#     while True:
#         elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - start))
#         os.system(f'title Discord Generator ^| Rate Limit Timer ^| Time Elapsed {elapsed}')
#         time.sleep(0.05)
#         if elapsed == '00:01:00':
#             print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Timer finished.")
#             break

def gather_proxy():
        proxies = []
        with open('config/proxies.txt', 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            for line in lines:
                proxies.append(line.replace('\n', ''))
        return proxies

def free_print(arg):
    lock.acquire()
    stdout.flush()
    print(arg)
    lock.release()   

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_console():
    if os.name == 'nt':
        os.system('pause>nul')
    else:
        input('Press Enter to continue...')

def set_console_title(title):
    if os.name == 'nt':
        os.system(f'title {title}')

class DiscordGen:
    def __init__(self, email, username, password, proxy=None):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        if proxy:
            options.add_argument('--proxy-server=%s' % proxy)

        self.driver = uc.Chrome(options=options)

        self.email = email
        self.username = username
        self.password = password

    def _find_input(self, xpaths):
        for xpath in xpaths:
            try:
                return self.driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                continue
        raise NoSuchElementException(f'Unable to find any input matching {xpaths}')

    def _find_select(self, xpaths):
        for xpath in xpaths:
            try:
                return Select(self.driver.find_element(By.XPATH, xpath))
            except NoSuchElementException:
                continue
        return None

    def _find_button(self, texts):
        buttons = self.driver.find_elements(By.XPATH, '//button')
        for button in buttons:
            text = button.text.strip()
            if text and any(t.lower() in text.lower() for t in texts):
                return button
        for xpath in ["//button[@type='submit']", "//button[contains(@class,'button')]"]:
            try:
                return self.driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                continue
        raise NoSuchElementException('Unable to find a submit button')

    def register(self):
        self.driver.get('https://discord.com/register')

        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Loading Discord register page")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='email' or @type='email']"))
        )

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " + self.email)
        email_input = self._find_input([
            "//input[@name='email']",
            "//input[@type='email']",
        ])
        email_input.clear()
        email_input.send_keys(self.email)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " + self.username)
        username_input = self._find_input([
            "//input[@name='username']",
            "//input[@type='text' and not(@aria-hidden='true')]",
            "//input[@placeholder='Username']",
        ])
        username_input.clear()
        username_input.send_keys(self.username)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} " + self.password)
        password_input = self._find_input([
            "//input[@name='password']",
            "//input[@type='password']",
        ])
        password_input.clear()
        password_input.send_keys(self.password)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Submitting credentials")
        try:
            continue_btn = self._find_button(['Continue', 'Next', 'Sign Up', 'Create Account', 'Submit'])
            continue_btn.click()
        except NoSuchElementException:
            password_input.send_keys(Keys.ENTER)

        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Filling birthday")
        month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        month_value = random.randint(1, 12)
        day_value = random.randint(1, 28)
        year_value = random.randint(1990, 2001)

        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='birthday_month' or @placeholder='Month' or contains(@aria-label,'Month')]"))
            )
        except TimeoutException:
            free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Birthday fields not found, continuing manually.")

        month_select = self._find_select([
            "//select[@name='birthday_month']",
            "//select[contains(@aria-label,'Month')]",
        ])
        day_select = self._find_select([
            "//select[@name='birthday_day']",
            "//select[contains(@aria-label,'Day')]",
        ])
        year_select = self._find_select([
            "//select[@name='birthday_year']",
            "//select[contains(@aria-label,'Year')]",
        ])

        if month_select and day_select and year_select:
            try:
                month_select.select_by_visible_text(month_names[month_value - 1])
            except Exception:
                try:
                    month_select.select_by_value(str(month_value))
                except Exception:
                    pass
            try:
                day_select.select_by_visible_text(str(day_value))
            except Exception:
                try:
                    day_select.select_by_value(str(day_value))
                except Exception:
                    pass
            try:
                year_select.select_by_visible_text(str(year_value))
            except Exception:
                try:
                    year_select.select_by_value(str(year_value))
                except Exception:
                    pass
        else:
            month_input = self._find_input([
                "//input[@name='birthday_month']",
                "//input[contains(@placeholder,'Month')]",
                "//input[contains(@aria-label,'Month')]",
            ])
            day_input = self._find_input([
                "//input[@name='birthday_day']",
                "//input[contains(@placeholder,'Day')]",
                "//input[contains(@aria-label,'Day')]",
            ])
            year_input = self._find_input([
                "//input[@name='birthday_year']",
                "//input[contains(@placeholder,'Year')]",
                "//input[contains(@aria-label,'Year')]",
            ])

            month_input.clear()
            month_input.send_keys(str(month_value))
            day_input.clear()
            day_input.send_keys(str(day_value))
            year_input.clear()
            year_input.send_keys(str(year_value))

        try:
            submit_btn = self._find_button(['Continue', 'Next', 'Sign Up', 'Create Account', 'Submit'])
            submit_btn.click()
        except NoSuchElementException:
            pass

        while True:
            lock.acquire()
            checker = input(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Have you solved the captcha and submit? [y/n] > ")
            lock.release()
            if checker == "y":
                token = self.driver.execute_script("return window.localStorage.getItem('token')")
                if isinstance(token, str):
                    token = token.strip('"')
                self.token = token
                break
            elif checker == "n":
                sys.exit()

        return False

    def verify_account(self, link):
        self.driver.get(link)
        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Email verification page opened")

    def join_server(self, invite_url):
        if not invite_url:
            return
        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Joining server: {invite_url}")
        self.driver.get(invite_url)
        try:
            join_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'join') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept invite') or contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept')]")
                )
            )
            join_btn.click()
            free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Server join clicked")
        except TimeoutException:
            free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Could not find a join button on invite page")

    def close_driver(self):
        self.driver.close()

def start_verify(email, email_type):  #email, 'dot'/'plus'
    free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Checking email inbox.')
    raw_email = email

    if email_type == 'dot':
        email = dfilter_email(raw_email)

    if email_type == 'plus':
        email = pfilter_email(raw_email)

    g = GmailnatorRead(email, raw_email, email_type)

    retry_count = 1

    while retry_count <= 6:
        messages = g.get_inbox()  # Returns list of dicts
        for msg in messages:
            if 'discord' in msg.get('mail_subject', '').lower() or 'discord' in msg.get('mail_from', '').lower():
                # Get the full message
                message_data = g.get_single_message(msg['mail_id'])  # Returns dict with 'mail_body' key
                if message_data and 'mail_body' in message_data:
                    content_html = message_data['mail_body']
                    bs = soup(content_html, 'html.parser')
                    href_links = [a['href'] for a in bs.find_all('a')]

                    if href_links:
                        # Find Discord verification link
                        for link in href_links:
                            if 'discord' in link.lower() or 'verify' in link.lower():
                                free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Extracted discord link.')
                                return link
                        # If no specific link found, return the first one
                        discord_verify = href_links[0]
                        free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Extracted discord link.')
                        return discord_verify
                    else:
                        free_print(f'{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} No links found in Discord email.')
                else:
                    free_print(f'{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Could not retrieve message content.')
            else:
                free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Non-Discord email found. Subject: {msg.get("mail_subject", "")}')
        
        free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Inbox checked. Retry count: {retry_count}')
        free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Sleeping for 15 seconds. Waiting for Discord email.')
        time.sleep(15)
        retry_count += 1
    
    free_print(f'{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Discord keyword not found. Unable to verify account via email.')
    return False  # cant find any email with the word discord in it

def worker(proxy=None, task_queue=None, invite_url=None):
    while True:
        if task_queue is not None:
            try:
                task_queue.get_nowait()
            except queue.Empty:
                break

        if proxy:
            free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Proxy used {proxy} ")
        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Scraping email. ")

        g = GmailnatorGet()
        new_email = g.get_email()
        
        free_print(f"{Fore.LIGHTMAGENTA_EX}[*]{Style.RESET_ALL} Scraped {new_email}")
 
        email_type = find_email_type(new_email)

        if email_type =='dot':
            filtered_email = dfilter_email(new_email)

        if email_type == 'plus':
            filtered_email = pfilter_email(new_email)

        discord_usernames = []
        with open('config/discord_usernames.txt', 'r', encoding='UTF-8') as username_txt:
            lines = username_txt.readlines()
            for line in lines:
                discord_usernames.append(line.replace('\n', ''))

        username = random.choice(discord_usernames)
        password = password_gen()

        if proxy:
            d = DiscordGen(new_email, username, password, proxy=proxy)
        else:
            d = DiscordGen(new_email, username, password)

        try:
            d.register()
            token = str(d.token)
            lock.acquire()
            with open('output/login.txt', 'a', encoding='UTF-8') as login_file:
                login_file.write(new_email + ':' + password + ':' + token + '\n')      
            lock.release()
            try:
                verify_link = start_verify(new_email, email_type)
                if verify_link:
                    d.verify_account(verify_link)
                else:
                    d.verify_account('https://www.gmailnator.com/inbox/#' + new_email)

                if invite_url:
                    d.join_server(invite_url)
                pause_console()
                d.close_driver()

            except Exception as e:
                print('some error occured')
                print(e)
                d.verify_account('https://www.gmailnator.com/inbox/#' + new_email)
                if invite_url:
                    d.join_server(invite_url)
                pause_console()
                d.close_driver()   
                         
        except WebDriverException:
            free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Webdriver Error. Unable to continue.")

        free_print(f"{Fore.LIGHTMAGENTA_EX}[!]{Style.RESET_ALL} Worker task ended.")

        if task_queue is None:
            break
        task_queue.task_done()
    
def menu():
    proxies = gather_proxy()

    clear_console()

    if len(proxies) != 0:
        set_console_title('Discord Generator ^| coded by NightfallGT ^| PROXY LIST DETECTED')

    else:
        set_console_title('Discord Generator ^| coded by NightfallGT ')
    UI.banner()
    UI.start_menu()

    try:
        user_input = int(input(f"\t\t{Fore.LIGHTMAGENTA_EX}[?]{Style.RESET_ALL} > "))
        print('\n\n')
    except ValueError:
        user_input = 0

    if user_input == 1:
        clear_console()
        UI.banner()
        UI.menu2()

        try:
            user_input = int(input(f"\t\t{Fore.LIGHTMAGENTA_EX}[?]{Style.RESET_ALL} > "))
            print('\n\n')
        except ValueError:
            user_input = 0

        if user_input == 1:
            return 2

        elif user_input == 2:
            return 1

        else:
            return None
            
def main():
    continue_program = True

    m = menu()

    if m == 1:
        user_thread= True
    elif m == 2:
        user_thread = False
    else:
        continue_program = False

    if continue_program:
        num_accounts = 1
        if user_thread:
            print(f"{Fore.LIGHTMAGENTA_EX}[WARNING]{Style.RESET_ALL} Do not put a lot of threads or you will crash. 2 threads is decent. (chrome windows)")
            num_accounts = int(input(f"{Fore.LIGHTMAGENTA_EX}[>]{Style.RESET_ALL} Enter number of accounts to generate > "))
            num_thread = int(input(f"{Fore.LIGHTMAGENTA_EX}[>]{Style.RESET_ALL} Enter number of threads [eg. 3] > "))
        else:
            num_accounts = int(input(f"{Fore.LIGHTMAGENTA_EX}[>]{Style.RESET_ALL} Enter number of accounts to generate > "))

        invite_url = input(f"{Fore.LIGHTMAGENTA_EX}[>]{Style.RESET_ALL} Enter Discord invite URL to auto-join (or leave blank) > ").strip() or None

        proxies = gather_proxy()

        clear_console()
        UI.banner()
        print('\n\n')

        if user_thread:
            threads = []
            task_queue = queue.Queue()
            for _ in range(num_accounts):
                task_queue.put(1)

            if len(proxies) != 0:
                set_console_title('Discord Generator ^| Proxy: True ^| Threading: True')

                for i in range(num_thread):
                    t = threading.Thread(target=worker, args=(random.choice(proxies), task_queue, invite_url))
                    threads.append(t)
                    t.start()
            else:
                set_console_title('Discord Generator ^| Proxy: False ^| Threading: True')

                for i in range(num_thread):
                    t = threading.Thread(target=worker, args=(None, task_queue, invite_url))
                    threads.append(t)
                    t.start()

            for t in threads:
                t.join()
        else:
            if len(proxies) != 0:
                set_console_title('Discord Generator ^| Proxy: True ^| Threading: False')
                for _ in range(num_accounts):
                    worker(random.choice(proxies), None, invite_url)
            else:
                set_console_title('Discord Generator ^| Proxy: False ^| Threading: False')
                for _ in range(num_accounts):
                    worker(None, None, invite_url)

if __name__ == '__main__':
    main()
