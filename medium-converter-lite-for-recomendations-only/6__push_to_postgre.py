from sqlalchemy import create_engine
from sqlalchemy import text

import pandas as pd
import numpy as np
df = pd.read_csv(
    "./dataframes/medium-350-texts-processed-vectors-cosine_sim.csv")
engine = create_engine(
    'postgresql://postgres:123@192.168.120.37:5432/mydatabase-8-27-20')
# engine = create_engine('postgres://rtojjxph:58NCmCIhCDvHi-pM8d5mLUuLlpjHQF94@ruby.db.elephantsql.com:5432/rtojjxph')
df.to_sql('medium_texts', engine, if_exists='append', index=False)
sql = text('ALTER TABLE public.medium_texts ALTER COLUMN cosine_sim TYPE text[] USING cosine_sim::text[];')
engine.execute(sql)
# sql = text('ALTER TABLE public.medium_texts DROP COLUMN index;')
# engine.execute(sql)
