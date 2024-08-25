from function import DataPreparation as dp, GetParamAPI as api


statement = "I want to download data from north -5.1, east 98, west 96"

DataTopexParam = api.GetDataTopexParam(statement)
print(DataTopexParam)

# DataGrav, DataTopo = dp.GetDataTopex(**DataTopexParam)
# print(DataGrav)
