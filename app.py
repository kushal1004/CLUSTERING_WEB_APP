from flask import Flask, render_template, request
import os
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

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

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Load dataset
    data = pd.read_csv(filepath)

    # Keep only numeric columns
    data = data.select_dtypes(include=['number']).dropna()

    # ❌ Edge case
    if data.shape[1] < 2:
        return "Dataset must have at least 2 numeric columns"

    # Scale data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # 🔥 PCA for better visualization
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(scaled_data)

    # -------- FIND BEST K --------
    best_k = 2
    best_score = -1
    inertias = []

    for k in range(2, 8):
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(scaled_data)

        inertias.append(kmeans.inertia_)

        try:
            score = silhouette_score(scaled_data, labels)
            if score > best_score:
                best_score = score
                best_k = k
        except:
            continue

    # -------- FINAL MODELS --------
    kmeans = KMeans(n_clusters=best_k, random_state=42)
    kmeans_labels = kmeans.fit_predict(scaled_data)

    hc = AgglomerativeClustering(n_clusters=best_k)
    hc_labels = hc.fit_predict(scaled_data)

    # Slightly improved DBSCAN
    db = DBSCAN(eps=0.7, min_samples=5)
    db_labels = db.fit_predict(scaled_data)

    # -------- SCORES --------
    def safe_score(data, labels):
        try:
            if len(set(labels)) > 1 and -1 not in set(labels):
                return silhouette_score(data, labels)
        except:
            pass
        return -1

    score_kmeans = safe_score(scaled_data, kmeans_labels)
    score_hier = safe_score(scaled_data, hc_labels)
    score_db = safe_score(scaled_data, db_labels)

    scores = {
        "K-Means": score_kmeans,
        "Hierarchical": score_hier,
        "DBSCAN": score_db
    }

    best_algorithm = max(scores, key=scores.get)

    print("Scores:", scores)  # Debug

    # -------- PLOT FUNCTION --------
    def plot_clusters(data_2d, labels, title, filename):
        plt.figure()
        plt.scatter(data_2d[:, 0], data_2d[:, 1], c=labels, cmap='viridis', s=30)
        plt.title(title)
        plt.xlabel("Component 1")
        plt.ylabel("Component 2")
        plt.tight_layout()
        plt.savefig(f"static/plots/{filename}")
        plt.close()

    # -------- GENERATE PLOTS --------
    plot_clusters(reduced_data, kmeans_labels, "K-Means Clustering", "kmeans.png")
    plot_clusters(reduced_data, hc_labels, "Hierarchical Clustering", "hierarchical.png")
    plot_clusters(reduced_data, db_labels, "DBSCAN Clustering", "dbscan.png")

    # Elbow Method
    plt.figure()
    plt.plot(range(2, 8), inertias, marker='o')
    plt.xlabel("Number of Clusters (K)")
    plt.ylabel("Inertia")
    plt.title("Elbow Method")
    plt.tight_layout()
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