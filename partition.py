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

class Partition(object):
  def __init__(self, data, partition_num, eps, method):

    # assuming data is in 2D    
    if len(data) != 2 or len(data[0]) != len(data[1]):
      print('Error: Only 2D data is supported. Expected same x and y dimension')
      exit(-1)
    
    # data.cache()

    self.partition_num = partition_num
    self.eps = eps

    if method not in ('spatial split'):
      print('Error: Unknown method', method)
      exit(-1)
      
    self.method = method

   
#  def create_partitions(self, data, box):
    
  def split(self, data):

    if len(data[0]) <= 0:
      # nothing to do
      return data

    if self.method == 'spatial split':
      # find the range
      minX = min(data[0])
      maxX = max(data[0])
      minY = min(data[1])
      maxY = max(data[1])

      # get the factor list of the partition num to separate the space for x and y more evenly
      factors = []
      for factor in range(1, self.partition_num+1):
        if self.partition_num % factor == 0:
          factors.append(factor)

      # default 1 x partition_num  
      x_partition_num = factors[len(factors) // 2-1]
      y_partition_num = factors[len(factors) // 2]

      # error checking
      if x_partition_num * y_partition_num != self.partition_num:
        print('Error: Incorrect x y partition', x_partition_num, y_partition_num)
        exit(-1)
      
      # split the x range by x_partition_num and that of y 
      
      x_coordinates = []
      y_coordinates = []

      for i in range(x_partition_num):
        interval = round((maxX - minX) / x_partition_num)
        x_coordinates.append(minX + i* interval)

      for i in range(y_partition_num):
        interval = round((maxY - minY) / y_partition_num)
        y_coordinates.append(minY + i * interval)

      # I will push the partition class ID here 
      data.append([])

      # Partition ID
      #  2 5 8 ...
      #  1 4 7 ...
      #  0 3 6 ...
      id_mapping = []      
      counter = 0 
      for i in range(x_partition_num):
        ylist = []
        for j in range(y_partition_num):
          ylist.append(counter)
          counter +=1
        id_mapping.append(ylist)

      for data_point in range(len(data[0])):
        mapx = x_partition_num - 1
        mapy = y_partition_num - 1
        for i in range(len(x_coordinates)):
          if data[0][data_point] < x_coordinates[i]:
            mapx = i-1
            break
        for j in range(len(y_coordinates)):
          if data[1][data_point] < y_coordinates[i]:
            mapy = j-1
            break

        data[2].append(id_mapping[mapx][mapy])

      border_coordinates = []
      for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
          next_x = maxX if i == len(x_coordinates)-1 else x_coordinates[i+1]
          next_y = maxY if j == len(y_coordinates)-1 else y_coordinates[j+1]
          border_coordinates.append((x_coordinates[i], y_coordinates[j], next_x, next_y))
    # Sample output for partitioner
    # [[  1.    1.2   0.8   3.7   3.9   3.6  10.   10.1  10.2 100. ]
    #  [  1.1   0.8   1.    4.    3.9   4.1  10.   10.1  10.2 100. ]
    #  [  1     0     3     4     4     5     2      4     4    9]]
    return data, border_coordinates 

  def expand(data, eps):
    # expand each partition by eps 
    return data
    
# Do the partition
if __name__ == '__main__':
  x = [[1, 1.2, 0.8, 3.7, 3.9, 3.6,  10., 10.1,  10.2, 100.],
    [  1.1, 0.8, 1, 4, 3.9, 4.1, 10, 10.1,  10.2, 100. ]]

  par_obj = Partition(x, 2, 0, 'spatial split')
  result, borders = par_obj.split(x)
  print(result)
  print()
  print(borders)
