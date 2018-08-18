# Spotify Song Suggestion

Package with tools originally made for supporting my Alexa Skill named **Song Discovery** and available via [Amazon Marketplace](https://www.amazon.com/ZipBomb-Song-Discovery/dp/B07G236PNN/ref=sr_1_1?s=digital-skills&ie=UTF8&qid=1533660700&sr=1-1&keywords=song+discovery). It consists of:

- *random_song.py*: Module that contains functions to make requests to the [Spotify Web API](https://developer.spotify.com/documentation/web-api/) to retrieve pseudo-random songs based or not on a given valid genre.
- *genres_scrapper.py*: Simple scrapper for retrieving valid Spotify genres based on the info posted on [Everynoise.com](http://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity).
- *genres.json*: List containing every valid Spotify genre retrieved from [Everynoise.com](http://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity).

You may find this tools useful if you are searching for a way to make random requests of songs from the Spotify API as there is no function specified for that purpose and/or if you want to find a list of every valid music genre handled by Spotify.

---
**Project licensed under the MIT License.**
