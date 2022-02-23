from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from ast import literal_eval

DATAFRAME = "./dataframes/medium-350-texts-processed.csv"

model = SentenceTransformer('bert-base-nli-mean-tokens')

med_exams = pd.read_csv(DATAFRAME)

sentences = [med_exams['text'][i] for i in range(len(med_exams))]


med_exams['vector'] = ""
med_exams['vector'] = med_exams['vector'].astype("str")
sentence_embeddings = model.encode(sentences)

print(
    f"Dataframe sentences = {len(sentences)}\nBert sentences = {len(sentence_embeddings)}")

for i in range(len(med_exams)):
    embedings = str(f"{list(sentence_embeddings[i])}".replace(
        "[", '').replace("]", '')).replace(" ", "")
    med_exams['vector'][i] = embedings
print(type(med_exams['vector'][i]))

# med_exams["vector"] = med_exams['vector'].apply(np.array)

# drop texts and titles
# med_exams = med_exams.drop('text', 1)

DATAFRAME = DATAFRAME.replace(".csv", "")


med_exams.to_csv(f"{DATAFRAME}-vectors.csv", index=False)

print(med_exams.dtypes)
print(med_exams.head())
