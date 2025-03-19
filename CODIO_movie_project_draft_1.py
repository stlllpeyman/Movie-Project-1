"""
CODE (this was a first draft!) WITH EXTENSIVE COMMENTS
FOR MY OWN UNDERSTANDING SINCE THERE WERE A FEW NEW THINGS
HAPPENING HERE SUCH AS THE USE OF FUZZYWUZZY.
"""

import random
import matplotlib.pyplot as plt
from fuzzywuzzy import process


# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"

def list_movies(database):
    print(f"{len(database)} movies in total")
    for movie, rating in database.items():
        print(f"{movie}: {rating}")


def add_movie(database):
    new_movie = input(f"{GREEN}Enter new movie name: {RESET}").title()

    while True:
        user_input = input(f"{GREEN}Enter new movie rating (0-10): {RESET}").replace(",", ".")
        movie_rating = float(user_input)

        if 0 <= movie_rating <= 10:
            database[new_movie] = movie_rating
            print(f"Movie {new_movie} successfully added")
            break

        else:
            print(f"{RED}Rating {movie_rating} is invalid{RESET}")


def delete_movie(database):
    movie_to_delete = input(f"{GREEN}Enter movie name to delete: {RESET}").title()

    if movie_to_delete not in database:
        print(f"{RED}Movie {movie_to_delete} doesn't exist!{RESET}")

    else:
        del database[movie_to_delete]
        print(f"Movie {movie_to_delete} successfully deleted")


def update_movie(database):
    movie_to_update = input(f"{GREEN}Enter movie name: {RESET}").title()
    if movie_to_update not in database:
        print(f"{RED}Movie {movie_to_update} doesn't exist!{RESET}")

    else:
        user_input = input(f"{GREEN}Enter new movie rating (0-10): {RESET}").replace(",", ".")
        new_rating =float(user_input)
        database[movie_to_update] = new_rating
        print(f"Movie {movie_to_update} successfully updated")


def get_movie_stats(database):
    sorted_values = sorted(database.values())

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
    for movie, rating in database.items():
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
    for movie, rating in database.items():
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


def get_random_movie(database):
    convert_database_to_tuple = list(database.items())
    random_movie = random.choice(convert_database_to_tuple)
    print(f"Your movie for tonight: {random_movie[0]}, it's rated {random_movie[1]}")


def search_movie(database):
    #print(database)
    search_input = input(f"{GREEN}Enter part of the movie name: {RESET}").casefold()

    # simple search without fuzzymatch:
    # for movie, rating in movies.items():
    #     if search_input in movie.casefold():
    #         print(f"{movie}, {rating}")

    # fuzzymatch module: using process.extract() to get best matches in list or dict
    # returns a list of tuples containing each match and its score
    best_matches = process.extract(search_input, database.keys(), limit=5)
    print(best_matches)
    print(type(best_matches))

    # manually filter matches based on score threshold
    filtered_matches = []
    for match in best_matches:
        movie, score = match
        # only include matches with a score of 70 or higher
        if score >= 60:
            filtered_matches.append(match)

    # if there are filtered matches, print them or print "No matches..."
    if filtered_matches:
        """best_matches/filtered_matches is a list of tuples, each tuple
        contains movie title and match score so both variables
        (movie title, match score) have to be in the for loop otherwise you
        cannot access the movie title separately (however, you could use
        a placeholder '_' if you don't want/need the score."""
        for movie, score in filtered_matches:
            print(f"{movie}: {database[movie]}")
            # print statement with match score
            #print(f"{movie}: {database[movie]} (Match score: {score})")

    else:
        print(f"{RED}No matches found{RESET}")


def sort_movies_desc(database):
    # convert the database into list of tuples, each tuple holds movie title + rating
    dict_convert_tuples_list = tuple(database.items())

    # simple function to return value of a tuple at index 1
    def get_values(item):
        return item[1]

    """using sorted() on list of tuples, passing get_values function to it as key
    that way list will be sorted by the values, reverse=True means in descending order"""
    sorted_movie_list_desc = sorted(dict_convert_tuples_list, key=get_values, reverse=True)

    for item in sorted_movie_list_desc:
        print(f"{item[0]}: {item[1]}")


# Create movie/rating bar chart
def create_rating_bar(database):
    database_keys = list(database.keys())
    database_values = list(database.values())
    ###BAR CHART: movies on x-axis, rating on y-axis
    plt.bar(database_keys, database_values, color="blue", edgecolor="black")

    for key, value in database.items():
        # used for x-position of each movie based on its index in list database_keys
        x_position = database_keys.index(key)
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
    while True:
        print(f"{BLUE}{10 * "*"} My Movies Database {10 * "*"}{RESET}")
        print(
            f"{BLUE}\nMenu: \n1. List Movies\n2. Add Movie\n3. Delete Movie\n4. Update Movie\n5. Stats\n6. Random Movie\n7. Search Movie\n8. Movies Sorted by Rating\n9. Create Rating Histogram\n{RESET}"
        )
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


if __name__ == "__main__":
    main()
