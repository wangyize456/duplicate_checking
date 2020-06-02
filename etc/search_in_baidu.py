from math import floor
from selenium.webdriver import ChromeOptions, Chrome
import time
import random
import re

def get_search_result(url, data):
    opt = ChromeOptions()
    opt.headless = True
    browser = Chrome(options=opt)    #指定浏览器 '''除了chrome以外的浏览器对于开发没有卵用
    browser.get(url)
    time1 = random.uniform(1, 2)
    time.sleep(time1)   #模拟休眠时间:秒
    browser.find_element_by_id('kw').send_keys(data)    #模拟输入
    #time.sleep(random.uniform(1, 2))   #这里似乎不需要停顿
    browser.find_element_by_id('su').click()    #模拟点击
    time2 = random.uniform(2, 5)
    time.sleep(time2)
    #html = browser.find_element_by_xpath("html").text  这一句很神奇可以直接拿到文本
    html = browser.execute_script("return document.documentElement.outerHTML")  #这句话可以拿到html的源码
    time3 = random.uniform(1, 3)
    time.sleep(time3)
    if len(data) >= 10:
        view_len = 10
    else:
        view_len = len(data)
    print('查询内容:' + data[:view_len] + '\n'
          '模拟载入时间:' + str(round(time1, 2)) + 's\n'
          '模拟搜索时间:' + str(round(time2, 2)) + 's\n'
          '模拟观看时间:' + str(round(time3, 2)) + 's\n')
    this_url = browser.current_url
    browser.close()
    reg = r'<div class="c-abstract">(.*?)</div><div class="f13">'     ##百度html的开头:&nbsp;-&nbsp;</span> \\\\结尾:</div><div class=
    result_first = [i for i in re.findall(reg, html) if i != '']
    result_final = []
    for i in result_first:
        reg = r'<span(.*?)</span>'
        try:
            del_text = re.findall(reg, i)[0]
            text_new = i.replace('<span', '').replace('</span>', '').replace(del_text, '')
        except:
            text_new = i.replace('<span', '').replace('</span>', '')
        result_final.append(text_new)
    result = result_final + [this_url] + [data]
    return result

