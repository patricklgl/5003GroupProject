import pandas
import pyspark as ps
import sklearn.cluster as skc
import numpy as np
import datetime
from dbscan import DBScan

if __name__ == '__main__':
    pd = pandas.read_csv('3000.txt', sep=" ", header=None)
    output = pd.T
    output.to_csv(r'SmallDataSet.txt', header=None, index=None)

    m = pandas.read_csv('SmallDataSet.txt', sep=",", header=None)
    
    rd = datetime.datetime.now()
    print("Run DBScan - ", rd)
    
    m1 = np.matrix(m)
    print (m1)
    
    eps = 200
    min_points = 2
    DB = DBScan()

    print(DB.dbscan(m1, eps, min_points))
    
    X = np.array(pd)
    K = 4
    DB.elbow(X,K)
    
    ed = datetime.datetime.now()
    print("End DBScan - ", ed)
    difference = ed - rd
    print("Total time spend - ", difference.seconds, " seconds")