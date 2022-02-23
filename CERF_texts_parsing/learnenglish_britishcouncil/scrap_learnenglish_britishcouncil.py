from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
import requests
import pprint
import itertools


class ScrapWebsite:
    def __init__(self):
        self.domain_name = "https://learnenglish.britishcouncil.org/"
        self.name = 'learnenglish_britishcouncil'
        self.column_names_list = ['link', 'level', 'name']
        self.column_names_texts = ['source_text',
                                   'level', 'link', 'name', 'metadata']
        self.pages_list_urls = {
            'A2': ['https://learnenglish.britishcouncil.org/skills/reading/pre-intermediate-a2/', ],
            'B1': ["https://learnenglish.britishcouncil.org/skills/reading/intermediate-b1/"],
            'B2': ["https://learnenglish.britishcouncil.org/skills/reading/upper-intermediate-b2/", ],
            'C1': ["https://learnenglish.britishcouncil.org/skills/reading/advanced-c1/"]
        }

    def parse_pages_urls(self, page_list_url, level):
        page = requests.get(page_list_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        links_list = soup.findAll(
            'div', attrs={'class': 'views-field views-field-title'})
        links_list = [str(item.find('a')['href']).split("/")[-1]
                      for item in links_list]

        rows = []
        # get hrefs
        for item in links_list:
            href = item

            article_link = self.pages_list_urls[level][0] + href
            row = {
                'link': article_link,
                'level': level,
                'name': self.name
            }
            rows.append(row)
        return rows

    def get_all_links(self):
        dataframe = pd.DataFrame(columns=self.column_names_list)

        for level, list_url in self.pages_list_urls.items():
            list_url = list_url[0]
            # print()
            texts_links = self.parse_pages_urls(list_url, level)
            for item in texts_links:
                dataframe = dataframe.append(item, ignore_index=True)

        dataframe = dataframe.drop_duplicates(subset=['link'])
        dataframe.to_csv(f"{self.name}_links.csv", index=False)
        print('OK. Links parsed.')

    def get_all_texts(self):
        dataframe_links = pd.read_csv(f"./{self.name}_links.csv")
        dataframe_texts = pd.DataFrame(columns=self.column_names_texts)
        data_len = len(dataframe_links)
        for i in range(data_len):
            # print(row)
            row = dataframe_links.iloc[i]
            level = row['level']
            link = row['link']
            new_row = self.scrap_one_page(link, level)
            dataframe_texts = dataframe_texts.append(
                new_row, ignore_index=True)
        dataframe_texts.to_csv(f'{self.name}_texts.csv', index=False)
        print('OK. Texts Parsed.')

    def scrap_one_page(self, url, level):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        title = soup.find('h1')
        title = title.getText()
        # print(soup)
        text = soup.find('div', attrs={
                         'class': 'field field-name-field-reading-text field-type-text-long field-label-hidden'}).findAll('p')
        text = " ".join([item.getText() for item in text])
        text = self.remove_trash(text)
        # print(text)

        row = {
            'level': level,
            'source_text': text,
            'link': url,
            'name': self.name,
            'metadata': "{'title': '%s'}" % title
        }

        return row

    def remove_trash(self, text=None):
        new_text = str(text)
        new_text = new_text.replace('\n', " ")

        regex_array = [
            r"[’”“–]",
            r"(_____)"
        ]
        for regex_str in regex_array:
            search_line = re.compile(regex_str)
            new_text = search_line.sub("", new_text).strip()

        return new_text


if __name__ == '__main__':
    site_scrapper = ScrapWebsite()
    # site_scrapper.get_all_links()
    site_scrapper.get_all_texts()

    # link = "https://learnenglish.britishcouncil.org/skills/reading/pre-intermediate-a2/choosing-a-conference-venue"
    # site_scrapper.scrap_one_page(link, "a1")
