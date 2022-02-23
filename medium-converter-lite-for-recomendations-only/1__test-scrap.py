from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import json
import os
from natsort import natsorted, ns
import uuid
import hashlib


class ScrapMedArticles:
    isResearch = False

    def __init__(self, df_path, directory, count):
        column_names = ["link", "topic"]
        self.df = pd.read_csv(df_path)
        self.directory = directory
        self.links = [link for link in self.df['link']]
        self.topics = [link for link in self.df['topic']]
        self.current_article = 0
        self.count = count
        self.process_all_articles()
        self.isResearch = False

    def encode_link(self, link):
        return hashlib.sha224(
            link.encode('utf-8')).hexdigest()

    def process_all_articles(self):
        print('start')
        all_articles = len(self.topics)
        if all_articles == len(self.links) and self.count < all_articles and self.current_article < self.count:
            all_articles = self.count
            for i in range(all_articles):
                article_id = self.encode_link(self.links[i])
                if not article_id in "".join(os.listdir(self.directory)):
                    self.get_medium_article(self.links[i], self.topics[i])
            print("Complete OK!")

    def get_medium_article(self, url, topic):
        driver = webdriver.Firefox()

        driver.get(url)

        content = driver.page_source
        sp = BeautifulSoup(content, features="html5lib")

        article_id = self.encode_link(url)

        scraped_article = {
            "title": "",
            "data": [],
            "topic": topic,
            "uuid": f"{article_id}",
            "link": f"{url}"
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
                log = f"{title} - {url}\n"
                f.write(log)
                f.close()

        else:
            self.current_article += 1

            scraped_article['title'] = title.replace("’", "'").replace(
                "‘", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("…", "...").replace("–", "-")
            pure_title = re.sub(
                "[^a-zA-Z]", " ", title)

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
                content_blocks = sp.findAll(
                    'div', attrs={'class': block_name})
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
                        text_pyload = ""

                        if block_type in ["p", "h2", "h1"]:
                            text_pyload = block.get_text().replace("’", "'").replace(
                                "‘", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("…", "...").replace("–", "-")

                        if block_type in ["p", "h2", "h1"] and once:
                            title = text_pyload[:10]

                        if block_type == "p":
                            scraped_article["data"].append({
                                "type": "sentence",
                                "content": text_pyload,
                            })
                        elif block_type == "h2":
                            scraped_article["data"].append({
                                "type": "subtitle",
                                "content": text_pyload,
                            })
                        elif block_type == "h1":
                            scraped_article["data"].append({
                                "type": "subtitle",
                                "content": text_pyload,
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
                    log = f'{title} - {url} {article_id}\n'
                    f.write(log)
                    f.close()

            if len(general_blocks) > 0:
                if self.isResearch:
                    last_number = 0
                    if len(os.listdir(self.directory)) > 0:

                        el = natsorted(os.listdir(self.directory),
                                       alg=ns.IGNORECASE)[-1]
                        # prin
                        last_number = int(el[7:el.index("-")])
                    last_number += 1
                    pure_title = re.sub("[^a-zA-Z]", " ", title)

                    with open(f'{self.directory}article{last_number}--{pure_title}.json', 'w', encoding='utf-8') as outfile:
                        json.dump(scraped_article, outfile)
                else:
                    with open(f'{self.directory}{article_id}.json', 'w', encoding='utf-8') as outfile:
                        json.dump(scraped_article, outfile)
            # else:
            #     print("already exists")
            #     driver.quit()


# driver_path = "C:/Users/dmitry/Documents/English App/research/web-scrapping/chromedriver"
# url = "https://medium.com/prodperfect/how-organizational-burnout-led-to-the-1986-challenger-disaster-and-what-engineering-teams-can-fe65d79d97fc"
# directory = "./test/"

med_art = ScrapMedArticles("medium-500.csv", "./medium_500_files/", 500)
