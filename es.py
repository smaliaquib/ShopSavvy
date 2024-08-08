import os
import json
import re

import openai
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
import elasticsearch
from tqdm import tqdm

from indexMapping import indexMapping

load_dotenv()
class ElasticSearchHelper:
    def __init__(self):
        self.host = os.getenv('ELASTICSEARCH_HOST')
        self.port = os.getenv('ELASTICSEARCH_PORT')
        self.username = os.getenv('ELASTICSEARCH_USERNAME')
        self.password = os.getenv('ELASTICSEARCH_PASSWORD')
        self.ca_cert = os.getenv("CA_CERT")
        self.index_name = os.getenv("INDEX_NAME")
        
        self.es = Elasticsearch(
            f"https://{self.host}:{self.port}",
            basic_auth=(self.username,self.password),
            ca_certs=self.ca_cert
        )

    def ping_es(self):
        return self.es.ping()

    def index_documents(self, docs):
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
        self.es.indices.create(index=self.index_name, mappings=indexMapping)
        for doc in tqdm(docs, total=len(docs)):
            try:
                self.es.index(index=self.index_name, document=doc, id=doc["product_id"])
            except Exception as e:
                print(e)

class OpenAIHelper:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

    def get_embedding(self, text, model="text-embedding-ada-002"):
        return openai.Embedding.create(input=[text], model=model).data[0].embedding

    def get_response(self, prompt, model="gpt-3.5-turbo-1106"):
        response = openai.ChatCompletion.create(
            model=model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output only in JSON format. No other text or explanation."},
                {"role": "user", "content": prompt}
            ]
        )
        # print(json.loads(response.choices[0].message.content))
        return json.loads(response.choices[0].message.content)

class SearchHelper:
    def __init__(self, es_helper):
        self.es_helper = es_helper

    def get_category_list(self, df):
        return df["category"].drop_duplicates().to_list()

    def define_query(self, vector_of_input_keyword, filter_map):
        q1 = {
            "knn": {
                "field": "name_description_vector",
                "query_vector": vector_of_input_keyword,
                "k": 60,
                "num_candidates": 10000
            },
            "_source": ["product_id", "product_title", "product_description", "category", "product_price", "product_link", "product_image", "real_price"]
        }
        filter_query = {
            "bool": {
                "must": [
                    {
                        "match": {
                            "category": {
                                "query": filter_map['category'],
                                "fuzziness": 0
                            }
                        }
                    },
                    {
                        "range": {
                            "real_price": {
                                "gte": filter_map["min_price"],
                                "lte": filter_map["max_price"]
                            }
                        }
                    }
                ]
            }
        }
        return q1, filter_query

    def perform_search(self, index_name, q1, filter_query):
        print(filter_query)
        try:
            res = self.es_helper.es.knn_search(index=index_name,
                                            body=q1,
                                            request_timeout=5000,
                                            filter=filter_query)
        except elasticsearch.BadRequestError as e:
            print(f"Error: {e}")
        return [result['_source'] for result in res["hits"]["hits"]]
    

def es_main(query, df, category_list):
    es_helper = ElasticSearchHelper()
    openai_helper = OpenAIHelper()
    search_helper = SearchHelper(es_helper)

    input_keyword = query
    vector_of_input_keyword = openai_helper.get_embedding(input_keyword)
    prompt = f"I have data in elastic search of all ecommerce products with their description, price and the category they belongs to.\ngenders are {category_list}\nprice can be anything from 0 to 100k.\nbased on user's search query. give me json output as follows\n{{\ncategory\": \"category should be from above list only. if not specified give Uncategorized.\"\"max_price\":\"\n\"min_price\":\"\n}}\nusers query : {input_keyword}"
    filter_map = openai_helper.get_response(prompt)
    print(filter_map)

    q1, filter_query = search_helper.define_query(vector_of_input_keyword, filter_map)
    sources = search_helper.perform_search(os.getenv("INDEX_NAME"), q1, filter_query)
    return sources
