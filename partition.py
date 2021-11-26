# Sample input for partitioner
# [[1, 1.2, 0.8, 3.7, 3.9, 3.6, 10.0, 10.1, 1.2, 13.0],
#  [1.1, 0.8, 1, 4, 3.9, 4.1, 10, 10.1, 10.2, 1.0]]

# X = np.array([[1, 1.1], [1.2, 0.8],[0.8, 1], [3.7, 4], [3.9, 3.9], [3.6, 4.1], [10, 10], [10.1, 10.1],[10.2, 10.2],[100,100]])
# source ~/.bash_profile
# source ~/.bashrc

import findspark
findspark.init()
from pyspark import SparkContext, SparkConf
sc = SparkContext()

class Partition(object):
  def __init__(self, data, partition_num, eps, method):
    
    self.partition_num = partition_num
    self.eps = eps
    self.ROUND_DIGIT = 6

    if method not in ('spatial split'):
      print('Error: Unknown method', method)
      exit(-1)
      
    self.method = method

#   def create_partitions_without_spark(self, data, border_coordinates):
#     allow_overlapping_boxes = True

#     partition_num = len(border_coordinates)
#     partitioned_data = [[ [] for j in range(2)] for i in range(partition_num)]
    
#     for i in range(len(data[0])):
#       x = data[0][i]
#       y = data[1][i]
#       for k in range(partition_num):
#         # box = (x0,y0, x1,y1)
#         box = border_coordinates[k]

#         if x < box[2] and x >= box[0] and y < box[3] and y >= box[1]:
#           partitioned_data[k][0].append(data[0][i])
#           partitioned_data[k][1].append(data[1][i])
#           if not allow_overlapping_boxes:
#             break

#     return partitioned_data

  def create_partitions_with_spark(self, data, border_coordinates):
    allow_overlapping_boxes = True

    partition_num = len(border_coordinates)
    rdd = data

    def label_partition(element):
      new_elements = []
      for k in range(partition_num):
          box = border_coordinates[k]
          x = element[0]
          y = element[1]
          if x < box[2] and x >= box[0] and y < box[3] and y >= box[1]:
              new_elements.append((element, k))
              if not allow_overlapping_boxes:
                break
          
      return new_elements

    partitioned_rdd = rdd.map(label_partition).flatMap(lambda x: x).map(lambda x: (str(x[1]),x[0])).partitionBy(partition_num,lambda k: int(k[0])).map(lambda x: x[1])
    # partitioned_rdd.glom().collect()

    return partitioned_rdd
  def split(self, data):

    if data.count() <= 0:
      # nothing to do
      return data,[]

    if self.method == 'spatial split':
      # get the factor list of the partition num to separate the space for x and y more evenly
      factors = []
      for factor in range(1, self.partition_num+1):
        if self.partition_num % factor == 0:
          # if divisible, it is a factor
          # if the factor^2 = partition_num, we should append twice 
          if factor * factor == self.partition_num:
            factors.append(factor)
          factors.append(factor)

      # default 1 x partition_num  
      x_partition_num = factors[len(factors) // 2-1]
      y_partition_num = factors[len(factors) // 2]

      # error checking
      if x_partition_num * y_partition_num != self.partition_num:
        print('Error: Incorrect x y partition', x_partition_num, y_partition_num)
        exit(-1)
      
      # store the partitioned x y left-down coordinates to set up the border
      x_coordinates = []
      y_coordinates = []

      # find the range
      minX = data.min()[0]
      maxX = data.max()[0]
      minY = data.min(lambda x: x[1])[1]
      maxY = data.max(lambda x: x[1])[1]

      # split the x range by x_partition_num and that of y 
      for i in range(x_partition_num):
        interval = round((maxX - minX) / x_partition_num)
        x_coordinates.append(minX + i* interval)

      for i in range(y_partition_num):
        interval = round((maxY - minY) / y_partition_num)
        y_coordinates.append(minY + i * interval)

      # Partition ID
      #  2 5 8 ...
      #  1 4 7 ...
      #  0 3 6 ...

      # output the border coordinates 
      border_coordinates = []
      for i in range(len(x_coordinates)):
        for j in range(len(y_coordinates)):
          # next x y is the next item in coordinate list
          # if already the last item, the next item will be the right data boundary (maxX or maxY)
          # +0.01 here is to make sure no data touch the top/right boundary for easy partition logic
          next_x = round(maxX+0.01,self.ROUND_DIGIT) if i == len(x_coordinates)-1 else x_coordinates[i+1]
          next_y = round(maxY+0.01,self.ROUND_DIGIT) if j == len(y_coordinates)-1 else y_coordinates[j+1]
          border_coordinates.append(
              (x_coordinates[i], y_coordinates[j], next_x, next_y))

      partitioned_data = self.create_partitions_with_spark(data, border_coordinates)

    # border_coordinates
    # [(0.8, 0.8, 100.0, 50.8), (0.8, 50.8, 100.0, 100.0)]

    return partitioned_data, border_coordinates

  def expand(self, data, border_coordinates):
    # expand each partition by eps 
    for i in range(len(border_coordinates)):
      border_coordinate = list(border_coordinates[i])
      border_coordinate[0] = round(border_coordinate[0] - self.eps, self.ROUND_DIGIT)
      border_coordinate[1] = round(border_coordinate[1] - self.eps, self.ROUND_DIGIT)
      border_coordinate[2] = round(border_coordinate[2] + self.eps, self.ROUND_DIGIT)
      border_coordinate[3] = round(border_coordinate[3] + self.eps, self.ROUND_DIGIT)
      border_coordinates[i] = tuple(border_coordinate)

      partitioned_data = self.create_partitions_with_spark(data,border_coordinates)
    return partitioned_data, border_coordinates
    
# Do the partition
if __name__ == '__main__':
  # x = [[1, 1.2, 0.8, 3.7, 3.9, 3.6,  10., 10.1,  1.2, 13.],
  #  [  1.1, 0.8, 1, 4, 3.9, 4.1, 10, 10.1,  10.2, 1. ]]

  lines = sc.textFile('./data/3000.txt')
  x = lines.map(lambda x: x.split()).map(lambda x: (int(x[0]),int(x[1])))

  PARTITION = 8
  EPS = 100
  par_obj = Partition(x, PARTITION, EPS, 'spatial split')
  result, borders = par_obj.split(x)

  print()
  print('==================Debug Ground==================')
  # Find the number of elements in each parttion
  def partitionsize(it): 
    yield len(list(it))
  
  # sum to 3000
  print('Size of each partition:',result.mapPartitions(partitionsize).collect())
  # print('Result', result.glom().collect())
  print('Border', borders)
  print()
  result, borders = par_obj.expand(x,borders)
  # print('After expand bounding box',result.glom().collect())
  print('Size of each partition:',result.mapPartitions(partitionsize).collect())
  print('Border', borders)