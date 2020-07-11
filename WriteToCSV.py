import pandas as pd

def writeRow(file_name, dict_val, dataSetPath = '.'):
    data = pd.DataFrame(dict_val)
    filePath = dataSetPath + '\\' + file_name
    print(filePath)
    data.to_csv(filePath, index = False)
