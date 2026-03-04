# name: Kaitlyn Staut
# date: 3-3-2026
# description: CS 178 lab 10 - Section 5

import boto3
from boto3.dynamodb.conditions import Attr

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Songs')

"""CREATE NEW SONG"""
def create_song():
    title = input("Enter song title: ").strip()

    response = table.scan(
        FilterExpression=Attr("Title").eq(title)
    )
    items = response.get("Items", [])

    if items:
        print(f"A song with that title already exists.")
        return

    table.put_item(
        Item={
            "Title": title,
        }
    )
    print("song created")


"""DISPLAY ALL MOVIES"""
def print_song(song):
    title = song.get("Title", "Unknown Title")
    artist = song.get("Artist", "Unknown Artist")
    year = song.get("Year", "Unkown Year")
    duration = song.get("Duration", "Unkown Duration")

    print(f"  Title  : {title}")
    print(f"  Artist   : {artist}")
    print(f"  Year: {year}")
    print(f"  Duration: {duration}")
    print()


def print_all_songs():
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No songs found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} song(s):\n")
    for song in items:
        print_song(song)


"""UPDATE RATING"""
def update_duration():
    title = input("What is the song title? ").strip()

    response = table.get_item(Key={"Title": title})
    song = response.get("Item")

    if not song:
        print("This song does not exist.")
        return

    new_duration = input("What is the song's new duration? ").strip()

    try:
        new_duration = int(new_duration)
    except ValueError:
        print("Duration must be an integer. Update canceled.")
        return

    table.update_item(
        Key={"Title": title},
        UpdateExpression="SET #dur = :d",
        ExpressionAttributeNames={"#dur": "Duration"},
        ExpressionAttributeValues={":d": new_duration}
    )

    print("movie ratings updated")


"""DELETE MOVIE"""
def delete_song():
    title = input("Enter song title: ").strip()

    response = table.scan(
        FilterExpression=Attr("Title").eq(title)
    )
    items = response.get("Items", [])

    if not items:
        print(f"This song already does not exist.")
        return

    table.delete_item(
        Key={"Title": title}
    )
    print("song deleted")

"""QUERY MOVIE"""
def query_movie():
    artist = input("Enter artist name: ").strip()

    response = table.scan(
        FilterExpression="Artist = :a",
        ExpressionAttributeValues={":a": artist}
    )

    items = response.get("Items", [])

    if not items:
        print(f"No songs found for artist '{artist}'.")
        return

    print(f"\nSongs by {artist}:")
    for song in items:
        print(f"- {song['Title']} ({song.get('Year', 'Unknown')})")


def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new song")
    print("Press R: to READ all songs")
    print("Press U: to UPDATE a song (update duration)")
    print("Press D: to DELETE a song")
    print("Press Q: to QUERY a song's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_song()
        elif input_char.upper() == "R":
            print_all_songs()
        elif input_char.upper() == "U":
            update_duration()
        elif input_char.upper() == "D":
            delete_song()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
