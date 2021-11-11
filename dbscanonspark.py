import pandas
pd = pandas.read_csv('3000.txt', sep=" ", header=None)
output = pd.T
output.to_csv(r'SmallDataSet.txt', header=None, index=None)
