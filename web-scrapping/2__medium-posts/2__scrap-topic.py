from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import re
import json
import os
from natsort import natsorted, ns
from concurrent.futures import ProcessPoolExecutor
from tqdm.notebook import tqdm


# def scrap_topic(url):
#     driver = webdriver.Firefox()
#     driver.get(url)

#     content = driver.page_source
#     sp = BeautifulSoup(content, features="html5lib")

#     list_of_blocks = ["hi hj ai fc r hk hl hm hn ho"]
#     general_blocks = []

#     for block_name in list_of_blocks:
#         content_blocks = sp.findAll('section', attrs={'class': block_name})
#         general_blocks = content_blocks
#     print(len(general_blocks))
#     print("OK")
#     driver.quit()
#     topic_hrefs = []
#     medium = "https://medium.com"

#     for block in general_blocks:
#         href = str(block.find("a")['href'])
#         if not medium in href:
#             href = f"{medium}{href}"
#             if '?' in href:
#                 href = href[:href.index("?")]
#         # print(href)
#         topic_hrefs.append(href)
#     # print(len(topic_hrefs))

#     return topic_hrefs


# url = "https://medium.com/topic/business"
# # scrap_topic(url)
# column_names = ["link", "topic"]
# med_df = pd.DataFrame(columns=column_names)

# topics = ["https://medium.com/topic/business"]


# def create_med_df(topics):
#     for topic in topics:
#         links = scrap_topic(topic)
#         topic_name = topic[url.index("topic")+6:]
#         for link in links:
#             row = {}
#             row['topic'] = str(topic_name)
#             row['link'] = str(link)
#             # print(row)
#             med_df = med_df.append(row, ignore_index=True)
# print('ok')


# create_med_df(topics)
# med_df.to_csv("medium-500.csv", index=False)


class ScrapMedTopics:
    def __init__(self, topics):
        column_names = ["link", "topic"]
        self.med_df = pd.DataFrame(columns=column_names)
        self.topics = topics
        # self.create_med_df()
        self.create_med_df_paralell()

    # def create_med_df(self):
    #     for topic in self.topics:
    #         links = self.scrap_topic(topic)
    #         topic_name = topic[topic.index("topic")+6:]
    #         for link in links:
    #             if not self.med_df['link'].str.contains(str(link)).any():
    #                 row = {}
    #                 row['topic'] = str(topic_name)
    #                 row['link'] = str(link)
    #                 self.med_df = self.med_df.append(row, ignore_index=True)

    def create_med_df_func(self, topic):
        links = self.scrap_topic(topic)
        topic_name = topic[topic.index("topic")+6:]
        dataframe = pd.DataFrame(columns=["link", "topic"])
        for link in links:
            if not self.med_df['link'].str.contains(str(link)).any():
                row = {}
                row['topic'] = str(topic_name)
                row['link'] = str(link)
                dataframe = dataframe.append(row, ignore_index=True)
        return dataframe

    def create_med_df_paralell(self):
        with ProcessPoolExecutor(max_workers=6) as executor:
            self.med_df = pd.concat([df for df in executor.map(
                self.create_med_df_func, self.topics)], ignore_index=True)

    def scrap_topic(self, url):
        topic_hrefs = []
        while len(topic_hrefs) < 20:
            driver = webdriver.Firefox()
            # driver.execute_script("window.scrollTo(0, 1000)")
            driver.get(url)

            content = driver.page_source
            sp = BeautifulSoup(content, features="html5lib")
            # while len(sp.findAll('section', attrs={'class': "hi hj ai fc r hk hl hm hn ho"})) < 34:
            #     print('wait')

            list_of_blocks = list(set([
                "hi hj ai fc r hk hl hm hn ho",
                "hb hc ai fc r hd he hf hg hh",
                "hi hj ai fc r hk hl hm hn ho",
                "hk hl aj fg s hm hn ho hp hq",
                "hd he aj fg s hf hg hh hi hj",
                "hj hk aj ff s hl hm hn ho hp",
                "hk hl aj fg s hm hn ho hp hq",
                "hd he aj fg s hf hg hh hi hj",
                "gp gq aj fg s gr gs gt gu gv",
                "hh hi aj fg s hj hk hl hm hn",
                "hk hl aj fg s hm hn ho hp hq",
                "hc hd aj ff s he hf hg hh hi",
                "gz ha aj ff s hb hc hd he hf",
                "gz ha aj ff s hb hc hd he hf",
                "hc hd aj ff s he hf hg hh hi",
                "hc hd aj ff s he hf hg hh hi",
                "hg hh aj ff s hi hj hk hl hm",
                "hg hh aj ff s hi hj hk hl hm",
                "hg hh aj ff s hi hj hk hl hm",
                "hg hh aj ff s hi hj hk hl hm"

            ]))
            general_blocks = []

            # wait = WebDriverWait(driver, 10)
            # men_menu = wait.until(
            #     len(sp.findAll('section', attrs={'class': list_of_blocks[0]})) < 34)

            for block_name in list_of_blocks:
                content_blocks = sp.findAll(
                    'section', attrs={'class': block_name})
                # print(content_blocks)
                if len(content_blocks) >= 30:
                    general_blocks.extend(content_blocks)
                    break

            print(len(general_blocks), url)
            print("OK")
            driver.quit()

            medium = "https://medium.com"

            for block in general_blocks:
                href = str(block.find("a")['href'])
                if not "https://" in href:
                    href = f"{medium}{href}"
                if '?' in href:
                    href = href[:href.index("?")]
                # print(href)
                topic_hrefs.append(href)
            # print(len(topic_hrefs))

        return topic_hrefs


if __name__ == '__main__':
    medium_topics = open('medium_topics.txt', 'r', encoding='utf')
    medium_topics.seek(0)
    topics = list(set([topic.rstrip("\n")
                       for topic in medium_topics.readlines()]))
    # print(topics, f'Length = {len(topics)}')

    scrap = ScrapMedTopics(topics)
    print(scrap.med_df)
    scrap.med_df.to_csv("medium_700_GEN_5_23_21.csv", index=False)
