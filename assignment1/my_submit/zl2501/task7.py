import sys
from csv import reader
from pyspark import SparkContext

sc = SparkContext()
lines = sc.textFile(sys.argv[1], 1)
lines = lines.mapPartitions(lambda x: reader(x))

weekdays = lines.map(
    lambda x: (x[2], (0 if int(x[1][-2:]) in (5, 6, 12, 13, 19, 20, 26, 27) else 1))) \
    .reduceByKey(lambda x, y: x + y)
weekdays = weekdays.map(lambda x: (x[0], float(x[1] / 23)))

weekends = lines.map(
    lambda x: (x[2], (1 if int(x[1][-2:]) in (5, 6, 12, 13, 19, 20, 26, 27) else 0))) \
    .reduceByKey(lambda x, y: x + y)

weekends = weekends.map(lambda x: (x[0], float(x[1] / 8)))

res = weekends.join(weekdays).map(
    lambda x: x[0] + '\t' + "{0:.2f}".format(x[1][0]) + ', ' + "{0:.2f}".format(x[1][1]))

res.saveAsTextFile("task7.out")
