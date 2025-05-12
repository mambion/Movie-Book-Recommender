import unittest
from recommender import Book, Movie, recommend_books_by_rating, recommend_movies

class TestBook(unittest.TestCase):
    def test_rating_distance(self):
        book = Book(1, "Test Book", "Author A", 200, 4.2, "2020-01-01")
        # Should be 0.2 + 0.05 = 0.25
        self.assertAlmostEqual(book.rating_distance(4.0, 150), 0.2 + 0.05)

class TestMovie(unittest.TestCase):
    def test_matches_preferences_genre_and_runtime(self):
        movie = Movie("Test Movie", ["Action", "Thriller"], 120, "Overview", "2022", 8.0)
        # genre_score = 1, runtime_score = 15
        self.assertEqual(movie.matches_preferences(["Action"], 120), 100 + 15)
        # No genre match, should return 0
        self.assertEqual(movie.matches_preferences(["Comedy"], 120), 0)

class TestRecommendFunctions(unittest.TestCase):
    def test_recommend_books_by_rating(self):
        books = [
            Book(1, "A", "X", 100, 4.0, "2000"),
            Book(2, "B", "Y", 200, 4.5, "2001"),
        ]
        recs = recommend_books_by_rating(books, 4.1, None, top_n=1)
        self.assertEqual(recs[0].title, "A")

    def test_recommend_movies(self):
        movies = [
            Movie("M1", ["Action"], 120, "O1", "2020", 8.0),
            Movie("M2", ["Comedy"], 90, "O2", "2019", 7.0),
        ]
        recs = recommend_movies(movies, ["Action"], 120, top_n=1)
        self.assertEqual(recs[0].title, "M1")
        recs_none = recommend_movies(movies, ["Sci-Fi"], 100, top_n=1)
        self.assertEqual(len(recs_none), 0)

if __name__ == '__main__':
    unittest.main()
