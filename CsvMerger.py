import os, glob
import pandas as pd

def merge (filePath):  
    all_files = glob.glob(os.path.join(filePath, "*.csv"))
    all_csv = (pd.read_csv(f, encoding = 'UTF-8') for f in all_files)
    df_merged = pd.concat(all_csv, ignore_index=True)
    df_merged.to_csv("merged.csv", index = False)