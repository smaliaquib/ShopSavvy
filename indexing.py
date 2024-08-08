import pandas as pd
import numpy as np
from es import ElasticSearchHelper

es_helper = ElasticSearchHelper()

embd = pd.read_csv("embeddings.csv")
data = pd.read_csv("df_with_embeddings.csv")
data.drop(columns='name_description_vector', inplace=True)
data['name_description_vector'] = embd.apply(lambda row: np.array(row.values), axis=1)
docs = data.to_dict("records")

print(f"Ping ES: {es_helper.ping_es()}")
es_helper.index_documents(docs=docs)