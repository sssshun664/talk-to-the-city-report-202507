"""Generate labels for all the clusters."""

from tqdm import tqdm
from typing import List
import numpy as np
import pandas as pd
from langchain_openai import ChatOpenAI
from utils import messages, update_progress


def labelling(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/labels.csv"

    arguments = pd.read_csv(f"outputs/{dataset}/args.csv")
    clusters = pd.read_csv(f"outputs/{dataset}/clusters.csv")

    results = pd.DataFrame()

    sample_size = config['labelling']['sample_size']
    prompt = config['labelling']['prompt']
    model = config['labelling']['model']

    question = config['question']
    cluster_ids = clusters['cluster-id'].unique()

    update_progress(config, total=len(cluster_ids))

    for _, cluster_id in tqdm(enumerate(cluster_ids), total=len(cluster_ids)):
        args_ids = clusters[clusters['cluster-id']
                            == cluster_id]['arg-id'].values
        args_ids = np.random.choice(args_ids, size=min(
            len(args_ids), sample_size), replace=False)
        args_sample = arguments[arguments['arg-id']
                                .isin(args_ids)]['argument'].values

        args_ids_outside = clusters[clusters['cluster-id']
                                    != cluster_id]['arg-id'].values
        args_ids_outside = np.random.choice(args_ids_outside, size=min(
            len(args_ids_outside), sample_size), replace=False)
        args_sample_outside = arguments[arguments['arg-id']
                                        .isin(args_ids_outside)]['argument'].values

        label = generate_label(question, args_sample,
                               args_sample_outside, prompt, model)
        results = pd.concat([results, pd.DataFrame(
            [{'cluster-id': cluster_id, 'label': label}])], ignore_index=True)
        update_progress(config, incr=1)

    results.to_csv(path, index=False)


def generate_label(question, args_sample, args_sample_outside, prompt, model):
    llm = ChatOpenAI(model=model, temperature=0.0)
    outside = '\n * ' + '\n * '.join(args_sample_outside)
    inside = '\n * ' + '\n * '.join(args_sample)
    input = f"Question of the consultation:{question}\n\n" + \
        f"Examples of arguments OUTSIDE the cluster:\n {outside}" + \
        f"Examples of arguments INSIDE the cluster:\n {inside}"
    response = llm.invoke(messages(prompt, input))
    return response.content.strip()


def label_cluster(cluster: pd.DataFrame, question: str, opposite_args: List[str], prompt: str, model: str):
    sample_size = len(cluster)
    sample_cluster = cluster.sample(n=min(sample_size, 30), random_state=42)
    sampled_args = [f" * {arg}" for arg in sample_cluster["argument"].values]
    sampled_args_text = "\n".join(sampled_args)

    opposite_args_sample = opposite_args[:30] if len(
        opposite_args) > 30 else opposite_args
    opposite_args_text = "\n".join([f" * {arg}" for arg in opposite_args_sample])

    input_text = f"""Question of the consultation: "{question}"

Examples of arguments OUTSIDE the cluster of interest:

{opposite_args_text}

Examples of arguments inside the cluster:

{sampled_args_text}"""

    llm = ChatOpenAI(model=model, temperature=0.0)
    response = llm.invoke(messages(prompt, input_text))
    label = response.content.strip()
    return label
