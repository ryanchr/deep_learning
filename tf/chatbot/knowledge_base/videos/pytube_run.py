from pytube import YouTube

##url = "https://www.youtube.com/watch?v=hkxT0nR6dxY"
url = "https://www.youtube.com/watch?v=QGarmmz2S78"

yt = YouTube(url)
##yt = yt.get('mp4', '720p')
yt.streams.first().download()
