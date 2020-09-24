from textattack.augmentation import EmbeddingAugmenter
import SentimentAnalysis as sa
import pandas as pd                     

def augmenter (x, y):
  values = y.value_counts().index.tolist()
  max_value = values[0]
  max_count = y.value_counts()[max_value]
  text_name = x.name
  target_name = y.name
  df = pd.concat([x, y], axis=1)
  lastdf = pd.DataFrame(columns=[text_name, target_name])
  augmenteddf = pd.DataFrame(columns=[text_name, target_name])
  aug = EmbeddingAugmenter(pct_words_to_swap = 1)
  
  for value in values :
    partofdf = df[y == value]
    if max_count > y.value_counts()[value]:
      for index, row in partofdf.iterrows():
        augmentedtext = aug.augment(row[0])
        if augmentedtext not in partofdf.values:
          myval = sa.analysis(augmentedtext[0])
          if myval == value:
            onedf = pd.DataFrame({text_name : [augmentedtext[0]], target_name : [value]})
            augmenteddf = augmenteddf.append(onedf)
            partofdf = partofdf.append(onedf)
            print(str(len(partofdf)) + '-' + str(max_count))
            if len(partofdf) == max_count:
              break
          else:
            continue
        else:
          continue
    lastdf = lastdf.append(partofdf, ignore_index=True)
  return lastdf