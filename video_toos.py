import os

def flv2mp4(index,out):
    os.system("ffmpeg -i "+str(index)+".flv "+str(out)+".mp4")

def get_video_url_path(name):
    return "./static/video/"+str(name)+".mp4"

def get_image_url_path(name):
    return "./static/img/"+str(name)

if __name__=="__main__":
    #flv2mp4(1, 1)
    print(get_video_url_path("1"))