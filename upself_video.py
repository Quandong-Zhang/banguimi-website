import sqlite3
import os
'''
上架视频脚本，开发中.....
'''
conn = sqlite3.connect("bgm.db",check_same_thread=False)


def main():
    cursor = conn.cursor()
    d=input("指定id")
    #if d=="":
    #    d=None
    #else:
    #    d=int(d)
    title=input("标题（番剧名称）：")
    desc=input("简介（不宜太长）：")
    img="./static/img/"+input("主封面图片名，文件放在 ./ststic/img/ 下")
    count=int(input("总集数："))
    back_string=input("视频文件后缀名，如 mp4 flv webm 等")
    if d:
        cursor.execute("insert into bgmList (id,title,desc,img,len) values (?,?,?,?,?)" , (d,title,desc,img,count))
    else:
        cursor.execute("insert into bgmList (title,desc,img,len) values (?,?,?,?,?)" , (title,desc,img,count))
    cursor.close()
    conn.commit()
    cursor = conn.cursor()
    cursor.execute("select * from bgmlist")
    d = cursor.fetchall()[-1][0]
    for p in range(1,count+1):
        purl = "./static/video/"+str(d)+"/"+str(p)+"."+back_string
        cursor.execute("insert into pList (id,p,purl) values (?,?,?)" , (d,p,purl))
    cursor.close()
    conn.commit()
    print("数据库写入成功！\n start to make dir")
    os.makedirs("./static/video/"+str(d))
    #input("将视频文件移动到弹出的窗口中：")
    input("将视频文件移动到"+"./static/video/"+str(d)+"\n 移动完之后按回车键")
    for r,d233,files in os.walk("./static/video/"+str(d),topdown=False):
        for index,name in enumerate(files):
            os.rename("./static/video/"+str(d)+"/"+name, "./static/video/"+str(d)+"/"+str(index+1)+"."+back_string)
    print("完毕！")



if __name__=='__main__':
    main()