#Movie Book Recommendation System

import pandas as pd
import numpy as np
class MovieBookRecommender:
    def __init__(self, movie_data, book_data):
        self.movie_data = movie_data
        self.book_data = book_data

    def recommend_movies(self, user_preferences):
        # Simple recommendation logic based on user preferences
        recommended_movies = self.movie_data[self.movie_data['genre'].isin(user_preferences['movie_genres'])]
        return recommended_movies

    def recommend_books(self, user_preferences):
        # Simple recommendation logic based on user preferences
        recommended_books = self.book_data[self.book_data['genre'].isin(user_preferences['book_genres'])]
        return recommended_books
# Example usage
if __name__ == "__main__":
    # Sample movie and book data
    movie_data = pd.DataFrame({
        'title': ['Inception', 'The Matrix', 'Interstellar'],
        'genre': ['Sci-Fi', 'Action', 'Sci-Fi']
    })

    book_data = pd.DataFrame({
        'title': ['Dune', 'Neuromancer', 'Foundation'],
        'genre': ['Sci-Fi', 'Sci-Fi', 'Sci-Fi']
    })

    recommender = MovieBookRecommender(movie_data, book_data)

    user_preferences = {
        'movie_genres': ['Sci-Fi'],
        'book_genres': ['Sci-Fi']
    }

    recommended_movies = recommender.recommend_movies(user_preferences)
    recommended_books = recommender.recommend_books(user_preferences)

    print("Recommended Movies:")
    print(recommended_movies)

    print("\nRecommended Books:")
    print(recommended_books)

# This code defines a simple movie and book recommendation system based on user preferences.
# It uses pandas to handle data and provides a basic structure for recommending movies and books.



























    
