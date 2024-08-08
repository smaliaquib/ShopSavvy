import logging

from es import ElasticSearchHelper
from es import es_main
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


embd = pd.read_csv("embeddings.csv")
data = pd.read_csv("df_with_embeddings.csv")
data.drop(columns='name_description_vector', inplace=True)
data['name_description_vector'] = embd.apply(lambda row: np.array(row.values), axis=1)

algorithms = ["Elastic Search", "TFIDF", "BOW"]
categories = data['category'].unique().tolist()
randomized_products = data.sample(frac=1).head(60).to_dict('records')
top_products = 60
category = data['category'].unique()
docs = data.to_dict("records")



app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

es_helper = ElasticSearchHelper()

print(f"Ping ES: {es_helper.ping_es()}")

@app.route('/')
def index():
    return render_template('index.html', categories=categories, algorithms=algorithms, products=randomized_products)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    logger.debug(f'Selected product_id: {product_id}')
    product_details = data[data['product_id'] == product_id].to_dict('records')
    if product_details:
        return render_template('product.html', product=product_details[0])
    else:
        logger.debug(f'Product with id {product_id} not found.')
        return "Product not found", 404

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    algorithm = request.form['algorithm']
    category = request.form.get('category')

    if category == "":
        df_filter = data
    else:
        df_filter = data[data['category'] == category]

    if query == "":
        return render_template('index.html', categories=categories, algorithms=algorithms, products=randomized_products)
    else:
        results = perform_search(query, algorithm, df_filter)
        return render_template('results.html', query=query, algorithm=algorithm, results=results)



def perform_search(query, algorithm, df_filter):
    if algorithm == 'TFIDF':
        return tfidf_search(query, df_filter)
    elif algorithm == 'BOW':
        return bow_search(query, df_filter)
    elif algorithm == 'Elastic Search':
        return es_search(query, df_filter, category)
    return []

def es_search(query, df_filter, category):
    results = es_main(query, df_filter, category)
    return results

def tfidf_search(query, df_filter):
    # Preprocess data to handle missing values
    # df_filter['product_description'] = df_filter['product_description'].fillna('')
    vectorizer = TfidfVectorizer()
    # docs = (df_filter['product_title'] + df_filter['product_description']).tolist()
    docs = df_filter['name_description'].tolist()
    X = vectorizer.fit_transform(docs)
    # results = similarity(X, vectorizer, query, df_filter)
    query_vec = vectorizer.transform([query])
    similarities = np.dot(X, query_vec.T).toarray().flatten()
    top_indices = np.argsort(-similarities)[:top_products]
    results = df_filter.iloc[top_indices]
    return results[['category','product_id','product_title', 'product_image', 'product_link', 'product_price', 'product_description']].to_dict(
        'records')


def bow_search(query, df_filter):
    # df_filter['product_description'] = df_filter['product_description'].fillna('')
    vectorizer = CountVectorizer()
    # docs = (df_filter['product_title'] + df_filter['product_description']).tolist()
    docs = df_filter['name_description'].tolist()
    X = vectorizer.fit_transform(docs)
    query_vec = vectorizer.transform([query])
    similarities = np.dot(X, query_vec.T).toarray().flatten()
    results = df_filter.iloc[np.argsort(-similarities)[:top_products]]
    return results[['category','product_id','product_title', 'product_image', 'product_link', 'product_price', 'product_description']].to_dict(
        'records')


if __name__ == '__main__':
    app.run(debug=True)
