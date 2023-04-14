# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import numpy as np
import re

import googleapiclient.discovery

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAN17yfOJXIalDCcSKfr1_LXtpKKll_V48"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)



def api_call(videoId, npt=None):
    NUM = 100
    if npt is None:
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=NUM,
            order='relevance',
            textFormat="html",
            videoId=videoId
        )
    else:
        request = youtube.commentThreads().list(
            part="snippet",
            maxResults=NUM,
            order='relevance',
            textFormat="html",
            videoId=videoId,
            pageToken=npt
        )

    responseComments = request.execute()

    return responseComments

def get_stats(videoId):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=videoId
    )
    responseStats = request.execute()
    return responseStats

def handle_response(response, title, views, likes, comments):
    items = []
    for thread in response['items']:
        threadData = thread['snippet']
        numReplies = threadData['totalReplyCount']
        tlc = threadData['topLevelComment']
        comment = tlc['snippet']
        numLikes = comment['likeCount']
        timestamp = comment['publishedAt']
        text = comment['textOriginal']
        text = reformat_str(text)

        item = [text, numLikes, numReplies, timestamp, title, views, likes, comments]
        items.append(item)
    return items

def write(data, ids):
    np.savetxt('./youtube_data.txt', data, fmt='%s', encoding='utf-8', delimiter='|')

    with open('./id_written.txt', 'w') as file:
        for i in ids:
            file.write(i + "\n")

def load_data():
    data = np.loadtxt('./youtube_data.txt', dtype=object, encoding='utf-8', delimiter="|", comments=None)
    if len(data) == 0:
        data = [['comment', 'commentLikes', 'commentReplies', 'commentTimestamp', 'videoTitle', 'videoViews', 'videoLikes', 'videoComments']]
    
    with open('./id_written.txt', 'r') as file:
        rawids = file.read().split('\n')
        written_ids = []
        for idx in rawids:
            if idx:
                written_ids.append(idx)

    with open('./id_toget.txt', 'r') as file:
        rawids = file.read().split('\n')
        get_ids = []
        for idx in rawids:
            if idx:
                get_ids.append(idx)

    return data, written_ids, get_ids

def reformat_str(word):
    updated = re.sub(r'\|', ' ', word)
    updated = re.sub(r'\n', ' ', updated)
    return updated

def main():
    video_data, written_ids, video_ids = load_data()
    print(video_data)
    print()
    print(written_ids)
    print()
    PAGES = 2
    NPT = 'nextPageToken'

    #videoId="kCqN4xdkrbY" # many comments (BLR)
    #videoId="01tWk1qSX4I" # 14 comments
    #videoId="GDENKNxgycM" # no comments


    for videoId in video_ids:
        if videoId in written_ids:
            print("skipping:\t", videoId)
            continue
        else:
            print(videoId)
            stats = get_stats(videoId)['items'][0]
            title = stats['snippet']['title']
            title = reformat_str(title)
            views = stats['statistics']['viewCount']
            likes = stats['statistics']['likeCount']
            comments = stats['statistics']['commentCount']

            response = api_call(videoId)
            response_data = handle_response(response, title, views, likes, comments)
            if len(response_data) > 0:
                video_data = np.vstack([video_data, response_data])

            if NPT in response:
                npt = response[NPT]
                for i in range(PAGES - 1):
                    response = api_call(videoId, npt=npt)
                    response_data = handle_response(response, title, views, likes, comments)
                    if len(response_data) > 0:
                        video_data = np.vstack([video_data, response_data])
                    else:
                        break
                    if NPT in response:
                        npt = response[NPT]
                    else:
                        break

            written_ids.append(videoId)

    write(video_data, written_ids)

    #print(video_data)
    print('\n', len(video_data))

if __name__ == "__main__":
    main()
