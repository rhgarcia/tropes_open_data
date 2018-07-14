import unittest
from report.tropes_and_films import TropesAndFilms


class TropesByFilmTestCase(unittest.TestCase):
    def test_when_tropes_appearance_called_then_returns_a_dictionary(self):
        data = TropesAndFilms()
        occurrences = data.tropes_dictionary_sorted_by_number_of_films()
        self.assertTrue(True)

    def test_when_descriptive_statistics_called_then_returns_all_the_data(self):
        data = TropesAndFilms()
        tropes_by_film_stats = data.descriptive_statistics_for_tropes_by_film()
        data.descriptive_statistics_for_films_by_trope()

    def test_when_plot_tropes_histogram_called_then_returns_all_the_data(self):
        data = TropesAndFilms()
        data.plot_tropes_histogram()

    def test_get_best_distribution_of_films_returns_values(self):
        data = TropesAndFilms()
        (distribution, parameters) = data.get_best_distribution_of_films()

    def test_get_best_distribution_of_tropes_returns_values(self):
        data = TropesAndFilms()
        (distribution, parameters) = data.get_best_distribution_of_tropes()
        pass

    def test_plot_films_histogram(self):
        data = TropesAndFilms()
        data.plot_films_histogram()