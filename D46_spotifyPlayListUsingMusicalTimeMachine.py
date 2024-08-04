from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv


wantedDate = input('Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ')

response = requests.get(f'https://www.billboard.com/charts/hot-100/{wantedDate}/')
htmlData = response.text
soup = BeautifulSoup(htmlData, 'html.parser')

# Put Scraped Song names into a List
songs = soup.select('ul li ul li h3')
namesList = [ item.get_text().strip() for item in songs ] ## otherwise: \t\t\tBat Country\t\


# Access Spotify API: use spotipy library
    # spotify developer: https://developer.spotify.com/dashboard
    # spotifyOAuth(): https://spotipy.readthedocs.io/en/2.13.0/#spotipy.oauth2.SpotifyOAuth
    # sotipy: https://spotipy.readthedocs.io/en/2.24.0/

load_dotenv('E:\\Stella\\PythonProjectFiles\\EnvVar.env')
clientID = os.getenv('clientID')
clientSecret = os.getenv('clientSecret')

sp = spotipy.Spotify(auth_manager= SpotifyOAuth(
    client_id= clientID,
    client_secret= clientSecret,
    redirect_uri='http://example.com',
    scope='playlist-modify-private',  ##in order to create a private playlist on Spotify
    username='ElysiumPanda'
))

# results = sp.current_user_saved_tracks()  ##如果没有这一步不会有弹窗和跳出redirect page
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# Then copy the entire URL in the address bar TO the prompt in PyCharm
# Then close PyCharm and restart, see a new file in this project called token.txt OR .cache


# Get the user id of the authenticated user (your Spotify username)
    ## method: https://spotipy.readthedocs.io/en/2.13.0/#spotipy.client.Spotify.current_user
user = sp.current_user()
userID = user['id']



# Create a list of Spotify song URIs for the list of song names from 'scraping billboard 100'.
    ## search query --spotify doc: https://developer.spotify.com/documentation/web-api/reference/search

yyyy= wantedDate[:4]

for item in nameList:  # to get song ID
    q = f'track%3A%20%7B{name}%7D%20year%3A%20%7B{yyyy}%7D' # Decode: track: {name} year: {yyyy}'
        # sample: q=f'remaster%2520track%3ADoxy%2520artist%3AMiles%2520Davis' --The available filters are album, artist, track, year, upc, tag:hipster, tag:new, isrc, and genre

    track_js = sp.search(q, limit=1, offset=0, type='track', market=None)


    # add_to_queue(uri, device_id=None)