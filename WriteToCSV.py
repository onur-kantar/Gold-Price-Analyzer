import pandas as pd
import csv

def writeRow(file_name, dict_val, dataSetPath = '.'):
    data = pd.DataFrame(dict_val)
    filePath = dataSetPath + '\\' + file_name
    data.to_csv(filePath, index = False, quoting=csv.QUOTE_ALL)
