import pandas as pd
import csv

def writeRow(file_name, data, dataSetPath = '.'):
    filePath = dataSetPath + '\\' + file_name
    data.to_csv(filePath, index = False, quoting=csv.QUOTE_ALL)
