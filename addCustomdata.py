import pandas as pd

df = pd.read_csv('data/combinedData/averagedObservables.csv')
indexList= list(range(0,df.shape[0]))
df['index'] = indexList
print(df.head())
df.to_csv("data/combinedData/averagedObservables2.csv", index=False)






