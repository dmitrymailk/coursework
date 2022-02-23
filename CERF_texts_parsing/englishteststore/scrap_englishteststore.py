from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
import requests
import pprint
import base64
import json


class ScrapWebsite:
    def __init__(self):
        self.domain_name = "https://englishteststore.net"
        self.name = 'englishteststore'
        self.column_names_list = ['link', 'level', 'name']
        self.column_names_texts = ['source_text',
                                   'level', 'link', 'name', 'metadata']
        self.pages_list_urls = {
            'C1': ["https://englishteststore.net/test/reading/advanced/test{POS}/index.html", 55],
            'A2': ["https://englishteststore.net/test/reading/elementary/test{POS}/index.html", 35],
            'B1': ["https://englishteststore.net/test/reading/intermediate/test{POS}/index.html", 24],
        }

    def parse_pages_urls(self, page_list_url, level):
        page = requests.get(page_list_url)
        soup = BeautifulSoup(page.content, 'html5lib')

        links_list = soup.find(
            'div', attrs={'itemprop': 'articleBody'}).findAll('a')
        bad_chars = ["javascript", 'twitter']

        rows = []
        # get hrefs
        for item in links_list:
            href = item['href']
            article_link = self.domain_name + href
            cond = sum([int(char in href) for char in bad_chars])
            if cond == 0:
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
            list_url = list_url[0]
            # print()
            texts_links = self.parse_pages_urls(list_url, level)
            for item in texts_links:
                dataframe = dataframe.append(item, ignore_index=True)

        dataframe = dataframe.drop_duplicates(subset=['link'])
        dataframe.to_csv(f"{self.name}_links.csv", index=False)
        print('OK. Links parsed.')

    def get_all_texts(self):
        dataframe_texts = pd.DataFrame(columns=self.column_names_texts)

        for level, meta in self.pages_list_urls.items():
            for i in range(meta[1]):
                pos = "%0.2d" % (i+1)
                link = meta[0].replace("{POS}", pos)
                new_row = self.scrap_one_page(link, level)
                dataframe_texts = dataframe_texts.append(
                    new_row, ignore_index=True)

        dataframe_texts.to_csv(f'{self.name}_texts.csv', index=False)
        print('OK. Texts Parsed.')

    def scrap_one_page(self, url, level):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        html_page = str(soup)
        base64_text = re.findall(
            r'(var data = ".*")', html_page)[0].replace('var data = "', "").replace('"', '')

        decodedBytes = base64.urlsafe_b64decode(base64_text)
        decodedStr = json.loads(
            str(decodedBytes, "utf-8"))
        decodedStr = decodedStr['d']['sl']['g']

        text = ""
        for item in decodedStr:
            if item['S']:
                text = item['S'][0]['D']['d'][0]
                break
        text = self.remove_trash(text)

        row = {
            'level': level,
            'source_text': text,
            'link': url,
            'name': self.name,
            'metadata': "{}"
        }

        return row

    def remove_trash(self, text=None):
        new_text = str(text)
        new_text = new_text.replace('\n', " ")

        regex_array = [
            r"[’”“–]",
            r"(Question 1.*)",
            r"(\s{2,}|\\r|\\n)"
        ]
        for regex_str in regex_array:
            search_line = re.compile(regex_str)
            new_text = search_line.sub("", new_text).strip()

        return new_text


if __name__ == '__main__':
    site_scrapper = ScrapWebsite()
    # site_scrapper.get_all_links()
    site_scrapper.get_all_texts()
    # link = "https://englishteststore.net/test/reading/advanced/test55/index.html"
    # link = "https://englishteststore.net/index.php?option=com_content&view=article&id=2919:english-advanced-reading-comprehension-test-001&catid=201&Itemid=143"
    # site_scrapper.parse_pages_urls(link, 'a1')
    # site_scrapper.scrap_one_page(link, "a1")
