import requests
from function import DataPreparation, GetMessageAPI, Helper


def GetDataTopexParam(message):
    # Chat with an intelligent assistant in your terminal
    URL_API = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(URL_API, headers=headers, json=payload)
        return response.json()

    north = query({"inputs": {"question": "What is the value of north?", "context": message}})
    south = query({"inputs": {"question": "What is the value of south?", "context": message}})
    west = query({"inputs": {"question": "What is the value of west?", "context": message}})
    east = query({"inputs": {"question": "What is the value of east?", "context": message}})
    raw_data_type = query({"inputs": {"question": "What is the kind of data?", "context": message}})

    data_param_topex = {
        'north': float(Helper.CheckScore(north)) if Helper.CheckScore(north) != '' else Helper.CheckScore(north),
        'south': float(Helper.CheckScore(south)) if Helper.CheckScore(south) != '' else Helper.CheckScore(south),
        'west': float(Helper.CheckScore(west)) if Helper.CheckScore(west) != '' else Helper.CheckScore(west),
        'east': float(Helper.CheckScore(east)) if Helper.CheckScore(east) != '' else Helper.CheckScore(east),
        'raw_data_type': Helper.CheckScore(raw_data_type)
    }

    return data_param_topex


def GetBougerDensity(message):
    # Chat with an intelligent assistant in your terminal
    URL_API = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(URL_API, headers=headers, json=payload)
        return response.json()

    north = query({"inputs": {"question": "What is the value of north?", "context": message}})
    south = query({"inputs": {"question": "What is the value of south?", "context": message}})
    west = query({"inputs": {"question": "What is the value of west?", "context": message}})
    east = query({"inputs": {"question": "What is the value of east?", "context": message}})
    raw_data_type = query({"inputs": {"question": "What is the kind of data?", "context": message}})

    data_param_topex = {
        'north': float(Helper.CheckScore(north)) if Helper.CheckScore(north) != '' else Helper.CheckScore(north),
        'south': float(Helper.CheckScore(south)) if Helper.CheckScore(south) != '' else Helper.CheckScore(south),
        'west': float(Helper.CheckScore(west)) if Helper.CheckScore(west) != '' else Helper.CheckScore(west),
        'east': float(Helper.CheckScore(east)) if Helper.CheckScore(east) != '' else Helper.CheckScore(east),
        'raw_data_type': Helper.CheckScore(raw_data_type)
    }

    return data_param_topex