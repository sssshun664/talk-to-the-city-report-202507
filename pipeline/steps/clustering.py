"""Cluster the arguments using UMAP + HDBSCAN and GPT-4."""

import pandas as pd
import numpy as np
from importlib import import_module


def clustering(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/clusters.csv"
    arguments_df = pd.read_csv(f"outputs/{dataset}/args.csv")
    arguments_array = arguments_df["argument"].values

    embeddings_df = pd.read_pickle(f"outputs/{dataset}/embeddings.pkl")
    embeddings_array = np.asarray(embeddings_df["embedding"].values.tolist())
    clusters = config['clustering']['clusters']

    result = cluster_embeddings(
        docs=arguments_array,
        embeddings=embeddings_array,
        metadatas={
            "arg-id": arguments_df["arg-id"].values,
            "comment-id": arguments_df["comment-id"].values,
        },
        n_topics=clusters,
    )
    result.to_csv(path, index=False)


def cluster_embeddings(
    docs,
    embeddings,
    metadatas,
    min_cluster_size=2,
    n_components=2,
    n_topics=6,
):
    # (!) we import the following modules dynamically for a reason
    # (they are slow to load and not required for all pipelines)
    SpectralClustering = import_module('sklearn.cluster').SpectralClustering
    UMAP = import_module('umap').UMAP

    umap_model = UMAP(
        random_state=42,
        n_components=n_components,
    )

    # 日本語対応：埋め込みベクトルのみでクラスタリング
    n_samples = len(embeddings)
    n_neighbors = min(n_samples - 1, 10)
    spectral_model = SpectralClustering(
        n_clusters=n_topics,
        affinity="nearest_neighbors",
        n_neighbors=n_neighbors,
        random_state=42
    )
    
    # UMAP降次元
    umap_embeds = umap_model.fit_transform(embeddings)
    
    # スペクトラルクラスタリング実行
    cluster_labels = spectral_model.fit_predict(umap_embeds)

    # 結果データフレーム作成
    result_data = []
    for i, (doc, cluster_id) in enumerate(zip(docs, cluster_labels)):
        result_data.append({
            'arg-id': metadatas['arg-id'][i],
            'x': float(umap_embeds[i, 0]),
            'y': float(umap_embeds[i, 1]),
            'probability': 1.0,  # 確信度は1.0で固定
            'cluster-id': int(cluster_id)
        })
    
    result = pd.DataFrame(result_data)
    return result
