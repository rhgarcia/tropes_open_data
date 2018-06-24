import json
import os
from collections import OrderedDict

import matplotlib
import numpy
from matplotlib import pyplot
from scipy import stats


class TropesAndFilms(object):
    FILE_PATH = '../data/all_films_and_their_tropes.json'

    NUMBER_OF_OBSERVATIONS_KEY = "nobs"
    MINIMUM_KEY = "min"
    MAXIMUM_KEY = "max"
    MEAN_KEY = "mean"
    MEDIAN_KEY = "median"
    FIRST_QUARTILE_KEY = "q1"
    SECOND_QUARTILE_KEY = "q2"
    THIRD_QUARTILE_KEY = "q3"
    VARIANCE_KEY = "variance"
    SKEWNESS_KEY = "skewness"
    KURTOSIS_KEY = "kurtosis"

    def __init__(self):
        self._load_data()

    def _load_data(self):
        self._init_film_dictionary()
        self._init_trope_dictionary()
        self._init_sorted_keys()
        self._init_matplot_library()

    def _init_film_dictionary(self):
        data_file_path = self._get_data_file_path()
        with open(data_file_path, 'r') as file:
            self.film_dictionary = json.load(file)

    def _get_data_file_path(self):
        script_dir = os.path.dirname(__file__)
        data_file_path = os.path.join(script_dir, self.FILE_PATH)
        return data_file_path

    def _init_trope_dictionary(self):
        self.trope_dictionary = {}
        for film in self.film_dictionary.keys():
            trope_list = self.film_dictionary[film]
            for trope in trope_list:
                if trope not in self.trope_dictionary:
                    self.trope_dictionary[trope] = []
                self.trope_dictionary[trope].append(film)

    def _init_sorted_keys(self):
        self.tropes_sorted_by_occurrences = sorted(self.trope_dictionary.keys(), reverse=True,
                                                   key=lambda element: len(self.trope_dictionary[element]))
        self.film_sorted_by_occurrences = sorted(self.film_dictionary.keys(), reverse=True,
                                                 key=lambda element: len(self.film_dictionary[element]))

    @staticmethod
    def _init_matplot_library():
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
        return {self.NUMBER_OF_OBSERVATIONS_KEY: statistics.nobs,
                self.MINIMUM_KEY: statistics.minmax[0],
                self.MAXIMUM_KEY: statistics.minmax[1],
                self.MEAN_KEY: statistics.mean,
                self.MEDIAN_KEY: numpy.median(observations),
                self.FIRST_QUARTILE_KEY: numpy.percentile(observations, 25),
                self.SECOND_QUARTILE_KEY: numpy.percentile(observations, 50),
                self.THIRD_QUARTILE_KEY: numpy.percentile(observations, 75),
                self.VARIANCE_KEY: statistics.variance,
                self.SKEWNESS_KEY: statistics.skewness,
                self.KURTOSIS_KEY: statistics.kurtosis}

    def plot_films_histogram(self):
        observations = self.trope_observations_by_film()
        return self._get_histogram_for_observations(observations, "Number of tropes")

    def plot_tropes_histogram(self):
        observations = self.film_observations_by_trope()
        return self._get_histogram_for_observations(observations, "Number of films")

    @staticmethod
    def _get_histogram_for_observations(observations, x_label):
        pyplot.hist(observations, 'auto', density=True, facecolor='blue', alpha=0.75, histtype="stepfilled")
        pyplot.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.4)
        pyplot.xlabel(x_label)
        pyplot.ylabel('')
        pyplot.title(r'Histogram')
        pyplot.grid(True)
        return pyplot

    def plot_films_boxplot(self):
        x = self.trope_observations_by_film()
        return self._get_boxplot_for_observations(x, "Number of tropes")

    def plot_tropes_boxplot(self):
        x = self.film_observations_by_trope()
        return self._get_boxplot_for_observations(x, "Number of films")

    @staticmethod
    def _get_boxplot_for_observations(observations, x_label):
        pyplot.boxplot(observations, vert=False)
        pyplot.xlabel(x_label)
        pyplot.ylabel('')
        pyplot.title(r'Boxplot')
        pyplot.grid(True)
        return pyplot
