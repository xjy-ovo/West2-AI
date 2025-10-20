import requests
from bs4 import BeautifulSoup
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
}

for i in range(205,179,-1):
    response=requests.get(f"https://jwch.fzu.edu.cn/jxtz/{i}.htm",headers=headers)
    response.encoding = "utf-8"  # 显式指定编码为utf-8
    content = response.text

    soup = BeautifulSoup(content,"html.parser")
    all_item = soup.find("ul", attrs={"class":"list-gl"}).find_all("li")

    for item in all_item:
        # 处理时间
        time = item.find("span", attrs={"class": "doclist_time"})
        if time:  # 先判断time是否存在
            time_string = time.string
            clean_time = time_string.replace('\r', '').replace('\n', '').strip()
            print(clean_time, end=' ')
        else:
            print("无时间", end=' ')  # 处理未找到时间的情况
        
        # 处理标题和详情链接
        title = item.find("a")
        link=''
        if title and title.string:  # 先判断title是否存在且有string属性
            print(title.string,end=' ')
            link = title.get("href")
            print(link,end=' ')
        else:
            print("无标题",end=' ')  # 处理未找到标题的情况
            
        # 处理通知人
        person = ""
        if time and time.next_sibling:
            person = time.next_sibling.strip()
            # 清理一下，比如质量办
            person = person.replace('\n', '').replace('\r', '').replace('【', '').replace('】', '').strip()
            print(person,end=' ')
        if not person:
            person = "无通知人"
            
        attach = requests.get(f"http://{link}",headers=headers)
        
        print()
  