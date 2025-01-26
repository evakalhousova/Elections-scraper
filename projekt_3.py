"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Eva Kalhousová
email: eva.kalhousova@gmail.com
discord: evakalhousova
"""

from requests import get
from bs4 import BeautifulSoup
import sys
import csv

def check_arguments():
    if len(sys.argv) != 3:
        print('To run the script, you need to enter two arguments (url and csv file name).')
        sys.exit(1)
    elif 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=' not in sys.argv[1]:
        print('To run the script, you need to enter the url of the web with election results for a region as the first argument.')
        sys.exit(1)
    elif not sys.argv[2].endswith('.csv'):
        print("To run the script, you need to enter the csv file name including the '.csv' file extension as the second argument.")
        sys.exit(1)

def load_arguments():
    check_arguments()
    url = sys.argv[1]
    csv_name = sys.argv[2]
    return url, csv_name

def get_parsed_html_region(url):
    response = get(url)
    parsed_html = BeautifulSoup(response.text, features='html.parser')
    return parsed_html

def get_town_codes(url):
    parsed_html = get_parsed_html_region(url)
    town_codes = []
    for item in parsed_html.find_all('a'):
        if item.text.isnumeric():
            town_codes.append(item.text)
    return town_codes

def format_url_town(url, town_code):
    split_url = url.split('xkraj=')[1].split('&xnumnuts=')
    region_id = split_url[0]
    choice_id = split_url[1]
    formatted_url = f'https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={region_id}&xobec={town_code}&xvyber={choice_id}'
    return formatted_url

def get_parsed_html_town(formatted_url):
    response = get(formatted_url)
    parsed_html = BeautifulSoup(response.text, features='html.parser')
    return parsed_html

def get_town_name(parsed_html):
    for item in parsed_html.find_all('h3'):
        if 'Obec: ' in item.text:
            town_name = item.text.split(': ')[-1].strip()
    return town_name

def get_general_results(parsed_html):
    registered = parsed_html.find('td', {'headers': 'sa2'}).text.replace(u'\xa0', u'')
    envelopes = parsed_html.find('td', {'headers': 'sa3'}).text.replace(u'\xa0', u'')
    valid = parsed_html.find('td', {'headers': 'sa6'}).text.replace(u'\xa0', u'')
    general_results = registered, envelopes, valid
    return general_results

def get_parties(url, town_code):
    formatted_url = format_url_town(url, town_code)
    parsed_html = get_parsed_html_town(formatted_url)
    parties = []
    for item in parsed_html.find_all('td', {'class': 'overflow_name'}):
        parties.append(item.text)
    return parties

def get_votes(parsed_html):
    votes = []
    for item in parsed_html.find_all('td', {'headers': 't1sa2 t1sb3'}):
        if item.text == '-':
            continue
        else:
            votes.append(item.text.replace(u'\xa0', u''))
    for item in parsed_html.find_all('td', {'headers': 't2sa2 t2sb3'}):
        if item.text == '-':
            continue
        else:
            votes.append(item.text.replace(u'\xa0', u''))
    return votes

def create_header(town_codes, url):
    header = ['town code', 'town name', 'registered','envelopes', 'valid']
    parties = get_parties(url, town_codes[0])
    for item in parties:
        header.append(item)
    return header

def create_towns_data(town_codes, url):
    towns_data = []
    for town_code in town_codes:
        formatted_url = format_url_town(url, town_code)
        parsed_html = get_parsed_html_town(formatted_url)
        town_name = get_town_name(parsed_html)
        general_results = get_general_results(parsed_html)
        votes = get_votes(parsed_html)
        town_data = [town_code, town_name]
        for item in general_results:
            town_data.append(item)
        for item in votes:
            town_data.append(item)
        towns_data.append(town_data)
    return towns_data

def write_into_csv(csv_name, header, towns_data):
    with open(csv_name, mode="w", encoding='utf-8', newline="") as new_csv:
        writer = csv.writer(new_csv)
        writer.writerow(header)
        writer.writerows(towns_data)

def main():
    url, csv_name = load_arguments()
    print(f'Downloading data from url: {url}')
    town_codes = get_town_codes(url)
    header = create_header(town_codes, url)
    towns_data = create_towns_data(town_codes, url)
    write_into_csv(csv_name, header, towns_data)
    print(
        f'Saving data to file: {csv_name}',
        'Ending projekt_3.py', sep="\n"
    )

main()
