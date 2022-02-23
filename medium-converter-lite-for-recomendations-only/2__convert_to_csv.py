import json
import os
from natsort import natsorted, ns
import pandas as pd
# from progress.bar import ChargingBar


class CreateCSV:
    def __init__(self, source, dest, text_only=False):
        self.source = source
        self.dest = dest
        self.columns = ["title", "text"]
        self.df = pd.DataFrame(columns=self.columns)
        self.text_only = text_only
        self.read_medium()

    def article_content(self, json_data):
        only_text = ""
        for item in json_data['data']:
            if item['type'] == "sentence":
                content = item['content']
                only_text += content
        return only_text

    def get_first_img(self, json_data):
        img_path = ""
        for item in json_data["data"]:
            if item['type'] == 'image':
                img_path = item['content']
                break
        return img_path

    def read_medium(self):
        all_articles = natsorted(os.listdir(self.source), alg=ns.IGNORECASE)
        print(len(all_articles))
        # bar = ChargingBar('Json to csv', max=len(all_articles))
        for article in all_articles:
            row = self.json_to_row(f"{self.source}{article}")
            if row != 0:
                self.df = self.df.append(row, ignore_index=True)
                # bar.next()
            else:
                print(article)

        self.df.to_csv(self.dest, index=False)

    def json_to_row(self, json_path):
        json_data = json.load(open(f'{json_path}', "r", encoding="utf-8"))

        text = self.article_content(json_data)
        img = self.get_first_img(json_data)
        if img == "" and not self.text_only:
            return 0
        row = {}
        row["title"] = json_data["title"]
        row["text"] = text
        row["topic"] = json_data['topic']
        row['uuid'] = json_data["uuid"]
        row['link'] = json_data["link"]
        row['img'] = img
        return row


med_to_dataframe = CreateCSV(
    "./medium_for_NER/", "./dataframes/medium_for_NER_2_14_21.csv", text_only=True)
