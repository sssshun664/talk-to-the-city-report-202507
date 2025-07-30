"""Translate text to multiple languages."""

import json
from langchain_openai import ChatOpenAI
from utils import messages, update_progress
from langchain_core.messages import AIMessage


def translation(config):
    dataset = config['output_dir']
    path = f"outputs/{dataset}/translations.json"

    languages = config.get('translation', {}).get('languages', [])
    if len(languages) == 0:
        with open(path, 'w') as file:
            json.dump({}, file, indent=2)
        return

    result = {}

    # Translate config items
    result = translate_config(config, result, languages)

    # Translate arguments
    result = translate_arguments(config, result, languages)

    # Translate clusters
    result = translate_clusters(config, result, languages)

    # Translate overview
    result = translate_overview(config, result, languages)

    with open(path, 'w') as file:
        json.dump(result, file, indent=2)


def translate_config(config, result, languages):
    for field in ['name', 'question', 'intro']:
        if field in config and config[field]:
            result[config[field]] = []
            for language in languages:
                translation = translate_text(config[field], language, config['translation']['model'])
                result[config[field]].append(translation)
    return result


def translate_arguments(config, result, languages):
    import pandas as pd
    arguments = pd.read_csv(f"outputs/{config['output_dir']}/args.csv")
    
    update_progress(config, total=len(arguments))
    
    for _, row in arguments.iterrows():
        argument_text = row['argument']
        if argument_text not in result:
            result[argument_text] = []
            for language in languages:
                translation = translate_text(argument_text, language, config['translation']['model'])
                result[argument_text].append(translation)
        update_progress(config, incr=1)
    
    return result


def translate_clusters(config, result, languages):
    import pandas as pd
    labels = pd.read_csv(f"outputs/{config['output_dir']}/labels.csv")
    takeaways = pd.read_csv(f"outputs/{config['output_dir']}/takeaways.csv")
    
    # Translate labels
    for _, row in labels.iterrows():
        label_text = row['label']
        if label_text not in result:
            result[label_text] = []
            for language in languages:
                translation = translate_text(label_text, language, config['translation']['model'])
                result[label_text].append(translation)
    
    # Translate takeaways
    for _, row in takeaways.iterrows():
        takeaway_text = row['takeaways']
        if takeaway_text not in result:
            result[takeaway_text] = []
            for language in languages:
                translation = translate_text(takeaway_text, language, config['translation']['model'])
                result[takeaway_text].append(translation)
    
    return result


def translate_overview(config, result, languages):
    try:
        with open(f"outputs/{config['output_dir']}/overview.txt", 'r') as f:
            overview_text = f.read().strip()
            if overview_text and overview_text not in result:
                result[overview_text] = []
                for language in languages:
                    translation = translate_text(overview_text, language, config['translation']['model'])
                    result[overview_text].append(translation)
    except FileNotFoundError:
        pass
    
    return result


def translate_text(text, language, model):
    llm = ChatOpenAI(model=model, temperature=0.0)
    prompt = f"Translate the following text to {language}. Return only the translation without any additional text or explanation:"
    response = llm.invoke(messages("", f"{prompt}\n\n{text}"))
    
    if isinstance(response, AIMessage):
        return response.content.strip()
    else:
        return response.content.strip()
