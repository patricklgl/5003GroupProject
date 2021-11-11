# the project uses "BoundingBox" in geometry.py
# for performing data points partition, 
# m I need to know the structure for plotting the graph.

# Sample
# [1, 1, 1, 2, 2, 2, 3, 3, 3, None]
# it means point 1,2,3 in cluster 1
# point 4,5,6 in cluster 2
# None = outlier 

# Sample input for partitioner
# [[  1.    1.2   0.8   3.7   3.9   3.6  10.   10.1  10.2 100. ]
#  [  1.1   0.8   1.    4.    3.9   4.1  10.   10.1  10.2 100. ]]

# X = np.array([[1, 1.1], [1.2, 0.8],[0.8, 1], [3.7, 4], [3.9, 3.9], [3.6, 4.1], [10, 10], [10.1, 10.1],[10.2, 10.2],[100,100]])



# Create a class with 2 methods spilt and enlarge as mentioned 

Class Partition(object):
  def __init__(self, data):
    self = self
   
#  def create_partitions(self, data, box):
  
  def spilt(self, data):
    return
    
  
  def enlarge(self, data):
    return 
  
# Do the partition

