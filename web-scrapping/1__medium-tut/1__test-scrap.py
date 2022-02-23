from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import json
import os
from natsort import natsorted, ns


# def get_medium_article(url, directory, topic):
#     driver = webdriver.Firefox()

#     # url = url

#     driver.get(url)

#     content = driver.page_source
#     sp = BeautifulSoup(content, features="html5lib")
#     #     price = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
#     scraped_article = {
#         "title": "",
#         "data": [],
#         "topic": topic
#     }
#     title = "without title"
#     once = True
#     if not sp.find('h1') is None:
#         once = False
#         title = sp.find('h1')
#         if title.find("strong") is None:
#             title = title.text.strip()
#         else:
#             title = title.find("strong").text
#     print(title)
#     scraped_article['title'] = title

#     list_of_blocks = ["z ab ac ae af eh ah ai", "z ab ac ae af de ah ai",
#                       "z ab ac ae af dm ah ai", "z ab ac ae af do ah ai", "z ab ac ae af dc ah ai",
#                       "z ab ac ae af dq ah ai", "z ab ac ae af fh ah ai",
#                       "z ab ac ae af dd ah ai", "z ab ac ae af dt ah ai",
#                       "z ab ac ae af fe ah ai", "z ab ac ae af ef ah ai",
#                       "z ab ac ae af dx ah ai", "z ab ac ae af ei ah ai",
#                       "z ab ac ae af ej ah ai", "z ab ac ae af df ah ai",
#                       "z ab ac ae af dv ah ai", "z ab ac ae af eg ah ai"]
#     general_blocks = []

#     for block_name in list_of_blocks:
#         content_blocks = sp.findAll('div', attrs={'class': block_name})
#         if len(content_blocks) > 0:
#             general_blocks = content_blocks
#             break

#     for general_block in general_blocks:
#         # print(f"\n{general_block['class']} - CLASS\n")
#         if len(general_block['class']) > 3:
#             for block in general_block:
#                 block_type = block.name
#                 # print(block.name, block.get_text(), block.findAll(
#                 #     "img"), len(block.findAll("img")))
#                 if block_type in ["p", "h2", "h1"] and once:
#                     title = block.get_text()[:10]

#                 if block_type == "p":
#                     scraped_article["data"].append({
#                         "type": "sentence",
#                         "content": block.get_text(),
#                     })
#                 elif block_type == "h2":
#                     scraped_article["data"].append({
#                         "type": "subtitle",
#                         "content": block.get_text(),
#                     })
#                 elif block_type == "h1":
#                     scraped_article["data"].append({
#                         "type": "subtitle",
#                         "content": block.get_text(),
#                     })
#                 elif block_type == "figure":
#                     if not block.find("img") is None:
#                         scraped_article["data"].append({
#                             "type": "image",
#                             "content": block.findAll("img")[-1]['src'],
#                         })
#                         print(block.findAll("img")[-1]['src'])

#         # print()
#     print("OK")
#     driver.quit()

#     # with open('data.json', 'w') as outfile:
#     #     json.dump(scraped_article, outfile)
#     if len(general_blocks) > 0:
#         last_number = 0
#         if len(os.listdir(directory)) > 0:

#             el = natsorted(os.listdir(directory), alg=ns.IGNORECASE)[-1]
#             # prin
#             last_number = int(el[7:el.index("-")])
#         last_number += 1
#         pure_title = re.sub("[^a-zA-Z]", " ", title)

#         with open(f'{directory}article{last_number}--{pure_title}.json', 'w') as outfile:
#             json.dump(scraped_article, outfile)


class ScrapMedArticles:
    def __init__(self, df_path, directory):
        column_names = ["link", "topic"]
        self.df = pd.read_csv(df_path)
        self.directory = directory
        self.links = [link for link in self.df['link']]
        self.topics = [link for link in self.df['topic']]

        self.process_all_articles()

    def process_all_articles(self):
        if len(self.topics) == len(self.links):
            for i in range(len(self.topics)):
                self.get_medium_article(self.links[i], self.topics[i])

    def get_medium_article(self, url, topic):
        driver = webdriver.Firefox()

        driver.get(url)

        content = driver.page_source
        sp = BeautifulSoup(content, features="html5lib")
        #     price = a.find('div', attrs={'class': '_1vC4OE _2rQ-NK'})
        scraped_article = {
            "title": "",
            "data": [],
            "topic": topic
        }
        title = "without title"
        once = True
        if not sp.find('h1') is None:
            once = False
            title = sp.find('h1')
            if title.find("strong") is None:
                title = title.text.strip()
            else:
                title = title.find("strong").text
        print(title)
        if title == "without title":
            with open('log-med.txt', 'a', encoding='utf-8') as f:
                log = f'{title} - {url}\n'
                f.write(log)
                f.close()

        scraped_article['title'] = title
        pure_title = re.sub(
            "[^a-zA-Z]", " ", title)
        if not pure_title in "".join(os.listdir("./medium-500/")):
            list_of_blocks = list(set(["z ab ac ae af eh ah ai", "z ab ac ae af de ah ai",
                                       "z ab ac ae af dm ah ai", "z ab ac ae af do ah ai", "z ab ac ae af dc ah ai",
                                       "z ab ac ae af dq ah ai", "z ab ac ae af fh ah ai",
                                       "z ab ac ae af dd ah ai", "z ab ac ae af dt ah ai",
                                       "z ab ac ae af fe ah ai", "z ab ac ae af ef ah ai",
                                       "z ab ac ae af dx ah ai", "z ab ac ae af ei ah ai",
                                       "z ab ac ae af ej ah ai", "z ab ac ae af df ah ai",
                                       "z ab ac ae af dv ah ai", "z ab ac ae af eg ah ai",
                                       "z ab ac ae af db ah ai", "z ab ac ae af dp ah ai",
                                       "z ab ac ae af dn ah ai", "z ab ac ae af dj ah ai",
                                       "z ab ac ae af ec ah ai", "z ab ac ae af dl ah ai",
                                       "z ab ac ae af du ah ai", "z ab ac ae af dl ah ai",
                                       "z ab ac ae af ds ah ai", "z ab ac ae af dn ah ai"]))

            general_blocks = []

            for block_name in list_of_blocks:
                content_blocks = sp.findAll('div', attrs={'class': block_name})
                if len(content_blocks) > 0:
                    general_blocks = content_blocks
                    break

            for general_block in general_blocks:
                # print(f"\n{general_block['class']} - CLASS\n")
                if len(general_block['class']) > 3:
                    for block in general_block:
                        block_type = block.name
                        # print(block.name, block.get_text(), block.findAll(
                        #     "img"), len(block.findAll("img")))
                        if block_type in ["p", "h2", "h1"] and once:
                            title = block.get_text()[:10]

                        if block_type == "p":
                            scraped_article["data"].append({
                                "type": "sentence",
                                "content": block.get_text(),
                            })
                        elif block_type == "h2":
                            scraped_article["data"].append({
                                "type": "subtitle",
                                "content": block.get_text(),
                            })
                        elif block_type == "h1":
                            scraped_article["data"].append({
                                "type": "subtitle",
                                "content": block.get_text(),
                            })
                        elif block_type == "figure":
                            if not block.find("img") is None:
                                scraped_article["data"].append({
                                    "type": "image",
                                    "content": block.findAll("img")[-1]['src'],
                                })
                                print(block.findAll("img")[-1]['src'])

                # print()
            print("OK")
            driver.quit()

            # with open('data.json', 'w') as outfile:
            #     json.dump(scraped_article, outfile)
            if len(general_blocks) == 0:
                with open('log-med.txt', 'a', encoding='utf-8') as f:
                    log = f'{title} - {url}\n'
                    f.write(log)
                    f.close()

            if len(general_blocks) > 0:
                last_number = 0
                if len(os.listdir(self.directory)) > 0:

                    el = natsorted(os.listdir(self.directory),
                                   alg=ns.IGNORECASE)[-1]
                    # prin
                    last_number = int(el[7:el.index("-")])
                last_number += 1
                pure_title = re.sub("[^a-zA-Z]", " ", title)

                with open(f'{self.directory}article{last_number}--{pure_title}.json', 'w') as outfile:
                    json.dump(scraped_article, outfile)
        else:
            print("already exists")
            driver.quit()


# driver_path = "C:/Users/dmitry/Documents/English App/research/web-scrapping/chromedriver"
# url = "https://medium.com/prodperfect/how-organizational-burnout-led-to-the-1986-challenger-disaster-and-what-engineering-teams-can-fe65d79d97fc"
# directory = "./test/"

med_art = ScrapMedArticles("medium-500.csv", "./medium-500/")
