#!/usr/bin/env python3
"""
Module that makes use of the Spotify Web API to retrieve pseudo-random songs based
or not on a given exiting Spotify genre (look at genres.json, filled with info
scrapped from http://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity)
Spotify Ref: https://developer.spotify.com/documentation/web-api/reference-beta/#category-search
"""

import sys
import json
import re
import requests
import base64
import urllib
import random

# Client Keys
CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR CLIENT SECRET"

# Spotify API URIs
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


def get_token():
    client_token = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET)
                                    .encode('UTF-8')).decode('ascii')

    headers = {"Authorization": "Basic {}".format(client_token)}
    payload = {
        "grant_type": "client_credentials"
    }
    token_request = requests.post(
        SPOTIFY_TOKEN_URL, data=payload, headers=headers)
    access_token = json.loads(token_request.text)["access_token"]
    return access_token


def request_valid_song(access_token, genre=None):
    # Wildcards for random search
    randomSongsArray = ['%25a%25', 'a%25', '%25a',
                        '%25e%25', 'e%25', '%25e',
                        '%25i%25', 'i%25', '%25i',
                        '%25o%25', 'o%25', '%25o',
                        '%25u%25', 'u%25', '%25u']
    randomSongs = random.choice(randomSongsArray)
    # Genre filter definition
    if genre:
        genreSearchString = " genre:'{}'".format(genre)
    else:
        genreSearchString = ""
    # Upper limit for random search
    maxLimit = 10000
    while True:
        try:
            randomOffset = random.randint(1, maxLimit)
            authorization_header = {
                "Authorization": "Bearer {}".format(access_token)
            }
            song_request = requests.get(
                "{}/search?query={}&offset={}&limit=1&type=track".format(
                    SPOTIFY_API_URL,
                    randomSongs + genreSearchString,
                    randomOffset
                ),
                headers=authorization_header
            )
            song_info = json.loads(song_request.text)['tracks']['items'][0]
            artist = song_info['artists'][0]['name']
            song = song_info['name']
        except IndexError:
            if maxLimit > 1000:
                maxLimit = maxLimit - 1000
            elif maxLimit <= 1000 and maxLimit > 0:
                maxLimit = maxLimit - 10
            else:
                artist = "Rick Astley"
                song = "Never gonna give you up"
                break
            continue
        break
    return "{} - {}".format(artist, song)


def main():
    args = sys.argv[1:]
    n_args = len(args)

    if n_args > 1:
        print('usage: py ./random_song.py [genre]')
        sys.exit(1)
    else:
        access_token = get_token()
        if n_args == 0:
            result = request_valid_song(access_token)
        else:
            selected_genre = (re.sub('[^a-zA-Z0-9]', '', args[0])).lower()
            try:
                with open('genres.json', 'r') as infile:
                    valid_genres = json.load(infile)
            except FileNotFoundError:
                print("Couldn't find genres file!")
                sys.exit(1)

            if selected_genre in valid_genres:
                result = request_valid_song(access_token, genre=selected_genre)
            else:
                result = request_valid_song(access_token)

        print(result)


if __name__ == '__main__':
    main()
