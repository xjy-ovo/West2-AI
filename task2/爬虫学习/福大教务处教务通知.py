import requests
from bs4 import BeautifulSoup
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
}

for i in range(205,204,-1):
    response=requests.get(f"https://jwch.fzu.edu.cn/jxtz/{i}.htm",headers=headers)
    response.encoding = "utf-8"  # 显式指定编码为utf-8
    content = response.text

    soup = BeautifulSoup(content,"html.parser")
    all_item = soup.find("ul", attrs={"class":"list-gl"}).find_all("li")

    for item in all_item:
        # 处理时间
        time = item.find("span", attrs={"class": "doclist_time"})
        clean_time=""
        if time:  # 先判断time是否存在
            time_string = time.string
            clean_time = time_string.replace('\r', '').replace('\n', '').strip()
            print(clean_time, end=' ')
        else:
            print("无时间", end=' ')  # 处理未找到时间的情况
        
        # 处理标题和详情链接
        title = item.find("a")
        link=''
        Title=""
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
        print()
            
        info = requests.get(f"https://jwch.fzu.edu.cn/{link}",headers=headers)
        info.encoding = "utf-8"
        info_content = info.text
        info_soup = BeautifulSoup(info_content,"html.parser")
        #     # 获取所有ul标签
        # all_uls = info_soup.find_all("ul")
        # # 打印每个ul的属性和部分内容
        # for i, ul in enumerate(all_uls):
        #     print(f"\n第{i+1}个ul标签：")
        #     print("属性：", ul.attrs)  # 打印ul的所有属性（如style、class等）
        #     print("部分内容：", ul.text[:50])  # 打印前50个字符，判断是否是目标
        all_attach = info_soup.find("ul",attrs={'style': 'list-style-type:none;'})
        if all_attach:
            all_attach = all_attach.find_all("li")
            for attach in all_attach:
            # 处理附件名
                a_tag = attach.find("a")
                attach_name = a_tag.string if a_tag else "无附件名"
                
                # 处理下载次数
                span_tag = attach.find("span")
                doneload_sum = span_tag.string if span_tag else "0"
                
                # 处理附件链接
                attach_link = a_tag.get("href") if a_tag else "无链接"
                
                print(f"{attach_name} {doneload_sum} {attach_link}")
        else:
            attach_name="无附件名"
            doneload_sum=0
            attach_link="无链接"
            print("无附件")
        
        print()
  