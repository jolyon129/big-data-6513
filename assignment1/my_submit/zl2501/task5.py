import sys
from csv import reader
from pyspark import SparkContext

sc = SparkContext()
lines = sc.textFile(sys.argv[1], 1)
lines = lines.mapPartitions(lambda x: reader(x))

violation = lines.map(lambda x: ((x[14], x[16]), 1)) \
    .reduceByKey(lambda x, y: x + y) \
    .sortBy(lambda x: x[1], False)

greatest_items = sc.parallelize(violation.take(1)).map(lambda x: (x[0][0], x[0][1], x[1]))

output = greatest_items.map(lambda x: x[0] + ', ' + x[1] + '\t' + str(x[2]))
output.saveAsTextFile("task5.out")
