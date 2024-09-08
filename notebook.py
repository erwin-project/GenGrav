from function import DataPreparation, GetParamAPI, Helper

statement = "I want to download gravity data from north -5.1, south -5.2 west 96 east 98"
# print(Helper.CleanText(statement))

data_param_topex = GetParamAPI.GetDataTopexParam(Helper.CleanText(statement))
print(data_param_topex)

