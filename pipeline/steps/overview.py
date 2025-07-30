"""Generate overview for the whole project."""

from tqdm import tqdm
from typing import List
import numpy as np
import pandas as pd
from langchain_openai import ChatOpenAI
from utils import messages, update_progress


def overview(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/overview.txt"

    labels = pd.read_csv(f"outputs/{dataset}/labels.csv")
    takeaways = pd.read_csv(f"outputs/{dataset}/takeaways.csv")

    prompt = config['overview']['prompt']
    model = config['overview']['model']

    question = config['question']

    update_progress(config, total=1)

    # Prepare the input for generating overview
    all_labels = labels['label'].values
    all_takeaways = takeaways['takeaways'].values

    overview_text = generate_overview(question, all_labels, all_takeaways, prompt, model)

    with open(path, 'w') as f:
        f.write(overview_text)

    update_progress(config, incr=1)


def generate_overview(question, labels, takeaways, prompt, model):
    llm = ChatOpenAI(model=model, temperature=0.0)
    
    labels_text = '\n * ' + '\n * '.join(labels)
    takeaways_text = '\n * ' + '\n * '.join(takeaways)
    
    input = f"Question of the consultation: {question}\n\n" + \
            f"Cluster labels:\n{labels_text}\n\n" + \
            f"Cluster takeaways:\n{takeaways_text}"
    
    response = llm.invoke(messages(prompt, input))
    return response.content.strip()
