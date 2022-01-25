import urllib.request
import requests
import os
import parsel
import re

url = 'https://www.jdlingyu.com/tag/%e5%b0%91%e5%a5%b3'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

# 2.发送指定地址请求，请求数据 getpost 请求 响应
response = requests.get(url=url, headers=headers)
html_str = response.text
#print(html_str)

# 3.数据提取
selector = parsel.Selector(html_str)

lis = selector.xpath('//div[@id="post-list"]/ul/li')

for li in lis:
    pic_title = li.xpath('.//h2/a/text()').get()  #相册标题
    pic_url = li.xpath('.//h2/a/@href').get()     #相册链接
    print('正在下载相册：', pic_title)

    #构建相册文件夹
    if not os.path.exists('img\\' + pic_title): #没有该路径文件夹
        os.mkdir('img\\' + pic_title)

    #发送详情页地址请求 response
    response_pic = requests.get(url=pic_url, headers=headers).text

    #解析详情页中图片地址
    selector_2 = parsel.Selector(response_pic)
    pic_url_list = selector_2.xpath('//div[@class="entry-content"]//img/@src').getall()
    #print(pic_url_list)

    for pic_url in pic_url_list:#遍历每一个图片地址
        #发送图片链接请求，获取图片数据，图片数据是二进制，content：提取二进制
        img_data = requests.get(url=pic_url, headers=headers).content

    #4数据保存

        file_name = pic_url.split('/')[-1] #拆分，只取最后一个元素.
        print(file_name)
    #
    # #w write b binary二进制
        with open(f'img\\{pic_title}\\{file_name}', mode='wb') as f:
            f.write(img_data)
            print('保存成功:', file_name)

