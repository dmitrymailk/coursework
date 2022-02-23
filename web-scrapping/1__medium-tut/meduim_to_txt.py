import json
import os
from natsort import natsorted, ns
import pandas as pd
from progress.bar import ChargingBar


class CreateCSV:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest
        self.columns = ["title", "text"]
        self.df = pd.DataFrame(columns=self.columns)
        self.read_medium()

    def article_content(self, json_data):
        only_text = ""
        for item in json_data['data']:
            if item['type'] == "sentence":
                content = item['content'].replace(
                    "’", "'").replace("”", "\"").replace("“", "\"")
                only_text += content
        return only_text

    def read_medium(self):
        all_articles = natsorted(os.listdir(self.source), alg=ns.IGNORECASE)
        print(all_articles)
        bar = ChargingBar('Json to csv', max=len(all_articles))
        for article in all_articles:
            row = self.json_to_row(f"{self.source}{article}")
            self.df = self.df.append(row, ignore_index=True)
            bar.next()

        self.df.to_csv(self.dest, index=False)

    def json_to_row(self, json_path):
        json_data = json.load(open(f'{json_path}', "r", encoding="utf-8"))

        text = self.article_content(json_data)
        row = {}
        row["title"] = json_data["title"]
        row["text"] = text
        row["topic"] = json_data['topic']
        return row


med_to_dataframe = CreateCSV("./medium-500/", "medium-500-texts.csv")
