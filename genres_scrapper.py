#!/usr/bin/env python3

import sys
import re
from bs4 import BeautifulSoup
import json


def parse_genres_html(file):
    try:
        soup = BeautifulSoup(open(file), 'lxml')
    except FileNotFoundError:
        print("Couldn't find your file!\nUsage: py ./genres_scrapper file")
        sys.exit(1)

    tags = soup.findAll('tr')

    # For string normalization
    regex = re.compile('[^a-z0-9]')

    genres = []
    for tag in tags:
        genre = tag.contents[2].string
        genres.append(re.sub(regex, "", genre))

    return genres


def main():
    args = sys.argv[1:]
    n_args = len(args)

    if n_args != 1:
        print('Usage: py ./genres_scrapper file')
        sys.exit(1)
    else:
        genres = parse_genres_html(args[0])
        with open('genres.json', 'w') as outfile:
            json.dump(genres, outfile)


if __name__ == '__main__':
    main()
