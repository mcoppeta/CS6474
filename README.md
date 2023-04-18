# CS6474
CS 6474 Project

Libraries used:
sklearn
vaderSentiment

Put developer key in get_yt_data.py script.

Add YouTube video id's to id_toget.txt on newlines, 1s or 0s for about___ field:
`aboutApple aboutSamsung videoID`

Run get_yt_data.py

Data will be in youtube_data.txt with columns:
'comment', 'commentLikes', 'commentReplies', 'commentTimestamp', 'videoTitle', 'videoViews', 'videoLikes', 'videoComments', 'videoAboutApple', 'videoAboutSamsung'