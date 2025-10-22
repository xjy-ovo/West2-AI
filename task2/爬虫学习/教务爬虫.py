import os
import csv
import requests
from bs4 import BeautifulSoup
import json

# 通过 script 提取下载次数（来自gpt）
def get_click_params(script_text):
    script_text = script_text.strip()
    # 形如：getClickTimes(16712478,1744984858,"wbnewsfile","attach")
    if script_text.startswith("getClickTimes(") and script_text.endswith(")"):
        inner = script_text[len("getClickTimes("):-1]
        parts = [p.strip().strip('"') for p in inner.split(",")]
        if len(parts) >= 2:
            return parts[0], parts[1]
    return None, None

def get_download_times(aid, owner):#（来自gpt）
    url = f"https://jwch.fzu.edu.cn/system/resource/code/news/click/clicktimes.jsp?wbnewsid={aid}&owner={owner}&type=wbnewsfile&tablename=attach"
    try:
        r = requests.get(url, timeout=5)
        data = json.loads(r.text.strip())   # ✅ 解析返回的JSON字符串
        return str(data.get("wbshowtimes", "0"))  # 只取下载次数
    except Exception:
        return "0"
    


def main():
    #创建保存附件的文件夹
    os.makedirs("attachments",exist_ok=True)
    
    with open("result.csv","w",newline="utf-8-sig") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["时间", "标题", "详情链接", "通知人", "附件名", "下载次数", "附件链接", "附件保存路径"])

        heads={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0"
        }
        
        for i in range(205,190,-1):
            #获取每一个通知
            url = f"https://jwch.fzu.edu.cn/jxtz/{i}.htm"
            response = requests.get(url,headers=heads,timeout=10)
            response.encoding="utf-8"
            soup=BeautifulSoup(response.text,"html.parser")
            all_item = soup.find("ul",atters={"class":"list-gl"}).find_all("li")
            
            for item in all_item:
                #时间
                time_tag = item.find("span",atters={"class":"doclist_time"})
                clean_time = "无时间"
                if time_tag:  # 先判断time是否存在
                    time_string = time_tag.string
                    clean_time = time_string.replace('\r', '').replace('\n', '').strip()
                
                #标题和详情链接
                title_tag = item.find("a")
                link=""
                Title="无标题"
                if title_tag:
                    Title = title_tag.string
                    link = title_tag.get("href")
                    
                #通知人
                person = "无通知人"
                if time_tag and time_tag.next_sibling:
                    person = time_tag.next_siblings.replace('\n','').replace('\r', '').replace('【', '').replace('】', '').strip()
                
                #详情页
                info = requests.get(f"https://jwch.fzu.edu.cn/{link}", headers=heads, timeout=10)
                info.encoding = "utf-8"
                info_soup = BeautifulSoup(info.text,"html.parser")
                all_attach = info_soup.find("ul",attrs={"style":"list-style-type:none;"})
                
                if all_attach:
                    li_tags = all_attach.find_all("li")
                    for li in li_tags:
                        attach_name = "无附件名"
                        attach_link = "无链接"
                        doneload = "0"
                        attach_path = ""
                        
                        a_tag = li.find("a")
                        if a_tag:
                            attach_name = a_tag.text.strip()
                            attach_link = a_tag.get("href")
                            if attach_link and attach_link.startswith("/"):
                                attach_link = "https://jwch.fzu.edu.cn" + attach_link

                        # 解析 script 获取下载次数 (这个来自于chatgpt)
                        script_tag = li.find("script")
                        if script_tag and script_tag.string:
                            aid, owner = get_click_params(script_tag.string)
                            if aid and owner:
                                doneload_sum = get_download_times(aid, owner)
                        
                        # 下载附件 （来自gpt（一部分）
                        if attach_link != "无链接":
                            file_ext = os.path.splitext(attach_link.split("?")[0])[1]
                            safe_name = attach_name.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_")
                            filename = f"{safe_name}{file_ext}" if file_ext else f"{safe_name}.bin"
                            filepath = os.path.join("attachments", filename)

                            file_resp = requests.get(attach_link, headers=heads, timeout=20)
                            with open(filepath, "wb") as f:
                                f.write(file_resp.content)

                            attach_path = filepath
                                
                        csv_writer.writerow([clean_time, Title, link, person, attach_name, doneload_sum, attach_link, attach_path])
                else:
                    csv_writer.writerow([clean_time, Title, link, person, "无附件名", "0", "无链接", ""])    
                    
if __name__ == "__main__":
    main()