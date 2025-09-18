from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('clean_data.csv')
vectorizer = TfidfVectorizer()

x = vectorizer.fit_transform(data['Combined'])

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

@app.route('/home')
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