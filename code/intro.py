# coding: utf-8
import pickle

import luigi
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SortData(luigi.Task):
    file = luigi.ListParameter(default=['names.txt'])
    lines_to_load = luigi.IntParameter(default=100)

    def output(self):
        return luigi.LocalTarget('sorted.txt')

    def run(self):
        for i in self.file:
            with open(i, 'r') as in_file:
                if self.lines_to_load:
                    names = [next(in_file) for _ in range(self.lines_to_load)]
                else:
                    names = in_file.readlines()
        names = sorted(names)

        with self.output().open('w') as out_file:
            for name in names:
                print(name, file=out_file, end='')


class FindSimilar(luigi.Task):

    def requires(self):
        return SortData()

    def run(self):
        with self.input().open('r') as f:
            data = f.readlines()
            data = np.array(data)

        vec = TfidfVectorizer(ngram_range=(1, 3), analyzer='word', stop_words=None)
        ft = vec.fit_transform(data)
        groups = []
        for i in range(ft.shape[0] - 1):
            grp = set()
            sim = cosine_similarity(ft[i], ft[i + 1])
            grp.add(data[i])
            if sim > 0.01:
                groups.append(grp)
            grp.add(data[i + 1])

            if ft.shape[0] % 100 == 0:
                self.set_status_message('{:.2f}'.format(100 * i / len(data)))

        # dmp = pickle.dumps(groups)
        with self.output().open('w') as out_file:
            # out_file.write(dmp)
            pickle.dump(groups, out_file)

    def output(self):
        return luigi.LocalTarget('result.pickle', format=luigi.format.Nop)
