

# import numpy as np
import multiprocessing
from tqdm import tqdm
# from score_text import ScoreText
from progress.bar import ChargingBar
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support


class MultyPool:
    def __init__(self, name):
        self.name = name

    def transform_dataset(self, row):
        # test = ScoreText(row['text'])
        row['grammar'] = 0  # test.gram.score
        row['words'] = 0  # test.voc.score
        row['score'] = 0  # test.score
        return row

    def process_docs(self):
        with ProcessPoolExecutor(max_workers=6) as executor:
            rows = []
            for row in pd.read_csv(self.name).to_dict('records'):
                rows.append(row)

            results = list(
                tqdm(executor.map(self.transform_dataset, rows), total=len(rows)))

            new_df = pd.DataFrame(results)
            output_file = f"./{self.name}".replace(".csv", "")
            output_file = f"{output_file}-processed.csv"
            new_df.to_csv(output_file, index=False)
            print('Ok')
            print(pd.read_csv(output_file).head(20))


def main(name):
    docs = MultyPool(name)
    docs.process_docs()


if __name__ == '__main__':
    freeze_support()
    # df_ted = pd.read_csv("ted-dataframe_index.csv").to_dict('records')
    name = "./dataframes/medium-350-texts.csv"
    main(name)
