import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("Real estate data - Copy.csv")

engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/real estate DB")

df.to_sql("Real estate data", engine, if_exists="replace", index=False)

print("Import successful")
