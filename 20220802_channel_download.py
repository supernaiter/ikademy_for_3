import urllib.request
import urllib.parse
import json
import csv
import isodate
import datetime
import argparse


# Import required packages
import os
import time 
import ffmpeg
import re
import urllib.request
import multiprocessing
import csv
from datetime import datetime
# def youtubevidgettor(vid_url):
#     d_vid = YouTube(vid_url).streams.first(# Import required packages
import cv2
import pytesseract
from pytube import YouTube
import os
import time
import sys
import subprocess
import urllib.request
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from datetime import datetime
# def youtubevidgettor(vid_url):
#     d_vid = YouTube(vid_url).streams.first().download(filename='video.mp4')
# # Mention the installed location of Tesseract-OCR in your system
from moviepy.editor import VideoFileClip

#-------↓パラメータ入力↓-------

parser = argparse.ArgumentParser()

parser.add_argument('--APIKEY',help='APIKEY')

parser.add_argument('--channel_id',help='channel_id')

args = parser.parse_args()

#channel_id = 'UC4BQjeEH7-iUqUbyYVDYtsg'


APIKEY = args.APIKEY
channel_id = args.channel_id

print(APIKEY,channel_id)

#-------↑パラメータ入力↑-------

#dt_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
nextPageToken = ''
item_count = 0
outputs = []
#outputs.append(['publishedAt', 'title', 'description', 'url', 'thumbnail_url', 'categoryId', 'liveBroadcastContent', 'duration', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 'embedHtml'])
n = 0


frmlist =[]
start_frame_list = []
end_frame_list = []
count1=[]
count2=['1']
youtube_links = []
matches= []
ff = []
path = os.getcwd()

def youtubevidgettor(vid_url, folder_maker):
    count1.clear()
    start_frame_list.clear()
    count2.append('1')
    res= '720p'
    # video_path = r'{}/videos/{}'.format(path, folder_maker)
    video_path = os.path.join(path,"footages",folder_maker)
    print(video_path)
    if os.path.exists(video_path):
            print(video_path,'already exists.')

    #if not os.path.exists(os.path.join(path,"footages")):
    #    os.mkdir(os.path.join(path,"footages"))
    
    #video_path = os.path.join(path,"footages",folder_maker)
    #print(video_path)
    else:
        os.mkdir(video_path)
        print("here")

        yt=YouTube(vid_url).streams.filter(fps=30 , res='1080p').first()
        if yt is not None:
            print('downloading')
            print('{}.mp4'.format(folder_maker))
            #yt.download(filename='{}.mp4'.format(folder_maker),output_path= video_path)
            yt.download(filename='raw.mp4',output_path= video_path)
            print('downloaded')

            #os.remove(r'{}/{}.mp4'.format(video_path, folder_maker))
        elif yt is None and res=='720p':
            print('downloading')
            print('{}.mp4'.format(folder_maker))
            yt = YouTube(vid_url).streams.filter(fps=30, res=res).first()
            if yt is not None:
                #yt.download(filename='{}.mp4'.format(folder_maker),output_path= video_path )
                yt.download(filename='raw.mp4',output_path= video_path)
                print('downloaded')
                #os.remove(r'{}/{}.mp4'.format(video_path, folder_maker))

        else:
            print('No Video Found Of Required Quality')
            os.rmdir(video_path)


def youtube_crawler(one_video):
    try:
        print(one_video)
        video_id = one_video[1]
        #video_id = list(dict.fromkeys(video_id))
        print("video_id",video_id)
        with open("video_id.txt",'a+') as f:
            if video_id not in f.readlines():
                f.write('{}\n'.format(video_id)) 
                f.close()
                # print(url)
        # with open("video_id.txt",'r') as f:   
        f=open("video_id.txt",'r')
        link_list  = {x.replace('\n','') for x in f.readlines()}
        for link in link_list:
            print(link)
            url = 'https://www.youtube.com/watch?v={}'.format(link)
            try:
                youtubevidgettor(url, link)

            except Exception as E:
                print(E)
                raise
    except Exception as E:
        print(E)




if __name__ == "__main__":
    while True:
        #searchメソッドでvideoid一覧取得
        param = {
            'part':'snippet',
            'channelId':channel_id,
            'maxResults':50,
            'order':'date',
            'type':'video',
            'pageToken':nextPageToken,
            'key':APIKEY
        }
        target_url = 'https://www.googleapis.com/youtube/v3/search?'+urllib.parse.urlencode(param)
        print('動画リスト取得')
        print(target_url)

        req = urllib.request.Request(target_url)
        try:
            with urllib.request.urlopen(req) as res:
                search_body = json.load(res)
                item_count += len(search_body['items'])
                video_list = []
                for item in search_body['items']:
                    #videoメソッド用list作成
                    video_list.append(item['id']['videoId'])
                    
                #videoメソッドで動画情報取得
                param = {
                    'part':'id,snippet,contentDetails,liveStreamingDetails,player,recordingDetails,statistics,status,topicDetails',
                    'id':",".join(video_list),
                    'key':APIKEY
                }
                target_url = 'https://www.googleapis.com/youtube/v3/videos?'+(urllib.parse.urlencode(param))
                print('動画情報取得：合計' + str(item_count)+'件')
                print(target_url)

                req = urllib.request.Request(target_url)
                try:
                    with urllib.request.urlopen(req) as res:
                        videos_body = json.load(res)
                        #CSV書き込み用データ準備
                        for item in videos_body['items']:
                            #値が存在しない場合ブランク
                            publishedAt = item['snippet']['publishedAt'] if 'publishedAt' in item['snippet'] else ''
                            title = item['snippet']['title'] if 'title' in item['snippet'] else ''
                            description = item['snippet']['description'] if 'description' in item['snippet'] else ''
                            url = 'https://www.youtube.com/watch?v=' + item['id'] if 'id' in item else ''
                            thumbnail_url = item['snippet']['thumbnails']['high']['url'] if 'thumbnails' in item['snippet'] else ''
                            categoryId = item['snippet']['categoryId'] if 'categoryId' in item['snippet'] else ''
                            liveBroadcastContent = item['snippet']['liveBroadcastContent'] if 'liveBroadcastContent' in item['snippet'] else ''
                            if 'duration' in item['contentDetails']:
                                #durationを時分秒へ変換
                                duration = isodate.parse_duration(item['contentDetails']['duration'])
                            else:
                                duration = ''
                            viewCount = item['statistics']['viewCount'] if 'viewCount' in item['statistics'] else 0
                            likeCount = item['statistics']['likeCount'] if 'likeCount' in item['statistics'] else 0
                            favoriteCount = item['statistics']['favoriteCount'] if 'favoriteCount' in item['statistics'] else 0
                            commentCount = item['statistics']['commentCount'] if 'commentCount' in item['statistics'] else 0
                            embedHtml = item['player']['embedHtml'] if 'embedHtml' in item['player'] else ''
                            outputs.append([title, item['id']])
                            n += 1

                except urllib.error.HTTPError as err:
                    print(err)
                    break
                except urllib.error.URLError as err:
                    print(err)
                    break
            
            #nextPageTokenが表示されなくなったらストップ
            if 'nextPageToken' in search_body:
                nextPageToken = search_body['nextPageToken']
            else:
                break

        except urllib.error.HTTPError as err:
            print(err)
            break
        except urllib.error.URLError as err:
            print(err)
            break


    print(outputs)

    with multiprocessing.Pool(processes=3) as pool:
        pool.map(youtube_crawler, outputs)
