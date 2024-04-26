import movie_storage
import requests
import random

# API URL with your API key
api_key = '188c2dda'
OMDB_API_URL = f'http://www.omdbapi.com/?apikey={api_key}'


def display_menu():
    """Display the menu options."""
    print("\nMenu:")
    print("0. Exit")
    print("1. List Movies")
    print("2. Add Movie")
    print("3. Delete Movie")
    print("4. Update Movie")
    print("5. Statistics")
    print("6. Random Movie")
    print("7. Search Movie")
    print("8. Movies Sorted by Rating (Descending)")
    print("9. Generate Website")


def list_movies():
    """List all movies from the database."""
    movies = movie_storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    print(f"{len(movies)} movies in total")
    for title, info in movies.items():
        print(
            f"{title}: Rating - {info['rating']}, Year of Release - {info['year']}, Poster URL - {info['poster_url']}")


def add_movie():
    """Add a new movie to the database using OMDb API."""
    title = input("Please write the name of the movie: ")

    # Make request to OMDb API
    try:
        response = requests.get(f"{OMDB_API_URL}&t={title}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        movie_data = response.json()

        # Check if movie data is found
        if movie_data.get('Response') == 'True':
            # Extract necessary information
            year = movie_data.get('Year')
            rating = movie_data.get('imdbRating')
            if rating != 'N/A':
                rating = float(rating)
            else:
                rating = None  # Set rating to None if it's not available

            poster_url = movie_data.get('Poster')

            # Save data to the database
            movie_storage.add_movie(title, year, rating, poster_url)
            print(f"Movie '{title}' successfully added")
        else:
            print(f"Movie '{title}' not found in the database.")
    except requests.RequestException as e:
        print("Error accessing the OMDb API:", e)
        print("Please check your internet connection and try again.")


def delete_movie():
    """Delete a movie from the database."""
    title = input("Please write the name of the movie you want to delete: ")
    movie_storage.delete_movie(title)


def update_movie():
    """Update the rating of an existing movie in the database."""
    title = input("Please write the name of the movie you want to update: ")
    rating = float(input("Please enter the new rating for the movie: "))
    movie_storage.update_movie(title, rating)


def statistics():
    """Display statistics about the movies."""
    movies = movie_storage.list_movies()
    total_movies = len(movies)
    if total_movies == 0:
        print("No movies in the database.")
        return

    total_ratings = sum(info['rating'] for info in movies.values() if info['rating'] is not None)
    average_rating = total_ratings / total_movies

    print(f"Total number of movies: {total_movies}")
    print(f"Average rating of movies: {average_rating:.2f}")


def random_movie():
    """Display a random movie from the database."""
    movies = movie_storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return

    random_title = random.choice(list(movies.keys()))
    print(f"Random movie: {random_title}")


def search_movie():
    """Search for a movie by title."""
    title = input("Please enter the title of the movie: ")
    movies = movie_storage.list_movies()
    if title in movies:
        info = movies[title]
        print(
            f"{title}: Rating - {info['rating']}, Year of Release - {info['year']}, Poster URL - {info['poster_url']}")
    else:
        print(f"Movie '{title}' not found in the database.")


def movies_sorted_by_rating():
    """Display movies sorted by rating in descending order."""
    movies = movie_storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'] if x[1]['rating'] is not None else 0, reverse=True)
    for title, info in sorted_movies:
        print(
            f"{title}: Rating - {info['rating']}, Year of Release - {info['year']}, Poster URL - {info['poster_url']}")


def generate_website():
    """Generate the website according to the template."""
    with open("index_template.html", "r") as template_file:
        template = template_file.read()

    # Generate movie grid HTML
    movie_grid_html = ""
    movies = movie_storage.list_movies()
    for title, info in movies.items():
        movie_grid_html += f"<li class='movie'><img src='{info['poster_url']}' alt='{title}' class='movie-poster'><div class='movie-title'>{title}</div><div class='movie-year'>{info['year']}</div></li>"

    # Replace placeholder with movie grid HTML
    template = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # Save the generated HTML to index.html
    with open("index.html", "w") as output_file:
        output_file.write(template)

    print("Website was generated successfully.")


def main():
    """Main function to run the movie database application."""
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '0':
            print("Bye!")
            break  # Exit the loop and end the program
        elif choice == '1':
            list_movies()
        elif choice == '2':
            add_movie()
        elif choice == '3':
            delete_movie()
        elif choice == '4':
            update_movie()
        elif choice == '5':
            statistics()
        elif choice == '6':
            random_movie()
        elif choice == '7':
            search_movie()
        elif choice == '8':
            movies_sorted_by_rating()
        elif choice == '9':
            generate_website()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
