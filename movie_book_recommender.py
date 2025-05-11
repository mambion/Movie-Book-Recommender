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
    def user_preferences():
        """this function introduces what is going to happen next, collects what books and movie genres the user has, and 
        returns it as a dictionary"""
        print("Welcome! This recommendation algorithm finds books and movies for you based on what you like!\nAnswer the next few questions so we can learn what you like :)\n) 
        
        """asking all the user questions"""
        #asking for movie genres 
        movie_genres_input = input("What are your favorite movie genres? (Separate them with commas please): ")
        movie_genres = movie_genres_input.lower().split(",")
        #asking for book genres
        book_genres_input = input("What are your favorite book genres? (Separate them with commas please): ")
        book_genres = book_genres_input.lower().split(",")
        #asking for actors (but it's optional just in case they can't think of anyone)
        actors_input = input("Do you have any favorite movie actors? Be sure to spell their name right! (Optional – press Enter to skip, Separate them with commas please): ")
        if actors_input:
            actors = actors_input.lower().split(",")
        else:
            authors = []
        #asking for favorite authors (also optional)
        authors_input = input("Do you have any favorite book authors? Be sure to spell their name right! (Optional – press Enter to skip, Separate them with commas please): ")
        if authors_input:
            authors = authors_input.lower().split(",") 
        else:
            authors = []
            
        """cleaning up the given data"""    
        #makes sure theres no extra spaces in the lists
        for genre in movie_genres:
            if genre.strip():
                movie_genres = genre.strip() 
        for genre in book_genres:
            if genre.strip():
                book_genres = genre.strip() 
        for actor in actors:
            if actor.strip():
                actors = actor.strip()
        for author in authors:
            if author.strip():
                authors = author.strip() 
        #puts the answers in dictionary
        preferences = {'movie_genres': movie_genres, 'book_genres': book_genres, 'actors': actors, 'authors': authors} 
        return preferences
        
    def display_recommendations(movies, books):
    """displays the movie and book recommendations with their titles genres and actors/ authors"""
    #printing the movie recommendations
    print("\nRecommended Movies:")
    if movies.empty:
        print("Sorry, we couldn't find any matching movies :(")
    else:
        for row in movies[["title", "genre", "actor"]].values:
            title = row[0]
            genre = row[1]
            actor = row[2]
            print(" - " + title + " (" + genre + "), featuring: " + actor)
    #printing the book recommendations
    print("\nRecommended Books:")
    if books.empty:
        print("Sorry, we couldn't find any matching books :(")
    else:
        for row in books[["title", "genre"]].values:
            title = row[0]
            genre = row[1]
            author = row[2]
            print(" - " + title + " by " + author + " (" + genre + ")")


























    
