import requests  
import os
from bs4 import BeautifulSoup  
import csv  
  
def fetch_data(url):  
    # 发送HTTP GET请求  
    # response = requests.get(url)  
    # 确保请求成功  
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_trs_uv=lxn54c6j_6267_j39x; wzws_sessionid=gDEyNC44OS4xMTguMTk1oGbVcfmCN2VkMmQwgWU4ZGIxYQ==; CPS_SESSION=9297622C0009D862F61D4E6FE0818248; _trs_ua_s_1=m0lqm4u3_6267_b8ox',
        'Referer': 'https://www.stats.gov.cn/search/s?qt=70%E4%B8%AA%E5%A4%A7%E4%B8%AD%E5%9F%8E%E5%B8%82%E5%95%86%E5%93%81%E4%BD%8F%E5%AE%85%E9%94%80%E5%94%AE%E4%BB%B7%E6%A0%BC&siteCode=bm36000002&tab=all&toolsStatus=1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(
        url,
        headers=headers,
    )
    response.encoding = 'utf8'

    os.makedirs(basepath, exist_ok=True)

    with open(f"{basepath}.html", 'w', encoding='utf8') as f:
        f.write(response.text)

    # 解析HTML  
    soup = BeautifulSoup(response.text, 'html.parser')  
    # 查找包含数据的table（这里需要根据实际网页结构调整查找方式）  
    tables = soup.find_all('table')  
        
    # 假设第一个table是我们需要的  
    if tables:  
        # table = tables[0] 
        for idx, table in enumerate(tables): 
            # 初始化CSV文件  
            with open(f'{basepath}_{idx}.csv', 'w', newline='', encoding='utf-8') as csvfile:  
                writer = csv.writer(csvfile)  
                    
                # 遍历表格的每一行  
                for row in table.find_all('tr'):  
                    cols = row.find_all('td')  # 如果表格中有th标签，也可能需要处理th  
                    cols = cols + [row.find('th')] if row.find('th') else cols  
                    # 提取数据并写入CSV  
                    rows_data = [ele.text.strip() for ele in cols]  
                    writer.writerow(rows_data)  
    else:  
        print("No table found in the HTML.")  


# 目标网页URL  
url = 'https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202405/t20240517_1950386.html'
basepath = "datas/m4/april"

fetch_data(url)
