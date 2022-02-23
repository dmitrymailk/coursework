import pandas as pd
from scipy import spatial

# dataSetI = [3, 45, 7, 2]
# dataSetII = [2, 54, 13, 15]
# result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
DATAFRAME = "./dataframes/medium-350-texts-processed-vectors.csv"

df = pd.read_csv(DATAFRAME)


def string_to_arr(string):
    string = string.split(',')
    string = [float(i) for i in string]
    return string


df['cosine_sim'] = ""
df['cosine_sim'] = df['cosine_sim'].astype("str")

for i in range(len(df)):
    target_vector = string_to_arr(df['vector'][i])
    sim_array = []
    for j in range(len(df)):
        if j != i:
            article_vector = string_to_arr(df['vector'][j])
            result = 1 - spatial.distance.cosine(target_vector, article_vector)
            article_uuid = df['uuid'][j]
            sim_array.append((article_uuid, result))
    sim_array.sort(key=lambda x: x[1], reverse=True)
    sim_array = [item[0] for item in sim_array]
    sim_array = str(sim_array[:100]).replace(
        "[", '{').replace("]", '}').replace(" ", "").replace("'", "")
    df['cosine_sim'][i] = sim_array
    df['text'][i] = df['text'][i][:187]


df = df.drop('vector', 1)

DATAFRAME = DATAFRAME.replace(".csv", "")
df.to_csv(f"{DATAFRAME}-cosine_sim.csv", index=False)
