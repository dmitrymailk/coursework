from bs4 import BeautifulSoup
import re
import pandas as pd
import json
import os
import requests
import pprint
"""
A1 => https://www.learnamericanenglishonline.com/Reading/Blue_Level_Reading/Blue_Level_Reading_Room.html
A2 => https://www.learnamericanenglishonline.com/Reading/Red_Level_Reading/Red_Level_Reading_Room.html
B1 => https://www.learnamericanenglishonline.com/Reading/Yellow_Level_Reading/Yellow_Level_Reading_Room.html
B2 => https://www.learnamericanenglishonline.com/Reading/Green_Level_Reading/Green_Level_Reading_Room.html
"""
pp = pprint.PrettyPrinter(indent=4)
# url = "https://www.learnamericanenglishonline.com/Reading/Green_Level_Reading/Green_Level_Reading_Room.html"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'html.parser')
# links_list = soup.find(
#     'td', attrs={'class': 'bodyText'}).findAll('a', href=True)
# bad_chars = ["../", 'http']
# for item in links_list:
#   for char in bad_chars:
#     href = str(item['href'])
#     cond = sum([int(char in href) for char in bad_chars])
#     # print(cond)
#     if cond == 0:
#       print(href)


class ScrapWebsite:
    def __init__(self):
        self.domain_name = "https://www.learnamericanenglishonline.com/"
        self.name = 'learnamericanenglishonline'
        self.column_names_list = ['link', 'level', 'name']
        self.column_names_texts = ['source_text',
                                   'level', 'link', 'name', 'metadata']
        self.pages_list_urls = {
            'A1': ["https://www.learnamericanenglishonline.com/Reading/Blue_Level_Reading/", "Blue_Level_Reading_Room.html"],
            'A2': ['https://www.learnamericanenglishonline.com/Reading/Red_Level_Reading/', "Red_Level_Reading_Room.html"],
            'B1': ["https://www.learnamericanenglishonline.com/Reading/Yellow_Level_Reading/", "Yellow_Level_Reading_Room.html"],
            'B2': ["https://www.learnamericanenglishonline.com/Reading/Green_Level_Reading/", "Green_Level_Reading_Room.html"],
        }

    def parse_pages_urls(self, page_list_url, level):
        page = requests.get(page_list_url)
        soup = BeautifulSoup(page.content, 'html5lib')

        links_list = soup.find(
            'td', attrs={'class': 'bodyText'}).findAll('a', href=True)
        bad_chars = ["../", 'http']

        rows = []
        # get hrefs
        for item in links_list:
            href = str(item['href'])
            cond = sum([int(char in href) for char in bad_chars])
            # print(cond)
            if cond == 0:
                # print(href)

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
            list_url = list_url[0] + list_url[1]
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

        title = soup.find('td', attrs={'class': 'pageName'})
        if title:
            title = title.getText()

        text = soup.find('td', attrs={'class': 'bodyText'}).findAll('p')
        text = " ".join([item.getText() for item in text])
        text = self.remove_trash(text)
        # print(text)

        audio_link = soup.find('iframe')['data-src']

        row = {
            'level': level,
            'source_text': text,
            'link': url,
            'name': self.name,
            'metadata': "{'audio_link': '%s', 'title': '%s'}" % (audio_link, title)
        }

        return row

    def remove_trash(self, text=None):
        new_text = str(text)
        new_text = new_text.replace('\n', " ")

        regex_array = [
            r"[’”“]",
            r"(>>>>>>>>>>.*)",
            r"(_ _ _ _ _ _ _ _ _ _.*)",
            r"(O O O O O O O O O O O O O.*)",
            r"(\^ \^ \^ \^ \^ \^ \^ \^.*)",
            r"(Answers:.*)",
            r"(Questions:.*)",
            r"(\*Vocabulary:*)",
            r"(Check your understanding:.*)",
            r"(Now you try it. Read the paragraphs above and recored your voice:.*)",
            r"(Now you try it. Read the story above..*)",
        ]
        for regex_str in regex_array:
            search_line = re.compile(regex_str)
            new_text = search_line.sub("", new_text).strip()

        return new_text


if __name__ == '__main__':
    site_scrapper = ScrapWebsite()
    # site_scrapper.get_all_links()
    site_scrapper.get_all_texts()
    # link = "https://www.learnamericanenglishonline.com/Reading/Yellow_Level_Reading/10_Janice_is_a_careful_shopper.html"

    # site_scrapper.scrap_one_page(link, "a1")
