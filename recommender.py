import csv
from typing import List, Set, Optional

BOOKS_CSV = 'books.csv'
MOVIES_CSV = 'imdb_top_1000.csv'


class Book:
    """
    Represents a book with relevant attributes for recommendation.
    """
    # Rekish Kunwar worked on this class
    def __init__(self, book_id: int, title: str, authors: str,
                 num_pages: Optional[int], avg_rating: Optional[float], pub_date: str):
        self.book_id = book_id
        self.title = title
        self.authors = [author.strip() for author in authors.split(',')]
        self.num_pages = num_pages
        self.avg_rating = avg_rating
        self.pub_date = pub_date

    def rating_distance(self, target_rating: Optional[float], target_pages: Optional[int]) -> float:
        """
        Compute a score based on the distance from the target rating and page count.
        Lower scores are better matches.
        """
        score = 0.0
        if target_rating is not None and self.avg_rating is not None:
            score += abs(self.avg_rating - target_rating)
        if target_pages is not None and self.num_pages is not None:
            score += abs(self.num_pages - target_pages) / 1000.0  # to normalize page difference
        return score


class Movie:
    """
    Represents a movie with relevant attributes for recommendation.
    """
    # Rekish Kunwar worked on this class too
    def __init__(self, title: str, genres: List[str], runtime: Optional[int], overview: str,
                 released_year: str, imdb_rating: Optional[float]):
        self.title = title
        self.genres = [genre.strip() for genre in genres if genre]
        self.runtime = runtime
        self.overview = overview
        self.released_year = released_year
        self.imdb_rating = imdb_rating

    def matches_preferences(self, preferred_genres: List[str], preferred_runtime: Optional[int]) -> int:
        """
        Calculate a match score based on genre overlap and closeness to runtime.
        """
        genre_score = len(set(self.genres) & set(preferred_genres))
        if genre_score == 0:
            return 0  # Only recommend if at least one genre matches
        if preferred_runtime is not None and self.runtime is not None:
            runtime_score = max(0, 15 - abs(self.runtime - preferred_runtime))
        else:
            runtime_score = 0
        return genre_score * 100 + runtime_score


def get_all_movie_genres(file_path: str) -> Set[str]:
    """
    Extract all unique genres from the movies dataset.
    """
    # Martín Ambion worked on this function, as it involves extracting genres from a movie CSV.
    genres = set()
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                genre_list = row.get('Genre', '')
                for genre in genre_list.split(','):
                    genre = genre.strip()
                    if genre:
                        genres.add(genre)
    except Exception as e:
        print(f"Error reading movie genres: {e}")
    return genres


def prompt_user_choice() -> str:
    """
    Prompt the user to choose between book, movie, or both recommendations.
    """
    # Awad Gebrewahid worked on this function as it's the initial user choice prompt.
    print("")
    print("Welcome to the Movie🍿 and Book📖 Recommender!")
    print("")
    print("What would you like to be recommended?")
    print("1. Books 📚")
    print("2. Movies 🎬")
    print("3. Both 📚 & 🎬")
    print("")
    while True:
        choice = input("Enter 1 for Books, 2 for Movies, or 3 for Both: ").strip()
        if choice in ('1', '2', '3'):
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")


def prompt_user_preferences_for_books() -> dict:
    """
    Prompt the user for their book preferences: average rating and page count.
    """
    # Bethany Cruz worked on this function, as it handles user input specific to book preferences.
    while True:
        print("")
        rating_input = input("Enter the minimum average rating you prefer (e.g., 4.17, up to 5.0, or 'none' to skip): ").strip()
        if rating_input.lower() == 'none':
            target_rating = None
            break
        try:
            target_rating = float(rating_input)
            if 0.0 <= target_rating <= 5.0:
                break
            else:
                print("Please enter a rating between 0.0 and 5.0, or 'none'.")
        except ValueError:
            print("Invalid input. Please enter a decimal number or 'none'.")

    while True:
        print("")
        pages_input = input("Enter an estimate of how many pages you want (or 'none' to skip): ").strip()
        if pages_input.lower() == 'none':
            target_pages = None
            break
        if pages_input.isdigit():
            target_pages = int(pages_input)
            break
        else:
            print("Invalid input. Please enter a number or 'none'.")

    return {
        'target_rating': target_rating,
        'target_pages': target_pages
    }



def prompt_user_preferences_for_movies(available_genres: Set[str]) -> dict:
    """
    Prompt the user for their movie preferences, showing available genres and allowing 'none' for runtime.
    """
    # Awad Gebrewahid worked on this function as it's movie-specific user preference input.
    print("")
    print("Available movie genres:")
    print(", ".join(sorted(available_genres)))
    print()
    genres = input("Enter your favorite movie genres (comma-separated, or 'none'): ").strip()
    if genres.lower() == 'none':
        selected_genres = []
    else:
        selected_genres = [g.strip() for g in genres.split(',') if g.strip()]

    print()

    runtime = input("Enter an estimate of how many minutes you want the movie to be (or 'none' to skip): ").strip()
    if runtime.lower() == 'none' or not runtime.isdigit():
        preferred_runtime = None
    else:
        preferred_runtime = int(runtime)
    return {
        'genres': selected_genres,
        'preferred_runtime': preferred_runtime
    }


def load_books_data(file_path: str) -> List[Book]:
    """
    Load books from a CSV file and return a list of Book objects.
    Skips malformed lines in the CSV.
    """
    # Rekish Kunwar worked on this function, as it processes book data into a list of `Book` objects.
    books = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                try:
                    book_id = int(row['bookID']) if row['bookID'].isdigit() else 0
                    title = row['title']
                    authors = row['authors']
                    num_pages = int(row['num_pages']) if row['num_pages'].strip().isdigit() else None
                    avg_rating = float(row['average_rating']) if row['average_rating'].replace('.', '', 1).isdigit() else None
                    pub_date = row['publication_date'] if row['publication_date'] else "Unknown"
                    books.append(Book(
                        book_id=book_id,
                        title=title,
                        authors=authors,
                        num_pages=num_pages,
                        avg_rating=avg_rating,
                        pub_date=pub_date
                    ))
                except Exception:
                    continue
    except Exception as e:
        print(f"Error loading books CSV: {e}")
    return books


def load_movies_data(file_path: str) -> List[Movie]:
    """
    Load movies from a CSV file and return a list of Movie objects.
    """
    # Martín Ambion worked on this function, as it's focused on movie data processing.
    movies = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    genres = [g.strip() for g in row.get('Genre', '').split(',') if g.strip()]
                    runtime_str = row.get('Runtime', '').strip()
                    if runtime_str.endswith('min'):
                        try:
                            runtime = int(runtime_str.split()[0])
                        except Exception:
                            runtime = None
                    else:
                        runtime = None
                    overview = row.get('Overview', '')
                    released_year = row.get('Released_Year', 'Unknown')
                    imdb_rating_str = row.get('IMDB_Rating', '')
                    try:
                        imdb_rating = float(imdb_rating_str)
                    except Exception:
                        imdb_rating = None
                    movies.append(Movie(
                        title=row.get('Series_Title', ''),
                        genres=genres,
                        runtime=runtime,
                        overview=overview,
                        released_year=released_year,
                        imdb_rating=imdb_rating
                    ))
                except Exception:
                    continue
    except Exception as e:
        print(f"Error loading movies CSV: {e}")
    return movies


def recommend_books_by_rating(books: List[Book], target_rating: Optional[float], target_pages: Optional[int], top_n: int = 5) -> List[Book]:
    """
    Recommend books whose average rating is closest to the user's input (and optionally, page count).
    """
    # Rekish Kunwar worked on this function as it handles book recommendation logic.
    scored_books = [
        (book, book.rating_distance(target_rating, target_pages))
        for book in books if book.avg_rating is not None
    ]
    scored_books.sort(key=lambda x: x[1])
    return [book for book, score in scored_books][:top_n]


def recommend_movies(movies: List[Movie], preferred_genres: List[str], preferred_runtime: Optional[int], top_n: int = 5) -> List[Movie]:
    """
    Recommend movies based on user preferences.
    """
    # Bethany Cruz worked on this function, as it focuses on movie recommendation based on genres and runtime.
    scored_movies = [
        (movie, movie.matches_preferences(preferred_genres, preferred_runtime))
        for movie in movies
    ]
    scored_movies.sort(key=lambda x: x[1], reverse=True)
    return [movie for movie, score in scored_movies if score > 0][:top_n]


def display_book_recommendations(recommendations: List[Book]):
    """
    Display the book recommendations to the user.
    """
    # Rekish Kunwar worked on this function as it displays book recommendations.
    print(f"\nTop {len(recommendations)} Book Recommendations:\n")
    for idx, book in enumerate(recommendations, 1):
        pages = f"{book.num_pages} pages" if book.num_pages is not None else "Page count unknown"
        rating = f"{book.avg_rating:.2f}" if book.avg_rating is not None else "N/A"
        pub_date = book.pub_date if book.pub_date else "Unknown"
        authors = "/".join(book.authors) if book.authors else "Unknown"

        print(f"{idx}. {book.title} ({pages})")
        print(f"  Authors: {authors}")
        print(f"  Rating: {rating}")
        print(f"  Published: {pub_date}")
        print("")


def display_movie_recommendations(recommendations: List[Movie]):
    """
    Display the movie recommendations to the user.
    """
    # Awad Gebrewahid worked on this function, as it displays movie recommendations.
    print(f"\nTop {len(recommendations)} Movie Recommendations:\n")
    for idx, movie in enumerate(recommendations, 1):
        title = movie.title
        released_year = movie.released_year
        genres_display = ', '.join(movie.genres)
        imdb_display = f"IMDb: {movie.imdb_rating:.1f}" if movie.imdb_rating is not None else "IMDb: N/A"
        runtime_display = f"{movie.runtime} min" if movie.runtime is not None else "Runtime: Unknown"
        overview = movie.overview if movie.overview else "Overview not available."
        print(f"{title} ({released_year})")
        print(f"Genres: {genres_display}")
        print(f"{imdb_display}")
        print(f"Runtime: {runtime_display}")
        print(f"Overview: {overview}\n")


def main():
    """
    Main function to run the recommender system.
    """
    # Rekish Kunwar worked on this function as it's the overall flow controller.
    choice = prompt_user_choice()

    if choice == '1':
        user_prefs_books = prompt_user_preferences_for_books()
        books = load_books_data(BOOKS_CSV)
        recommendations_books = recommend_books_by_rating(
            books,
            user_prefs_books['target_rating'],
            user_prefs_books['target_pages']
        )
        display_book_recommendations(recommendations_books)

    elif choice == '2':
        available_genres = get_all_movie_genres(MOVIES_CSV)
        user_prefs_movies = prompt_user_preferences_for_movies(available_genres)
        movies = load_movies_data(MOVIES_CSV)
        recommendations_movies = recommend_movies(
            movies,
            user_prefs_movies['genres'],
            user_prefs_movies['preferred_runtime']
        )
        display_movie_recommendations(recommendations_movies)

    elif choice == '3':
        user_prefs_books = prompt_user_preferences_for_books()
        books = load_books_data(BOOKS_CSV)
        recommendations_books = recommend_books_by_rating(
            books,
            user_prefs_books['target_rating'],
            user_prefs_books['target_pages']
        )
        display_book_recommendations(recommendations_books)

        available_genres = get_all_movie_genres(MOVIES_CSV)
        user_prefs_movies = prompt_user_preferences_for_movies(available_genres)
        movies = load_movies_data(MOVIES_CSV)
        recommendations_movies = recommend_movies(
            movies,
            user_prefs_movies['genres'],
            user_prefs_movies['preferred_runtime']
        )
        display_movie_recommendations(recommendations_movies)


if __name__ == "__main__":
    main()