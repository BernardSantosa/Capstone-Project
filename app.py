from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests

DATA_URL = 'https://raw.githubusercontent.com/BernardSantosa/course-rec-data/refs/heads/main/clean_data.csv'
PICKLE_URL = 'https://raw.githubusercontent.com/BernardSantosa/course-rec-data/refs/heads/main/vectorizer.pkl'

DATA_PATH = '/tmp/clean_data.csv'
PICKLE_PATH = '/tmp/vectorizer.pkl'

def download_file(url, destination):
    if not os.path.exists(destination):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

if not os.path.exists('/tmp'):
    os.makedirs('/tmp')

download_file(DATA_URL, DATA_PATH)
download_file(PICKLE_URL, PICKLE_PATH)

data = pd.read_csv(DATA_PATH)
vectorizer = pickle.load(open(PICKLE_PATH, 'rb'))
x = vectorizer.transform(data['Combined'])

def get_recommendation(text, n_rec = 7):
  inp_vec = vectorizer.transform([text])
  similiarity = cosine_similarity(inp_vec, x).flatten()

  best_sim_idx = similiarity.argmax()
  best_data = data.iloc[best_sim_idx]
  best_cluster = best_data['Cluster']

  temp_data = data['Cluster'] == best_cluster
  copy_data = data[temp_data].copy()

  spesified_data = x[temp_data.values]
  spesified_sim = cosine_similarity(inp_vec, spesified_data).flatten()

  copy_data['Similarity'] = spesified_sim

  rec = copy_data.sort_values(by = 'Similarity', ascending = False).head(n_rec)
  return rec

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    text = request.json['text']
    recoms_df = get_recommendation(text)
    recoms = recoms_df.to_dict(orient="records")
    return jsonify(recoms)

def run_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    app.run(debug=True)
