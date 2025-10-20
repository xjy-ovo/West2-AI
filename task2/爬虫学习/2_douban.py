import requests
from bs4 import BeautifulSoup
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
}

for start_num in range(0,250,25):
    response=requests.get(f"http://movie.douban.com/top250?start={start_num}",headers=headers)
    print(response.text)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    print(soup.p)#打印第一个<p></p>标签里的内容
    print(soup.img)#打印第一个<img></img>标签里的内容

    all_titles = soup.find_all("span",attrs={"class":"title"})
    for title in all_titles:
        #print(title.string) #找到所有标题，包括中文标题和原版标题
        title_string = title.string
        if(title_string[1]!='/'):
            print(title_string)
        