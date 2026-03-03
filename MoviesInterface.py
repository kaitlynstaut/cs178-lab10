# name: Kaitlyn Staut
# date: 3-3-2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5)

import boto3
from boto3.dynamodb.conditions import Attr

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')


"""CREATE NEW MOVIE"""
def create_movie():
    title = input("Enter movie title: ").strip()

    response = table.scan(
        FilterExpression=Attr("Title").eq(title)
    )
    items = response.get("Items", [])

    if items:
        print(f"A movie with that title already exists.")
        return

    table.put_item(
        Item={
            "Title": title,
            "Ratings": []
        }
    )
    print("creating a movie")


"""DISPLAY ALL MOVIES"""
def print_movie(movie):
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    ratings = movie.get("Ratings", "No ratings")
    runtime = movie.get("Runtime", "Unkown runtime")

    print(f"  Title  : {title}")
    print(f"  Year   : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Runtimes: {runtime}")
    print()


def print_all_movies():
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

    print("printing all movies")


"""UPDATE RATING"""
def update_rating():
    """
    Prompt user for a Movie Title.
    Prompt user for a rating (integer).
    Append the rating to the movie's Ratings list in the database.
    """
    print("updating rating")

"""DELETE MOVIE"""
def delete_movie():
    """
    Prompt user for a Movie Title.
    Delete that item from the database.
    """
    print("deleting movie")

"""QUERY MOVIE"""
def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    print("query movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
