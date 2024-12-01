#! /usr/bin/env python3

import os
import yaml
import json
import time
import random
import logging
import requests
import argparse
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser(description='Add keywords to F5Bot.')
    parser.add_argument('-u', '--username', type=str, help='Username for F5Bot', default=os.getenv('F5BOT_USERNAME'))
    parser.add_argument('-p', '--password', type=str, help='Password for F5Bot', default=os.getenv('F5BOT_PASSWORD'))
    parser.add_argument('-i', '--input', type=str, required=True, help='Input YAML file with keywords')
    return parser.parse_args()

def load_keywords_from_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def login(session, username, password):
    # Step 1: Get the login page to get cookies
    login_page = session.get('https://f5bot.com/login')
    login_page.raise_for_status()

    # Step 2: Get the csrf token from hidden input under form with action /login-post
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find('form', {'action': '/login-post'}).find('input', {'name': 'csrf'})['value']

    # Step 3: Send the login request with cookie, csrf, username, and password
    login_data = {
        'csrf': csrf_token,
        'email': username,
        'password': password
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8,de;q=0.7',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://f5bot.com',
        'Pragma': 'no-cache',
        'Referer': 'https://f5bot.com/login',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    login_response = session.post('https://f5bot.com/login-post', data=login_data, headers=headers)
    login_response.raise_for_status()


def get_alerts(session):
    dash_page = session.get('https://f5bot.com/dash')
    dash_page.raise_for_status()
    soup = BeautifulSoup(dash_page.text, 'html.parser')
    alerts_table = soup.find('table', {'id': 'alerts'})
    alerts_data = []
    if alerts_table:
        for row in alerts_table.find_all('tr')[1:]:
            values = [value.text for value in row.find_all('td')]
            whole_word_form = row.find('form', {'action': '/toggle-whole'})
            enabled_form = row.find('form', {'action': '/toggle-enabled'})
            whole_word = whole_word_form.find('input', {'type': 'image'})['alt'] == 'Yes'
            enabled = enabled_form.find('input', {'type': 'image'})['alt'] == 'Yes'
            hits = values[4]
            try:
                hits = int(hits)
            except ValueError:
                hits = 0

            alerts_data.append({
                'keyword': values[0],
                'flags': values[1],
                'whole_word': whole_word,
                'enabled': enabled,
                'hits': hits,
            })

    return alerts_data

def add_keyword(session, keyword, flags, whole_word, enabled):
    # Step 1: Navigate to fbot.com/dash
    dash_page = session.get('https://f5bot.com/dash')
    dash_page.raise_for_status()
    soup = BeautifulSoup(dash_page.text, 'html.parser')
    
    # Step 2: Get the csrf token
    csrf_token = soup.find('form', {'action': '/add-alert'}).find('input', {'name': 'csrf'})['value']
    
    # Step 3: Prepare the data for the POST request
    data = {
        'csrf': csrf_token,
        'keyword': keyword,
        'flags': flags,
        'whole': '1' if whole_word else '0',
        'enabled': '1' if enabled else '0'
    }
    
    # Step 4: Perform the POST request to add the keyword
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8,de;q=0.7',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://f5bot.com',
        'Pragma': 'no-cache',
        'Referer': 'https://f5bot.com/dash',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
    }
    
    response = session.post('https://f5bot.com/add-alert', data=data, headers=headers)
    response.raise_for_status()

    # Step 5: Check for success or error message
    soup = BeautifulSoup(response.text, 'html.parser')
    error_message = soup.find('div', {'class': 'error-message'}).text.strip()
    success_message = soup.find('div', {'class': 'success-message'}).text.strip()

    if error_message != "":
        return False, error_message
    else:
        return True, success_message


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    args = parse_args()
    keywords_data = load_keywords_from_yaml(args.input)
    username = args.username
    password = args.password

    if not username or not password:
        raise ValueError("Username and password must be provided either as arguments or environment variables. (F5BOT_USERNAME, F5BOT_PASSWORD)")

    session = requests.Session()
    login(session, username, password)

    for keyword in keywords_data['track_keywords']:
        success, message = add_keyword(
            session, 
            keyword['keyword'], 
            keyword.get('flags', ''), 
            keyword.get('whole_word', False), 
            keyword.get('enabled', True)
        )

        text = f"Keyword {keyword['keyword']} - Enabled: {keyword.get('enabled', True)}"
        if not success:
            text += f" - ERROR: {message}"
        logger.info(text)
        time.sleep(random.randint(1, 7))

if __name__ == "__main__":
    main()