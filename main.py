import soundcloud
import urllib.request
import json
import requests
import time

clientID = "YOUR_CLIENT_ID_HERE"
client = soundcloud.Client(client_id=clientID)
api_base = "https://api.soundcloud.com"


def get_user_info(username):
    user = client.get('/resolve', url='http://soundcloud.com/{}/'.format(username))
    user_info = urllib.request.urlopen("{}/users/{}.json?consumer_key={}".format(api_base, user.id, clientID)).read()
    user_info_data = json.loads(user_info.decode())
    number_of_likes = user_info_data['public_favorites_count']
    username = user_info_data['username']
    return username, number_of_likes, user


user_information = get_user_info(input("Please enter your username: "))
user_name = user_information[0]
number_of_user_likes = user_information[1]
userID = user_information[2]

csv_file = open("{} like list.csv".format(user_name), "w", encoding='UTF-8')
csv_file.write("Track Title, Track URL\n")  # Writes headers to CSV file

offset_number = 0
page_size = 200
get_next_page = True
while get_next_page:
    try:
        if offset_number == 0:
          tracks_fetch = urllib.request.urlopen(
              "{}/users/{}/favorites?client_id={}&limit={}&linked_partitioning=1".format(api_base, userID.id, clientID,page_size)).read()
          tracks = json.loads(tracks_fetch.decode())
        else:
          tracks_fetch = urllib.request.urlopen(tracks['next_href']).read()
          tracks = json.loads(tracks_fetch.decode())
        for track in tracks['collection']:
          track_title = track['title'].replace(",", "")  # Removes commas as causes issues with .csv files
          csv_file.write("{},{}\n".format(track_title, track['permalink_url']))
        get_next_page = 'next_href' in tracks
        
        offset_number += 1
        print("Got page {} of {} results".format(offset_number,len(tracks['collection'])))
    except (IndexError, requests.HTTPError, urllib.error.HTTPError):
        print("There is an issue with Soundcloud, please try again")
        time.sleep(1)
    except requests.ConnectionError:
        print("Check your internet connection")
