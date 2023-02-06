import spotipy, os, re
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from youtubesearchpython import VideosSearch

def main():
    # PLAYLIST_LINK Example: https://open.spotify.com/playlist/1vaF88Z5msDzwFfRBa1IyM?si=fd5bf015b8a74445
    PLAYLIST_LINK = str(input("Enter Playlist Link from Spotify: "))

    # Loading Credentials from .env file
    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")

    # Authentication
    client_credentials_manager = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )

    # Create session object
    session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    match = re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK)
    if match:
        PLAYLIST_URI = match.groups()[0]
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")

    tracks = session.playlist_tracks(PLAYLIST_URI)["items"]

    FOLDER_NAME = session.user_playlist(user=None, playlist_id=PLAYLIST_URI, fields="name")["name"]
    print("Folder Name:" + " " + FOLDER_NAME)
    

    path = f"{os.environ['UserProfile']}/Music/" + FOLDER_NAME + "/"

    print(path)
    try: 
        os.mkdir(path) 
    except OSError as error: 
        print(error)

    # Get the list of artist and songs
    counter = 0
    for track in tracks:
        for artist in track["track"]["artists"]:
            videosSearch = VideosSearch(artist["name"] + " - " + track["track"]["name"], limit = 1)
            yt = YouTube(videosSearch.result()["result"][0]["link"])
            audio_file = yt.streams.filter(only_audio=True).first()

        # Download Songs from YouTube
        try: 
            out_file = audio_file.download(output_path=path, filename='.mp3', filename_prefix=track["track"]["name"] + ' - ' + artist["name"])    
        except OSError as error: 
            print("Failed to Download ("+ artist["name"] + " - " + track["track"]["name"] +")")
            continue
            
        counter += 1
        print(str(counter) + "/" + str(len(tracks)) + " (" + artist["name"] + " - " + track["track"]["name"] +")")

    print("Download Done ^____^")


if __name__ == "__main__":
    main()