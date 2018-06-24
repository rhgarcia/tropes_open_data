import json
import os
from collections import OrderedDict

import numpy
from scipy import stats

import matplotlib.pyplot as plt
import matplotlib

def hello_world():
    return "Hello world"


class Counter(object):
    def __init__(self):
        self.val = 0

    def add(self):
        self.val += 1
        return self.val


class TropesAndFilms(object):
    def __init__(self):
        self.load_data()

    def load_data(self):
        script_dir = os.path.dirname(__file__)
        data_file_path = os.path.join(script_dir, '../data/all_films_and_their_tropes.json')

        with open(data_file_path, 'r') as file:
            self.film_dictionary = json.load(file)

        self.trope_dictionary = {}
        for film in self.film_dictionary.keys():
            trope_list = self.film_dictionary[film]
            for trope in trope_list:
                if trope not in self.trope_dictionary:
                    self.trope_dictionary[trope] = []
                self.trope_dictionary[trope].append(film)

        self.tropes_sorted_by_occurrences = sorted(self.trope_dictionary.keys(), reverse=True,
                                                   key=lambda element: len(self.trope_dictionary[element]))
        self.film_sorted_by_occurrences = sorted(self.film_dictionary.keys(), reverse=True,
                                                 key=lambda element: len(self.film_dictionary[element]))

        font = {'weight': 'regular', 'size': 8}
        matplotlib.rc('font', **font)

    def tropes_dictionary_sorted_by_number_of_films(self):
        dictionary = OrderedDict()
        for trope in self.tropes_sorted_by_occurrences:
            dictionary[trope] = len(self.trope_dictionary[trope])
        return dictionary

    def films_dictionary_sorted_by_number_of_tropes(self):
        dictionary = OrderedDict()
        for film in self.film_sorted_by_occurrences:
            dictionary[film] = len(self.film_dictionary[film])
        return dictionary

    def trope_observations_by_film(self):
        return [len(values) for values in self.film_dictionary.values()]

    def film_observations_by_trope(self):
        return [len(values) for values in self.trope_dictionary.values()]

    def descriptive_statistics_for_tropes_by_film(self):
        return self.get_statistics_for_observations(self.trope_observations_by_film())

    def descriptive_statistics_for_films_by_trope(self):
        return self.get_statistics_for_observations(self.film_observations_by_trope())

    def get_statistics_for_observations(self, observations):
        statistics = stats.describe(observations)
        return {"nobs": statistics.nobs,
                "min": statistics.minmax[0],
                "max": statistics.minmax[1],
                "mean": statistics.mean,
                "median": numpy.median(observations),
                "q1": numpy.percentile(observations, 25),
                "q2": numpy.percentile(observations, 50),
                "q3": numpy.percentile(observations, 75),
                "variance": statistics.variance,
                "skewness": statistics.skewness,
                "kurtosis": statistics.kurtosis}

    def plot_films_histogram(self):
        x = self.trope_observations_by_film()
        return self._get_histogram_for_observations(x)

    def plot_tropes_histogram(self):
        x = self.film_observations_by_trope()
        return self._get_histogram_for_observations(x)

    def _get_histogram_for_observations(self, x):
        n, bins, patches = plt.hist(x, 'auto', density=True, facecolor='blue', alpha=0.75, histtype="stepfilled")
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
        plt.xlabel('Number of tropes')
        plt.ylabel('')
        plt.title(r'Histogram')
        plt.grid(True)
        return plt

    def plot_films_boxplot(self):
        x = self.trope_observations_by_film()
        return self._get_boplot_for_observations(x)

    def plot_tropes_boxplot(self):
        x = self.film_observations_by_trope()
        return self._get_boplot_for_observations(x)

    def _get_boplot_for_observations(self, x):
        plt.boxplot(x, vert=False)
        plt.xlabel('Number of tropes')
        plt.ylabel('')
        plt.title(r'Boxplot')
        plt.grid(True)
        return plt