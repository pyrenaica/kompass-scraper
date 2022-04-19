#! /usr/bin/env python3

import requests
import bs4
import re

base_url = input('Le URL Kompass SVP (https://fr.kompass.com/v/.../) inclue le derniere \'/\'\n')
total_pages = int(input('Nombre total des pages:\n'))
count_comp = 0

# Create soup from url


for page in range(1, total_pages + 1):
    url = base_url + 'page-' + str(page)
    req = requests.get(base_url)
    soup = bs4.BeautifulSoup(req.text, 'lxml')
    with open('out.txt', 'a') as out_file:
        # filter out each link to each company
        for link in soup.find_all(href=re.compile('https://fr.kompass.com/c/')):
            count_comp += 1
            company_link = link['href']
            print("Getting " + company_link)
            company_req = requests.get(company_link)
            company_soup = bs4.BeautifulSoup(company_req.text, 'lxml')
            # for item in company_soup:
            # Get the title / name of company
            title = company_soup.h1.get_text(strip=True)
            # Get the address, <span> with class "spRight"
            address = company_soup.find_all('span', class_='spRight')[0].get_text(' | ', strip=True)
            out_file.write(title + '\n')
            out_file.write(address + '\n')
            description = company_soup.find_all(itemprop="description")[0]
            for string in description.stripped_strings:
                out_file.write(string + '\n')
                out_file.write('------------------' + '\n' + '\n')


print("Total des entreprises: "count_comp)
