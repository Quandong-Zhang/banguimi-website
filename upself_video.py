import sqlite3
'''
上架视频脚本，开发中.....
'''
conn = sqlite3.connect("bgm.db",check_same_thread=False)
cursor = conn.cursor()

def main():
    d=input("指定id（可以为空，将自动分配）")
    if d=="":
        d=None
    else:
        d=int(d)
    title=input("标题：")
    desc=input("简介：")
    img=input("图片链接：")
    count=int(input("总集数："))
    cursor.execute("insert into bgmList (id,title,desc,img,len) values (?,?,?,?,?)" , (d,title,desc,img,count))
    for n in range(1,count):
        


main()