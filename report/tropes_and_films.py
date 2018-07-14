import json
import os
import warnings
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

    def fisk_parameters_for_tropes_by_films(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            observations = self.trope_observations_by_film()
            return list(stats.fisk.fit(observations))

    def foldcauchy_parameters_for_films_by_tropes(self):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            observations = self.film_observations_by_trope()
            return list(stats.foldcauchy.fit(observations))

    def plot_films_histogram(self):
        observations = self.trope_observations_by_film()
        plot = self._get_histogram_for_observations(observations, "Number of tropes", dark=True)
        return plot

    def plot_films_histogram_and_line(self):
        observations = self.trope_observations_by_film()
        plot = self._get_histogram_for_observations(observations, "Number of tropes", dark=False)
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            x = numpy.linspace(0, max(observations), 200)
            params = stats.fisk.fit(observations)
            pyplot.plot(x, stats.fisk.pdf(x, *list(params)), 'k-', alpha=0.7, lw=1, label='fisk pdf')
        pyplot.title("Estimated log-logistic distribution density "+str(params))
        return plot

    def plot_tropes_histogram(self):
        observations = self.film_observations_by_trope()
        plot = self._get_histogram_for_observations(observations, "Number of films", dark=True)
        return plot

    def plot_tropes_histogram_and_line(self):
        observations = self.film_observations_by_trope()
        plot = self._get_histogram_for_observations(observations, "Number of films", dark=False)

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            x = numpy.linspace(0, max(observations), 200)
            params = stats.foldcauchy.fit(observations)
            pyplot.plot(x, stats.foldcauchy.pdf(x, *list(params)), 'k-', alpha=0.7, lw=1, label='foldcauchy pdf')
        pyplot.title("Estimated folded Cauchy distribution density "+str(params))
        return plot

    @staticmethod
    def _get_histogram_for_observations(observations, x_label, dark = True):
        color = "blue" if dark else "aqua"
        pyplot.hist(observations, 'auto', density=True, facecolor=color, alpha=0.75, histtype="stepfilled")
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

    def get_best_distribution_of_films(self):
        data = self.trope_observations_by_film()
        return self._get_best_distribution(data)

    def get_best_distribution_of_tropes(self):
        data = self.film_observations_by_trope()
        return self._get_best_distribution(data)

    def _get_best_distribution(self, data, bins=200):

        """Model data by finding best fit distribution to data"""
        # Get histogram of original data
        y, x = numpy.histogram(data, bins=bins, density=True)
        x = (x + numpy.roll(x, -1))[:-1] / 2.0

        # Distributions to check
        DISTRIBUTIONS = [
            stats.alpha, stats.anglit, stats.arcsine, stats.beta, stats.betaprime, stats.bradford, stats.burr,
            stats.cauchy, stats.chi, stats.chi2, stats.cosine, stats.dgamma, stats.dweibull, stats.erlang,
            stats.expon,
            stats.exponnorm, stats.exponweib, stats.exponpow, stats.f, stats.fatiguelife, stats.fisk,
            stats.foldcauchy,
            stats.foldnorm, stats.frechet_r, stats.frechet_l, stats.genlogistic, stats.genpareto, stats.gennorm,
            stats.genexpon, stats.genextreme, stats.gausshyper, stats.gamma, stats.gengamma, stats.genhalflogistic,
            stats.gilbrat, stats.gompertz, stats.gumbel_r, stats.gumbel_l, stats.halfcauchy, stats.halflogistic,
            stats.halfnorm, stats.halfgennorm, stats.hypsecant, stats.invgamma, stats.invgauss, stats.invweibull,
            stats.johnsonsb, stats.johnsonsu, stats.ksone, stats.kstwobign, stats.laplace, stats.levy, stats.levy_l,
            stats.levy_stable, stats.logistic, stats.loggamma, stats.loglaplace, stats.lognorm, stats.lomax,
            stats.maxwell, stats.mielke, stats.nakagami, stats.ncx2, stats.ncf, stats.nct, stats.norm, stats.pareto,
            stats.pearson3, stats.powerlaw, stats.powerlognorm, stats.powernorm, stats.rdist, stats.reciprocal,
            stats.rayleigh, stats.rice, stats.recipinvgauss, stats.semicircular, stats.t, stats.triang,
            stats.truncexpon, stats.truncnorm, stats.tukeylambda, stats.uniform, stats.vonmises,
            stats.vonmises_line,
            stats.wald, stats.weibull_min, stats.weibull_max, stats.wrapcauchy
        ]

        # Best holders
        best_distribution = stats.norm
        best_params = (0.0, 1.0)
        best_sse = numpy.inf

        # Estimate distribution parameters from data
        for distribution in DISTRIBUTIONS:

            # Try to fit the distribution
            try:
                # Ignore warnings from data that can't be fit
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore')

                    # fit dist to data
                    params = distribution.fit(data)

                    # Separate parts of parameters
                    arg = params[:-2]
                    loc = params[-2]
                    scale = params[-1]

                    # Calculate fitted PDF and error with fit in distribution
                    pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                    sse = numpy.sum(numpy.power(y - pdf, 2.0))

                    # identify if this distribution is better
                    if best_sse > sse > 0:
                        best_distribution = distribution
                        best_params = params
                        best_sse = sse

            except Exception:
                pass

        return (best_distribution.name, best_params)
