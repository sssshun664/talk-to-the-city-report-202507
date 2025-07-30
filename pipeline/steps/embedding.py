
from langchain_openai import OpenAIEmbeddings
import pandas as pd
from tqdm import tqdm


def embedding(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/embeddings.pkl"
    arguments = pd.read_csv(f"outputs/{dataset}/args.csv")
    embeddings = []
    
    # 最新の埋め込みモデルを使用
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
    
    for i in tqdm(range(0, len(arguments), 1000)):
        args = arguments["argument"].tolist()[i: i + 1000]
        embeds = embedding_model.embed_documents(args)
        embeddings.extend(embeds)
    df = pd.DataFrame(
        [
            {"arg-id": arguments.iloc[i]["arg-id"], "embedding": e}
            for i, e in enumerate(embeddings)
        ]
    )
    df.to_pickle(path)
