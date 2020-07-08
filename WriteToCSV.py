import csv

def writeRow(file_path, tweets):
    with open(file_path, "w", newline = '', encoding = "UTF-8") as csvfile:
        fnames = ['tweet']
        writer = csv.DictWriter(csvfile, fieldnames=fnames)
        writer.writeheader()
        
        for tweet in tweets:
            writer.writerow({'tweet' : tweet})