import requests
from bs4 import BeautifulSoup
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
}

response = requests.get("http://books.toscrape.com/")
# print(response)
# print(response.status_code)#返回的http状态码
# if response.ok:#请求成功
#     print(response.text)#以字符串储存响应内容
# else:#请求失败
#     print("请求失败")
content = response.text
soup = BeautifulSoup(content, "html.parser")
print(soup.p)#打印第一个<p></p>标签里的内容
print(soup.img)#打印第一个<img></img>标签里的内容

all_prices = soup.find_all("p",attrs={"class":"price_color"})#找到所有的p标签内容，且这个标签的class是price_color
for price in all_prices:
    # print(price) #会打印出所有,如：<p>……</p>
    print(price.string)#只打印标签内容
all_titles = soup.find_all("h3")
for title in all_titles:
    all_links = title.find_all("a")
    for link in all_links:
        print(link.string)