from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import json
import os
from natsort import natsorted, ns
import uuid
import hashlib
from concurrent.futures import ProcessPoolExecutor


class ScrapMedArticles:
    isResearch = False

    def __init__(self, df_path, directory, count=None):
        column_names = ["link", "topic"]
        self.df = pd.read_csv(df_path)
        self.directory = directory
        self.links = [[i, link] for i, link in enumerate(self.df['link'])]
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
        # all_articles = len(self.topics)
        # if self.count:
        #     if self.count < all_articles:
        #         all_articles = self.count
        # for i in range(all_articles):
        #     article_id = self.encode_link(self.links[i])
        #     if not article_id in "".join(os.listdir(self.directory)):
        #         print(i)
        #         self.get_medium_article(self.links[i], self.topics[i])
        with ProcessPoolExecutor(max_workers=6) as executor:
            executor.map(self.get_medium_article, self.links)
        print("Complete OK!")

    def get_medium_article(self, url):
        print(url[0])
        topic = self.topics[url[0]]
        url = url[1]
        article_id = self.encode_link(url)
        if not article_id in "".join(os.listdir(self.directory)):
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

            title = "no title"
            once = True
            if not sp.find('h1') is None:
                once = False
                title = sp.find('h1')
                if title.find("strong") is None:
                    title = title.text.strip()
                else:
                    title = title.find("strong").text

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

                list_of_blocks = list(
                    set([
                        "ab ac ae af ag cx ai aj", "ab ac ae af ag dl ai aj", "aj ak al am an fm ap w",
                        "ab ac ae af ag dt ai aj", "aj ak al am an gf ap w", "ab ac ae af ag du ai aj",
                        "ab ac ae af ag dj ai aj", "ao ap aq ar as gd au v", "ab ac ae af ag di ai aj",
                        "ab ac ae af ag di ai aj", "ak al am an ao gj aq x", "ab ac ae af ag dk ai aj",
                        "ab ac ae af ag cy ai aj", "ai aj ak al am gb ao v", "aj ak al am an gh ap w",
                        "ai aj ak al am fz ao v", "aj ak al am an ga ap w", "ak al am an ao gk aq x",
                        "ab ac ae af ag cz ai aj", "ab ac ae af ag dq ai aj", "ab ac ae af ag dz ai aj",
                        "ab ac ae af ag dz ai aj", "ab ac ae af ag dn ai aj",  "ab ac ae af ag dz ai aj",
                        "ab ac ae af ag do ai aj", "ab ac ae af ag do ai aj", "ab ac ae af ag dc ai aj",
                        "ab ac ae af ag dc ai aj", "ab ac ae af ag dp ai aj", "ab ac ae af ag el ai aj",
                        "ab ac ae af ag dc ai aj", "ab ac ae af ag dp ai aj", "aj ak al am an gn ap w",
                        "ai aj ak al am gh ao v", "ak al am an ao gp aq x", "ab ac ae af ag dp ai aj",
                        "aj ak al am an fs ap w", "aj ak al am an gl ap w", "aj ak al am an fq ap w",
                        "ak al am an ao fu aq x", "aj ak al am an ft ap w", "aj ak al am an go ap w",
                        "ai aj ak al am fm ao v", "aj ak al am an go ap w", "ao ap aq ar as gj au v",
                        "ab ac ae af ag dw ai aj", "ao ap aq ar as gk au v", "ao ap aq ar as gj au v",
                        "ao ap aq ar as gj au v", "ab ac ae af ag ey ai aj", "aj ak al am an fq ap w",
                        "ab ac ae af ag cw ai aj", "ak al am an ao gq aq x", "aj ak al am an gg ap w",
                        "ab ac ae af ag dd ai aj", "ab ac ae af ag dd ai aj", "ak al am an ao gq aq x",
                        "ai aj ak al am gg ao v", "ab ac ae af ag eb ai aj", "ab ac ae af ag ei ai aj",
                        "aj ak al am an gk ap w", "aj ak al am an gj ap w", "ak al am an ao hd aq x",
                        "an ao ap aq ar fy at v", "ab ac ae af ag ee ai aj", "ap aq ar as at gk av w",
                        "ap aq ar as at gp av w", "ab ac ae af ag en ai aj", "an ao ap aq ar fy at v",
                        "ap aq ar as at gk av w", "aj ak al am an gk ap w", "ac ae af ag ah dd aj ak",
                        "ap aq ar as at gp av w", "ap aq ar as at gp av w", "ab ac ae af ag dd ai aj",
                        "ab ac ae af ag ff ai aj", "aj ak al am an hd ap w", "an ao ap aq ar gg at v",
                        "ab ac ae af ag dy ai aj", "ai aj ak al am gp ao v", "ap aq ar as at gl av w",
                        "ab ac ae af ag dy ai aj", "ak al am an ao fv aq x", "ap aq ar as at gl av w",
                        "ac ae af ag ah de aj ak", "ao ap aq ar as hb au v", "ab ac ae af ag dx ai aj",
                        "ab ac ae af ag dx ai aj", "ai aj ak al am fg ao v", "ai aj ak al am gf ao v",
                        "aj ak al am an he ap w", "ac ae af ag ah dc aj ak", "ab ac ae af ag eo ai aj",
                        "ak al am an ao gm aq x", "aj ak al am an gp ap w", "aq ar as at au gr aw x",
                        "ab ac ae af ag ek ai aj", "ai aj ak al am hc ao v", "aj ak al am an gm ap w",
                        "aj ak al am an fp ap w", "aq ar as at au gr aw x", "ab ac ae af ag ek ai aj",
                        "ao ap aq ar as ge au w", "ac ae af ag ah dp aj ak", "ab ac ae af ag de ai aj",
                        "ap aq ar as at fw av w", "aq ar as at au gu aw x", "aq ar as at au gu aw x",
                        "au av aw ax ay gn ba v", "ap aq ar as at gs av w", "ap aq ar as at ff av w",
                        "ap aq ar as at ff av w", "ap aq ar as at fw av w", "ap aq ar as at fw av w",
                        "au av aw ax ay gn ba v", "au av aw ax ay gn ba v", "ap aq ar as at ff av w",
                        "au av aw ax ay gn ba v", "aq ar as at au fz aw x", "ap aq ar as at gh av w",
                        "ap aq ar as at ff av w", "ap aq ar as at fw av w", "ap aq ar as at fd av w",
                        "ab ac ae af ag da ai aj", "ap aq ar as at ft av w", "ap aq ar as at gr av w",
                        "at au av aw ax fw az v", "av aw ax ay az go bb w", "ap aq ar as at hg av w",
                        "at au av aw ax gc az v", "ao ap aq ar as gl au v", "at au av aw ax gc az v",
                        "ao ap aq ar as fw au v", "av aw ax ay az go bb w", "aq ar as at au go aw x",
                        "ab ac ae af ag eu ai aj", "aq ar as at au fw aw x", "ao ap aq ar as gl au v",
                        "aw ax ay az ba gv bc x", "ao ap aq ar as gf au v", "ab ac ae af ag ed ai aj",
                        "ap aq ar as at ft av w", "ao ap aq ar as fk au v", "ap aq ar as at gr av w",
                        "ab ac ae af ag ch ai aj", "ap aq ar as at fq av w", "aq ar as at au gt aw x",
                        "ao ap aq ar as fq au v", "ap aq ar as at fx av w", "aq ar as at au gn aw x",
                        "ab ac ae af ag ej ai aj", "aq ar as at au gt aw x", "aq ar as at au fy aw x",
                        "aw ax ay az ba hm bc x", "au av aw ax ay gi ba w", "ab ac ae af ag ck ai aj",
                        "ab ac ae af ag dm ai aj", "ap aq ar as at fg av w", "av aw ax ay az gt bb w",
                        "ab ac ae af ag cj ai aj", "aq ar as at au fh aw x", "ap aq ar as at fc av w",
                        "ac ae af ag ah cv aj ak", "av aw ax ay az gf bb w", "au av aw ax ay gh ba v",
                        "aq ar as at au fu aw x", "ac ae af ag ah do aj ak", "av aw ax ay az gu bb w",
                        "av aw ax ay az gu bb w", "av aw ax ay az gt bb w", "aq ar as at au gj aw x",
                        "aq ar as at au gj aw x", "ac ae af ag ah ci aj ak", "aq ar as at au ge aw x",
                        "aq ar as at au ff aw x", "aq ar as at au fv aw x", "aq ar as at au gd aw x",
                        "aq ar as at au gh aw x", "ao ap aq ar as fn au v", "ab ac ae af ag cv ai aj",
                        "ap aq ar as at go av w", "ab ac ae af ag cv ai aj", "ab ac ae af ag db ai aj",
                        "ap aq ar as at fj av w", "ab ac ae af ag cv ai aj", "ap aq ar as at fs av w",
                        "ap aq ar as at fr av w", "at au av aw ax fn az v", "ab ac ae af ag ec ai aj",
                        "ap aq ar as at gc av w"
                    ]))

                general_blocks = []

                for block_name in list_of_blocks:
                    content_blocks = sp.findAll(
                        'div', attrs={'class': block_name})
                    if len(content_blocks) > 0:
                        general_blocks = content_blocks
                        break

                for general_block in general_blocks:
                    # print(general_block)
                    for block in general_block:
                        block_type = block.name
                        text_pyload = ""

                        if block_type in ["p", "h2", "h1"]:
                            text_pyload = block.get_text().replace("’", "'").replace(
                                "‘", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("…", "...").replace("–", "-")
                            if title == "no title" and once:
                                title = text_pyload[:10]
                                scraped_article['title'] = title
                                once = False

                        if block_type in ["blockquote"]:
                            text_pyload = block.get_text().replace("’", "'").replace(
                                "‘", "'").replace("“", '"').replace("”", '"').replace("—", "-").replace("…", "...").replace("–", "-")
                            # print('\n\n', block.get_text())

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
                driver.quit()

                # with open('data.json', 'w') as outfile:
                #     json.dump(scraped_article, outfile)
                if len(general_blocks) == 0:
                    with open('log-med.txt', 'a', encoding='utf-8') as f:
                        log = f'{title} - {url} {article_id}\n'
                        f.write(log)
                        f.close()

                if len(general_blocks) > 0:
                    with open(f'{self.directory}{article_id}.json', 'w', encoding='utf-8') as outfile:
                        json.dump(scraped_article, outfile)
                else:
                    print(url)


# driver_path = "C:/Users/dmitry/Documents/English App/research/web-scrapping/chromedriver"
# url = "https://medium.com/prodperfect/how-organizational-burnout-led-to-the-1986-challenger-disaster-and-what-engineering-teams-can-fe65d79d97fc"
# directory = "./test/"
if __name__ == '__main__':
    med_art = ScrapMedArticles(
        "medium_689_GEN_5_2_21.csv", "./med_5_2_21/")
