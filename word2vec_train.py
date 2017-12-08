from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SparkSession
#from pyspark.ml.evaluation import RegressionEvaluator
#from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
#from pyspark.ml.feature import StringIndexer

from pyspark.streaming import StreamingContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.clustering import StreamingKMeans

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.datasets import dump_svmlight_file
from sklearn.datasets import *
import numpy as np
import os


from pyspark.mllib.feature import Word2Vec



#conf = SparkConf().setAppName("App")

#sc = SparkContext(conf=conf)


conf = SparkConf().setAppName("Jack").setMaster("local").set('spark.driver.memory', '6G').set('spark.driver.maxResultSize', '10G')
#conf = SparkConf().setAppName("Jack").setMaster("local")
sc = SparkContext.getOrCreate(conf = conf)
spark = SparkSession.builder.appName("Python Spark SQL Example").getOrCreate()

# ml version
'''
from pyspark.ml.feature import Word2Vec
# Input data: Each row is a bag of words from a sentence or document.
documentDF = spark.createDataFrame([
    ("Hi I heard about Spark".split(" "), ),
    ("I wish Java could use case classes".split(" "), ),
    ("Logistic regression models are neat".split(" "), )
], ["text"])

# Learn a mapping from words to Vectors.
word2Vec = Word2Vec(vectorSize=3, minCount=0, inputCol="text", outputCol="result")
model = word2Vec.fit(documentDF)

result = model.transform(documentDF)
for row in result.collect():
    text, vector = row
    print("Text: [%s] => \nVector: %s\n" % (", ".join(text), str(vector)))
'''

# mllib version
'''
inp = sc.textFile("text8_lines").map(lambda row: row.split(" "))

k = 220         # vector dimensionality
word2vec = Word2Vec().setVectorSize(k)
model = word2vec.fit(inp)

print("HERE 1")

def getAnalogy(s, model):
    qry = model.transform(s[0]) - model.transform(s[1]) - model.transform(s[2])
    res = model.findSynonyms((-1)*qry,5) # return 5 "synonyms"
    res = [x[0] for x in res]
    for k in range(0,3):
        if s[k] in res:
            res.remove(s[k])
    return res[0]

print("HERE 2")
s = ('france', 'paris', 'portugal')
print(getAnalogy(s, model))
'''


file_path = 'text8'
#file_path = 'text8_lines'
#file_path = 'text8_lines_short'
#file_path = 'sample_lda_data.txt'
inp = sc.textFile(file_path).map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)

#print("OK HERE")
#synonyms = model.findSynonyms('china', 10)
#synonyms = model.findSynonyms('law', 5)
#synonyms = model.findSynonyms('1', 5)

#for word, cosine_distance in synonyms:
#    print ("{}: {}".format(word, cosine_distance))

print("HERE 1")
#model.save(sc, "myModelPath.mdl")
#model.save(sc, "text8_short2.mdl")
#model.save(sc, "text8_short4.mdl")
model.save(sc, "text8_long.mdl")
#print("HERE 1")
#sameModel = Word2VecModel.load(sc, "myModelPath")

'''
from pyspark.mllib.feature import Word2Vec

file_path = 'text8'
inp = sc.textFile(file_path).map(lambda row: row.split(" "))
word2vec = Word2Vec()
model = word2vec.fit(inp)
model.save(sc, "text8Model.mdl")
'''