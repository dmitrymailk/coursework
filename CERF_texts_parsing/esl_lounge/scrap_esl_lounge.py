from bs4 import BeautifulSoup
import re
from nltk.util import pr
import pandas as pd
import json
import os
import requests
import pprint
import itertools


class ScrapWebsite:
    def __init__(self):
        self.domain_name = "https://www.esl-lounge.com/"
        self.name = 'esl_lounge'
        self.column_names_list = ['link', 'level', 'name']
        self.column_names_texts = ['source_text',
                                   'level', 'link', 'name', 'metadata']

    def parse_pages_urls(self, page_list_url, level, position):
        page = requests.get(page_list_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        # .findAll('a', href=True)
        links_list = soup.findAll('div', attrs={'data-section-id': position})
        links_list = [item.findAll('a', href=True)
                      for item in links_list]
        links_list = list(itertools.chain(*links_list))
        links_list = list(set([str(item['href']) for item in links_list]))

        rows = []
        # get hrefs
        for item in links_list:
            href = item
            if not '../' in href:
                article_link = self.pages_list_urls[level][0] + href
                print(article_link)
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
            page_url = list_url[0]
            position = list_url[1]
            texts_links = self.parse_pages_urls(page_url, level, position)
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

        title = soup.find('h1').getText().strip()

        text = soup.find('div', attrs={'class': 'reading'})
        if not text:
            text = soup.find('div', attrs={'class': 'long-reading'})
        text = text.findAll('p')
        text = " ".join([item.getText() for item in text])
        text = self.remove_trash(text)

        # print(text)
        row = {
            'level': level,
            'source_text': text,
            'link': url,
            'name': self.name,
            'metadata': "{'title': '%s'}" % (title)
        }

        return row

    def remove_trash(self, text=None):
        new_text = str(text)
        new_text = new_text.replace('\n', " ")

        regex_array = [
            r"[’”“]",
            r"(A\. The traffic was bad.*)",
            r"(This article is licensed under the GNU.*)",
            r"Source:.*",
        ]
        for regex_str in regex_array:
            search_line = re.compile(regex_str)
            new_text = search_line.sub("", new_text).strip()

        return new_text


if __name__ == '__main__':
    site_scrapper = ScrapWebsite()
    # site_scrapper.get_all_links()
    site_scrapper.get_all_texts()
    # link = "https://www.esl-lounge.com/student/reading/1r1-toms-day.php"

    # site_scrapper.scrap_one_page(link, "a1")
