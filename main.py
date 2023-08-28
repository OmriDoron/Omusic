import json
from googleapiclient.discovery import build
from pytube import YouTube
import os


def input_username():
    username = str(input("enter username: "))
    if os.path.exists('./'+username) == False:
        os.mkdir('./' + username)

    return username

def read_config():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    return config

def search_youtube(song, api_key):
    youtube = build("youtube", "v3", developerKey=api_key)

    search_response = youtube.search().list(
        q=song,
        part="id",
        maxResults=1
    ).execute()

    video_id = search_response.get("items", [])[0]["id"]["videoId"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return video_url

def main():
    config = read_config()
    api_key = config.get("YOUTUBE_API_KEY")

    if not api_key:
        print("YouTube API key not found in the configuration.")
        return
    Username = input_username()
    search_song = input("Enter your song name: ")
    video_url = search_youtube(search_song, api_key)

    print(f"URL of the first video in search results: {video_url}")

    # url input from user
    yt = YouTube(str(video_url))

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    # check for destination to save file
    print("Enter the destination (leave blank for current directory)")
    destination = str('./'+ Username)
    temp_file_name = './' + Username+ '\\' + str(yt.title)+ '.mp3'
    file_name = os.path.abspath(temp_file_name)
    if os.path.isfile(file_name) == False:
    # save the file
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print(yt.title + " has been successfully downloaded.")
    else:
        print("there is alredy that file")








if __name__ == "__main__":
    main()