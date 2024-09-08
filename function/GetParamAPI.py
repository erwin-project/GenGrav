import requests
from function import DataPreparation, GetMessageAPI, Helper


def GetDataTopexParam(prompt):
    # Chat with an intelligent assistant in your terminal

    message = Helper.CleanText(prompt)

    north = Helper.query({"inputs": {"question": "What is the value of north?", "context": message}})
    south = Helper.query({"inputs": {"question": "What is the value of south?", "context": message}})
    west = Helper.query({"inputs": {"question": "What is the value of west?", "context": message}})
    east = Helper.query({"inputs": {"question": "What is the value of east?", "context": message}})
    RawDataType = Helper.query({"inputs": {"question": "What is the kind of data?", "context": message}})

    data_param_topex = {
        'north': float(Helper.CheckScore(north)) if Helper.CheckScore(north) != '' else Helper.CheckScore(north),
        'south': float(Helper.CheckScore(south)) if Helper.CheckScore(south) != '' else Helper.CheckScore(south),
        'west': float(Helper.CheckScore(west)) if Helper.CheckScore(west) != '' else Helper.CheckScore(west),
        'east': float(Helper.CheckScore(east)) if Helper.CheckScore(east) != '' else Helper.CheckScore(east),
        'RawDataType': Helper.CheckScore(RawDataType)
    }

    return data_param_topex


def GetBougerDensityParam(prompt):
    message = Helper.CleanText(prompt)
    data_param_bouger = GetDataTopexParam(message)

    return data_param_bouger
