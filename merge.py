# -*- coding: utf-8 -*-
"""merge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fo92ccCCvew_z_gtNqckc_ybKkRjhuyT
"""

class Cluster:
  def __init__(self, listOfListPointDim, listCluster):
    self.dictPoint = {}
    self.dictCluster = {}
    self.setNoise = set()
    intClusterCount = len(listCluster)
    intDimCount = len(listOfListPointDim)
    listPoint = [""] * intClusterCount
    for i in range(intDimCount):
      if len(listOfListPointDim[i]) != intClusterCount:
        raise ValueError("Cluster count was " + str(intClusterCount) + " but the number of values in dimension " + str(i + 1) + " was " + str(len(listOfListPointDim[i])) + ".")
      for j in range(len(listOfListPointDim[i])):
        listPoint[j] = listPoint[j] + str(listOfListPointDim[i][j]) + ":"
    for i in range(intClusterCount):
      # print(str(listCluster[i]) + '-' + str(listPoint[i])[:-1])
      if listCluster[i] == None:
        self.setNoise.add(str(listPoint[i])[:-1])
      else:
        if str(listPoint[i])[:-1] in self.dictPoint:
          if self.dictPoint[str(listPoint[i])[:-1]] != listCluster[i]:
            raise ValueError("One point (i.e. " + str(listPoint[i])[:-1] + ") cannot belong to 2 clusters (i.e. " + self.dictPoint[str(listPoint[i])[:-1]] + " and " + str(listCluster[i]) + ").")
        else:
          self.dictPoint[str(listPoint[i])[:-1]] = listCluster[i]
          if listCluster[i] in self.dictCluster:
            self.dictCluster[listCluster[i]].append(str(listPoint[i])[:-1])
          else:
            self.dictCluster[listCluster[i]] = [str(listPoint[i])[:-1]]
    # print(self.dictPoint)
    # print(self.dictCluster)
    # print(self.setNoise)
  def __add__(self, other):
    if type(other) != Cluster:
      raise ValueError("Only can merge Cluster objects but the provided object is in other type (i.e. " + str(type(other)) + ").")
    self.setNoise = set.union(self.setNoise, other.setNoise)
    for cluster in other.dictCluster:
      setMergeCluster = set()
      setMergePoint = set()
      for point in other.dictCluster[cluster]:
        if point not in self.dictPoint:
          setMergePoint.add(point)
        else:
          setMergeCluster.add(self.dictPoint[point])
      if len(setMergeCluster) == 0:
        listAllKey = self.dictCluster.keys()
        intNextClusterId = max(listAllKey) + 1
        # print(intNextClusterId)
        for point in setMergePoint:
          # print(point)
          self.dictPoint[point] = intNextClusterId
          if intNextClusterId in self.dictCluster:
            self.dictCluster[intNextClusterId].append(point)
          else:
            self.dictCluster[intNextClusterId] = [point]
      else:
        intMinKey = min(setMergeCluster)
        # print(intMinKey)
        setMergeCluster.remove(intMinKey)
        for point in setMergePoint:
          # print(point)
          self.dictPoint[point] = intMinKey
          self.dictCluster[intMinKey].append(point)
        for mergeCluster in setMergeCluster:
          # print(mergeCluster)
          for key, value in self.dictPoint.items():
            if value == mergeCluster:
              # print(key)
              self.dictPoint[key] = intMinKey
          for key, value in self.dictCluster.items():
            if key == mergeCluster:
              # print(value)
              self.dictCluster[intMinKey] = self.dictCluster[intMinKey] + value
          del self.dictCluster[mergeCluster]

if __name__ == "__main__":
  llPointDim1 = [[1., 1.2, 0.8, 3.7, 3.9, 3.6, 10., 10.1, 10.2, 100.],
          [1.1, 0.8, 1., 4., 3.9, 4.1, 10., 10.1, 10.2, 100.]]
  # llPointDim1 = [[1., 1.2, 0.8, 3.7, 3.9, 3.6, 10., 10.1, 10.2, 1.],
  #         [1.1, 0.8, 1., 4., 3.9, 4.1, 10., 10.1, 10.2, 1.1]]
  llPointDim2 = [[1., 3.7, 10.3, 11., 101.],
          [1.1, 4., 10.3, 11., 101.]]

  lCluster1 = [1, 1, 1, 2, 2, 2, 3, 3, 3, None]
  # lCluster1 = [1, 1, 1, 2, 2, 2, 3, 3, 3, 1]
  lCluster2 = [1, 1, 1, 2, None]

  c1 = Cluster(llPointDim1, lCluster1)
  c2 = Cluster(llPointDim2, lCluster2)

  print('*********************************')
  print("Cluster1")
  print(c1.dictPoint)
  print(c1.dictCluster)
  print(c1.setNoise)
  print('*********************************')
  print("Cluster2")
  print(c2.dictPoint)
  print(c2.dictCluster)
  print(c2.setNoise)
  print('*********************************')

  c1 + c2
  print('*********************************')
  print("Cluster1 + Cluster2")
  print(c1.dictPoint)
  print(c1.dictCluster)
  print(c1.setNoise)
  print('*********************************')