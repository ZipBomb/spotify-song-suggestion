#!/usr/bin/env python3
"""
Module that makes use of the Spotify Web API to retrieve pseudo-random songs based
or not on a given exiting Spotify genre (look at genres.json, filled with info
scrapped from http://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity)
Spotify Ref: https://developer.spotify.com/documentation/web-api/reference-beta/#category-search
"""
import base64
import json
import random
import re
import requests
import sys
import urllib

from fuzzysearch import find_near_matches


# Client Keys
CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR CLIENT SECRET"

# Spotify API URIs
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


def get_token():
    client_token = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode('UTF-8')).decode('ascii')
    headers = {"Authorization": "Basic {}".format(client_token)}
    payload = {"grant_type": "client_credentials"}
    token_request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token


def request_valid_song(access_token, genre=None):

    # Wildcards for random search
    random_wildcards = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    wildcard = random.choice(random_wildcards)
    
    # Make a request for the Search API with pattern and random index
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    
    # Cap the max number of requests until getting RICK ASTLEYED
    song = None
    for i in range(51):
        try:
            song_request = requests.get(
                '{}/search?q={}{}&type=track&offset={}'.format(
                    SPOTIFY_API_URL,
                    wildcard,
                    "%20genre:%22{}%22".format(genre.replace(" ", "%20")),
                    random.randint(0, 200)
                ),
                headers = authorization_header
            )
            song_info = random.choice(json.loads(song_request.text)['tracks']['items'])
            artist = song_info['artists'][0]['name']
            song = song_info['name']
            break
        except IndexError:
            continue
        
    if song is None:
        artist = "Rick Astley"
        song = "Never Gonna Give You Up"
        
    return "{} - {}".format(artist, song)


def main():
    args = sys.argv[1:]
    n_args = len(args)

    # Get a Spotify API token
    access_token = get_token()
    
    # Open genres file
    try:
        with open('genres.json', 'r') as infile:
            valid_genres = json.load(infile)
    except FileNotFoundError:
        print("Couldn't find genres file!")
        sys.exit(1)

    # Parse input or pick a random genre
    if n_args == 0:
        selected_genre = random.choice(valid_genres)
    else:
        selected_genre = (" ".join(args)).lower()
    
    # Call the API for a song that matches the criteria
    if selected_genre in valid_genres:
        result = request_valid_song(access_token, genre=selected_genre)
        print(result)
    else:
        # If genre not found as it is, try fuzzy search with Levenhstein distance 2
        valid_genres_to_text = " ".join(valid_genres)
        try:
            closest_genre = find_near_matches(selected_genre, valid_genres_to_text,  max_l_dist=2)[0].matched
            result = request_valid_song(access_token, genre=closest_genre)
            print(result)
        except IndexError:
            print("Genre not found")


if __name__ == '__main__':
    main()
