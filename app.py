from flask import Flask, render_template, request
import os
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure folders exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("static/plots", exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['dataset']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Load dataset
    data = pd.read_csv(filepath)

    # Keep only numeric columns
    data = data.select_dtypes(include=['number']).dropna()

    # Scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # -------- FIND BEST K USING SILHOUETTE --------
    best_k = 2
    best_score = -1
    inertias = []

    for k in range(2, 8):
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(scaled_data)

        inertias.append(kmeans.inertia_)  # Store inertia for elbow

        score = silhouette_score(scaled_data, labels)

        if score > best_score:
            best_score = score
            best_k = k

    # -------- APPLY FINAL CLUSTERING --------
    kmeans = KMeans(n_clusters=best_k, random_state=42)
    kmeans_labels = kmeans.fit_predict(scaled_data)

    hc = AgglomerativeClustering(n_clusters=best_k)
    hc_labels = hc.fit_predict(scaled_data)

    db = DBSCAN(eps=0.5, min_samples=5)
    db_labels = db.fit_predict(scaled_data)

    # -------- CALCULATE SILHOUETTE SCORES --------
    score_kmeans = silhouette_score(scaled_data, kmeans_labels)
    score_hier = silhouette_score(scaled_data, hc_labels)

    if len(set(db_labels)) > 1 and -1 not in set(db_labels):
        score_db = silhouette_score(scaled_data, db_labels)
    else:
        score_db = -1

    scores = {
        "K-Means": score_kmeans,
        "Hierarchical": score_hier,
        "DBSCAN": score_db
    }

    best_algorithm = max(scores, key=scores.get)

    # -------- GENERATE PLOTS --------

    # KMeans
    plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=kmeans_labels)
    plt.title("K-Means Clustering")
    plt.savefig("static/plots/kmeans.png")
    plt.close()

    # Hierarchical
    plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=hc_labels)
    plt.title("Hierarchical Clustering")
    plt.savefig("static/plots/hierarchical.png")
    plt.close()

    # DBSCAN
    plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=db_labels)
    plt.title("DBSCAN Clustering")
    plt.savefig("static/plots/dbscan.png")
    plt.close()

    # Elbow Method
    plt.plot(range(2, 8), inertias)
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.savefig("static/plots/elbow.png")
    plt.close()

    return render_template(
        "result.html",
        k=best_k,
        algo=best_algorithm,
        scores=scores
    )

if __name__ == '__main__':
    app.run(debug=True)