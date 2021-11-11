from pyspark.sql import SparkSession
  
spark = SparkSession.builder.getOrCreate()
  
df = spark.read.format("text").load("3000.txt")
  
df.selectExpr("split(value, ' ')\
as Text_Data_In_Rows_Using_format_load").show(4,False)
