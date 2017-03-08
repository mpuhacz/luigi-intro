import luigi
from luigi.contrib import spark
from splearn.rdd import ArrayRDD
from splearn.feature_extraction.text import SparkHashingVectorizer
from splearn.feature_extraction.text import SparkTfidfTransformer
from splearn.pipeline import SparkPipeline

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline


class SortData(spark.PySparkTask):
    lines_to_load = luigi.IntParameter(default=0)

    def main(self, sc, *args):
        names = sc.textFile('/names.txt')
        if self.lines_to_load:
            names = names.take(self.lines_to_load)
        names = names.sortByKey()
        names.saveAsTextFile('sorted.txt')  # self.output())

    def output(self):
        return luigi.LocalTarget('/sorted.txt')
