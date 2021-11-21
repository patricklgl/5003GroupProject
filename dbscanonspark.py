import pandas
# import pyspark as ps
import sklearn.cluster as skc
import numpy as np
from dbscan import DBScan

if __name__ == '__main__':
    pd = pandas.read_csv('3000.txt', sep=" ", header=None)
    output = pd.T
    output.to_csv(r'SmallDataSet.txt', header=None, index=None)

    m = pandas.read_csv('SmallDataSet.txt', sep=",", header=None)
    m1 = np.matrix(m)
    print (m1)
    
    eps = 2300
    min_points = 2

    DB = DBScan()

    print(DB.dbscan(m1, eps, min_points))
    
    X = np.array(pd)
    K = 4
    DB.elbow(X, K)