"""Generate takeaways for all the clusters."""

from tqdm import tqdm
from typing import List
import numpy as np
import pandas as pd
from langchain_openai import ChatOpenAI
from utils import messages, update_progress


def takeaways(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/takeaways.csv"

    arguments = pd.read_csv(f"outputs/{dataset}/args.csv")
    clusters = pd.read_csv(f"outputs/{dataset}/clusters.csv")

    results = pd.DataFrame()

    sample_size = config['takeaways']['sample_size']
    prompt = config['takeaways']['prompt']
    model = config['takeaways']['model']

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

        takeaway = generate_takeaways(question, args_sample, prompt, model)
        results = pd.concat([results, pd.DataFrame(
            [{'cluster-id': cluster_id, 'takeaways': takeaway}])], ignore_index=True)
        update_progress(config, incr=1)

    results.to_csv(path, index=False)


def generate_takeaways(question, args_sample, prompt, model):
    llm = ChatOpenAI(model=model, temperature=0.0)
    inside = '\n * ' + '\n * '.join(args_sample)
    input = f"Question of the consultation:{question}\n\n" + \
        f"Examples of arguments:\n {inside}"
    response = llm.invoke(messages(prompt, input))
    return response.content.strip()
