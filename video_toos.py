import os

def flv2mp4(index,out):
    os.system("ffmpeg -i "+str(index)+".flv "+str(out)+".mp4")

def get_flv_url_path(name):
    return "./static/video/"+str(name)

def get_mp4_url_path(name):
    return "./static/video/"+str(name)

def get_image_url_path(name):
    return "./static/img/"+str(name)

if __name__=="__main__":
    #flv2mp4(1, 1)
    #print(get_video_url_path("1"))
    d = input("id?")
    for n in range(1,int(input("共几集？"))):
        flv2mp4(get_flv_url_path(d+"/"+str(n)), get_mp4_url_path(d+"/"+str(n)))