import json

# Define the filename for the JSON file
FILENAME = "data.json"


def load_data():
    """Load data from the JSON file."""
    try:
        with open(FILENAME, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data


def save_data(data):
    """Save data to the JSON file."""
    with open(FILENAME, 'w') as file:
        json.dump(data, file)


def list_movies():
    """List all movies from the database."""
    data = load_data()
    return data


def add_movie(title, year, rating, poster_url):
    """Add a movie to the database."""
    data = load_data()
    if title in data:
        print(f"Movie {title} already exists!")
        return
    data[title] = {"year": year, "rating": rating,
                   "poster_url": poster_url}  # Add poster URL
    save_data(data)
    print(f"Movie {title} successfully added")


def delete_movie(title):
    """Delete a movie from the database."""
    data = load_data()
    if title not in data:
        print(f"Movie {title} does not exist!")
        return
    del data[title]
    save_data(data)
    print(f"Movie {title} successfully deleted")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    data = load_data()
    if title not in data:
        print(f"Movie {title} does not exist!")
        return
    data[title]["rating"] = rating
    save_data(data)
    print(f"Rating of movie {title} successfully updated to {rating}")
