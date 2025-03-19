import random
import matplotlib.pyplot as plt
from fuzzywuzzy import process


# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"


def list_movies(movies):
    print(f"{len(movies)} movies in total")
    for movie, rating in movies.items():
        print(f"{movie}: {rating}")


def add_movie(movies):
    new_movie = input(f"{GREEN}Enter new movie name: {RESET}").title()
    new_rating = float(input(f"{GREEN}Enter new movie rating (0-10): {RESET}").replace(",", "."))

    while True:

        if 0 <= new_rating <= 10:
            movies[new_movie] = new_rating
            print(f"Movie {new_movie} successfully added")
            break

        else:
            print(f"{RED}Rating {new_rating} is invalid{RESET}")


def delete_movie(movies):
    movie_to_delete = input(f"{GREEN}Enter movie name to delete: {RESET}").title()

    if movie_to_delete in movies:
        del movies[movie_to_delete]
        print(f"Movie {movie_to_delete} successfully deleted")

    else:
        print(f"{RED}Movie {movie_to_delete} doesn't exist!{RESET}")


def update_movie(movies):
    movie_to_update = input(f"{GREEN}Enter movie name: {RESET}").title()

    if movie_to_update in movies:
        new_rating = float(input(f"{GREEN}Enter new movie rating (0-10): {RESET}").replace(",", "."))
        movies[movie_to_update] = new_rating
        print(f"Movie {movie_to_update} successfully updated")

    else:
        print(f"{RED}Movie {movie_to_update} doesn't exist!{RESET}")


def get_movie_stats(movies):
    sorted_values = sorted(movies.values())

    average_rating = sum(sorted_values) / len(sorted_values)
    print(f"Average rating: {round(average_rating, 2)}")

    if len(sorted_values) % 2 == 0:
        mid_index2 = len(sorted_values) // 2
        mid_index1 = (len(sorted_values) // 2) - 1
        median_rating_even_list = (sorted_values[mid_index2] + sorted_values[mid_index1]) / 2
        print(f"Median rating: {median_rating_even_list}")

    else:
        mid_index = len(sorted_values) // 2
        median_rating_odd_list = sorted_values[mid_index]
        print(f"Median rating: {median_rating_odd_list}")

    best_movie = []
    best_rating = -1
    for movie, rating in movies.items():
        if rating > best_rating:
            best_rating = rating
            best_movie = [movie]
        elif rating == best_rating:
            best_movie.append(movie)

    if len(best_movie) == 1:
        print(f"Best movie: {best_movie[0]}, {best_rating}")

    else:
        best_movie_str = ""
        for movie in best_movie:
            best_movie_str += f"{movie}, {best_rating}; "

        best_movie_str = best_movie_str.rstrip("; ")
        print(f"Best movies: {best_movie_str}")

    worst_movie = []
    worst_rating = 10
    for movie, rating in movies.items():
        if rating < worst_rating:
            worst_rating = rating
            worst_movie = [movie]

        elif rating == worst_rating:
            worst_movie.append(movie)

    if len(worst_movie) == 1:
        print(f"Worst movie: {worst_movie[0]}, {worst_rating}")

    else:
        worst_movie_str = ""
        for movie in worst_movie:
            worst_movie_str += f"{movie}, {worst_rating}; "

        worst_movie_str = worst_movie_str.rstrip("; ")
        print(f"Worst movies: {worst_movie_str}")


def get_random_movie(movies):
    convert_database_to_tuple = list(movies.items())
    random_selection = random.choice(convert_database_to_tuple)
    print(f"Your movie for tonight: {random_selection[0]}, it's rated {random_selection[1]}")


def search_movie(movies):
    search_input = input(f"{GREEN}Enter part of the movie name: {RESET}").casefold()

    # fuzzymatch module: using process.extract() to get best matches
    best_matches = process.extract(search_input, movies.keys(), limit=5)

    # manually filter matches based on score threshold
    filtered_matches = []
    for match in best_matches:
        movie, score = match
        if score >= 70:
            filtered_matches.append(match)

    # if filtered matches, print them or print "No matches found"
    if filtered_matches:
        #print(filtered_matches)
        # filtered_matches = list of tuples, each tuple
        # contains movie title and match score
        for movie, score in filtered_matches:
            print(f"{movie}: {movies[movie]}")
            # print statement with match score
            # print(f"{movie}: {database[movie]} (Match score: {score})")

    else:
        print(f"{RED}No matches found{RESET}")


def sort_movies_desc(movies):
    """this function converts movies database into list of tuples,
    each tuple holds movie title and movie rating, and then sorts
    the list of movies by movie rating in descending order."""

    list_of_movie_tuples = tuple(movies.items())

    # simple function to unpack a tuple containing movie title and rating
    # to be used in sorted() as key in order to sort movies by ratings
    def get_values(movie_tuple):
        movie_title, rating = movie_tuple
        return rating

    sorted_movie_list_desc = sorted(list_of_movie_tuples, key=get_values, reverse=True)

    for item in sorted_movie_list_desc:
        print(f"{item[0]}: {item[1]}")


# Create movie/rating bar chart
def create_rating_bar(movies):
    """this function creates a bar chart (movies on x_axis,
    rating on y-axis) using the matplotlib module"""
    movies_keys = list(movies.keys())
    movies_values = list(movies.values())

    # BAR CHART: movies on x-axis, rating on y-axis
    plt.bar(movies_keys, movies_values, color="blue", edgecolor="black")

    for key, value in movies.items():
        # used for x-position of each movie based on its index in list database_keys
        x_position = movies_keys.index(key)
        plt.text(
            x_position,
            y=0.5, s=key,
            ha="center",
            va="bottom",
            rotation=90,
            fontsize=9,
            c="white",
            weight="bold")

    # removes x-axis labels (here: movie titles) because plt.bar() does that by default
    plt.xticks([])
    plt.title("Movie Rating Chart")
    plt.xlabel("Movies")
    plt.ylabel("Rating")
    plt.show()


def print_menu():
    menu_text = """
Menu: 
1. List Movies
2. Add Movie
3. Delete Movie
4. Update Movie
5. Stats
6. Random Movie
7. Search Movie
8. Movies Sorted by Rating
9. Create Rating Histogram
"""
    blue_menu_text = f"{BLUE}{menu_text}{RESET}"
    print(blue_menu_text)


def user_menu_input(movies):
    while True:
        print_menu()
        user_input = input(f"{GREEN}Enter choice (1-8): {RESET}").strip()
        # Ignore empty input
        if not user_input:
            continue
        if user_input == "1":
            list_movies(movies)
            input("\nPress enter to continue")

        elif user_input == "2":
            add_movie(movies)
            input("\nPress enter to continue")

        elif user_input == "3":
            delete_movie(movies)
            input("\nPress enter to continue")

        elif user_input == "4":
            update_movie(movies)
            input("\nPress enter to continue")

        elif user_input == "5":
            get_movie_stats(movies)
            input("\nPress enter to continue")

        elif user_input == "6":
            get_random_movie(movies)
            input("\nPress enter to continue")

        elif user_input == "7":
            search_movie(movies)
            input("\nPress enter to continue")

        elif user_input == "8":
            sort_movies_desc(movies)
            input("\nPress enter to continue")

        elif user_input == "9":
            create_rating_bar(movies)
            input("\nPress enter to continue")

        else:
            print(f"{RED}Invalid choice{RESET}")
            continue


def main():
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }
    print(f"{BLUE}{10 * "*"} My Movies Database {10 * "*"}{RESET}")
    user_menu_input(movies)


if __name__ == "__main__":
    main()