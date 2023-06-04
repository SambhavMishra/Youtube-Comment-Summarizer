import os
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.discovery import build
from preprocess import preprocess

# Replace with your own YouTube API key
class video_comments():

    def __init__(self):
        self.API_KEY = "AIzaSyAF3Lo8HQ3v467prHUKtzxfS3OCwiwXJ6I"
        self.process = preprocess()

    # Get video ID from the video link
    def get_video_id(self, link):
        return link.split("=")[1]

    # Get comments from a video using the YouTube Data API
    def get_comments(self, video_id):
        youtube = build("youtube", "v3", developerKey=self.API_KEY)
        comments = []
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=next_page_token
            ).execute()
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(self.process.totalPreprocess(comment))
            if "nextPageToken" in response:
                next_page_token = response["nextPageToken"]
            else:
                break
        self.count = len(comments)
        comments = ' '.join(comments)
        return comments

# Main function to get video link and print comments
def main():
    vc = video_comments()
    video_link = input("Enter YouTube video link: ")
    video_id = vc.get_video_id(video_link)
    comments = vc.get_comments(video_id)
    print("Comments:")
    for comment in comments:
        print(comment)

if __name__ == "__main__":
    main()
