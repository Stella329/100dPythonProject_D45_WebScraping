from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import pprint


wantedDate = input('Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ')

response = requests.get(f'https://www.billboard.com/charts/hot-100/{wantedDate}/')
htmlData = response.text
soup = BeautifulSoup(htmlData, 'html.parser')

# Put Scraped Song names into a List
songs = soup.select('ul li ul li h3')
namesList = [item.get_text().strip() for item in songs] ## otherwise: \t\t\tBat Country\t\


# STEP2: Access Spotify API: use spotipy library
    # spotify developer-我的app: https://developer.spotify.com/dashboard
    # spotifyOAuth(): https://spotipy.readthedocs.io/en/2.13.0/#spotipy.oauth2.SpotifyOAuth
    # sotipy doc: https://spotipy.readthedocs.io/en/2.24.0/
    # 更多spotify功能：more scope: https://developer.spotify.com/documentation/web-api/concepts/scopes

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
# for idx, item in enumerate(results['items']): ##more spotify test samples
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# next step:
# Then copy the entire URL in the address bar TO the prompt in PyCharm
# Then close PyCharm and restart, see a new file in this project called token.txt OR .cache


# Get the user id of the authenticated user (your Spotify profile)
    ## method: https://spotipy.readthedocs.io/en/2.13.0/#spotipy.client.Spotify.current_user
user = sp.current_user()
userID = user['id']



# # STEP3: Create a list of Spotify song URIs, for the list of song names from 'scraping billboard 100'.
#     ## Search query: how to write --spotify doc: https://developer.spotify.com/documentation/web-api/reference/search

yyyy= wantedDate[:4]

uri_list = []
uri_dict = {}
for name in namesList:  # to get song ID
    try:
        query = f'track%3A%20%7B{name}%7D%20year%3A%20%7B{yyyy}%7D' # Decode: track: {name} year: {yyyy}'
            # sample: q=f'remaster%2520track%3ADoxy%2520artist%3AMiles%2520Davis' --The available filters are album, artist, track, year, upc, tag:hipster, tag:new, isrc, and genre

        response_trackJs = sp.search(query, limit=1, offset=0, type='track', market=None)
        uri = response_trackJs['tracks']['items'][0]['uri'][
              14:]  # remove suffix in: 'spotify:track:6qyIvmBYgPHyS6Yh8Z44Eg'
    except IndexError:
        print(f'song {name} not found.')
        uri_dict[name]= 'Not Found'
    else:
        uri_list.append(uri) # Only lists are accepted when you add items to the playlist
        uri_dict[name]=uri #test, list返回了101项; dict匹配了99项 --可匹配排障，未完成

# uri_list.insert(4, uri_list)
# pprint.pp(uri_list)
# print(len(uri_list))
#
# pprint.pp(uri_dict)
# print(len(uri_dict))



# STEP4: Create a new playlist to my app; --You'll need the user id you got before
# Then add each of the song found to the new playlist
# doc: spotipy documentation上 -- use client Module->Playlist and sp obj created in STEP2

playlist = sp.user_playlist_create(user=userID, name=f'TimeMachine: Playlist for {wantedDate}', public=False) #create playlist
    ## public=False 因为前sp中参数为scope='playlist-modify-private'；否则会出现Error: Insufficient client scope
print(playlist)

sp.user_playlist_add_tracks(user =userID, playlist_id=playlist['id'], tracks=uri_list) #add tracks; tracks - a list of track URIs, URLs or IDs 注意只能是list！