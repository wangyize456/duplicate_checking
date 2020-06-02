#该脚本主要用于doc文档利用百度搜索引擎自动查寻并返回类似文本进行高亮批注
#只能读取[.docx]文件，不能读取[.doc]文件
from docx import Document
import re
import os
from selenium.webdriver import ChromeOptions, Chrome
import time
import random

# #此处在r'xxxx'中输入绝对路径
# path = r'C:\Users\admin\Desktop\未完整版：美腾科技所处行业分析报告（菁亿投顾-2020-05-25).docx'
# url = r'https://www.baidu.com/'
# duplicate_rate = 0.5

def main_app(path, duplicate_rate, granularity):
    path = path
    url = r'https://www.baidu.com/'
    duplicate_rate = duplicate_rate
    # 1.拿到word原始数据
    #首先提取docx文本内容并去掉标题和空白
    def get_docx_paragraph(path):
        paragraph = []
        document = Document(path)
        for i in document.paragraphs:
            if i.style.name != 'Normal':    #研究表明str对比区分大小写
                pass
            else:
                paragraph.append(i.text)    #有陷阱,空list是nonetype,nonetype不能append所以不能用赋值的方法
        paragraph = [i for i in paragraph if i != '']   #列表生成式去空集比较简单
        return paragraph

    # 2.取得正文(剔除不需要搜索的部分)
    def paragraph_data_clean(paragraph_data):
        r_paragraph = []
        for i in paragraph_data:
            pattern = '。|；'
            for n in re.split(pattern, i):  #对句号和分号进行分节
                r_paragraph.append(n)
        r_paragraph = [i for i in r_paragraph if i != '' and len(i) > granularity]   #继续使用列表生成式去空元/百度的查询限制在38个汉字以内
        return r_paragraph

    # 3.将数据丢给百度搜索并返回结果
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
        if len(result_first) == 0:
            result = ['百度无内容'] + [this_url] + [data]
            return result
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

    def round_new(a, b=2):
        return round(a, b)

    #直接拿到搜索的结果与test稍有不同
    def analyz_result_dup(result_search, duplicate_rate):
        reg = r'<em>(.*?)</em>'
        dup_rate = duplicate_rate * 100
        dup_rate_list = []
        for i in result_search[:-2]:
            all_len = len(i)
            dup_list = re.findall(reg, i)
            dup_str = ''.join(dup_list)
            dup_len = len(dup_str)
            dup_rate_list.append(dup_len / (all_len - len(dup_list) * 9) * 100)
        if max(dup_rate_list) < dup_rate:
            rate_result = ', '.join(list(map(str, list(map(round_new, dup_rate_list)))))
            result = [rate_result, '未见异常']
        else:
            rate_result = str(round(max(dup_rate_list), 2)) + '%'
            result = [result_search[-2][:-2], result_search[-1], rate_result]
        return result

    def folder_check(folder_path):
        boolean_value = os.path.exists(folder_path)
        if not boolean_value:
            os.makedirs(folder_path)
        return

    def file_check(folder_path, filename):
        file_path = folder_path + '\\' + filename
        boolean_value = os.path.exists(file_path)
        return boolean_value

    # 0.定义log路径及文件夹检查
    folder_path = path[:-5] + r' - 查重log'
    folder_check(folder_path)

    # 1.拿到word原始数据
    paragraph = get_docx_paragraph(path)

    # 2.取得正文(剔除不需要搜索的部分)
    r_paragraph = paragraph_data_clean(paragraph)
    fn = open(folder_path + r'\0.r_paragraph.txt', 'w', encoding='utf-8')
    fn.write('\n'.join(r_paragraph))
    fn.close()

    # 3.搜索的数据保存至log_search_data
    n = 0
    folder_path_search = folder_path + '\search_data'
    folder_check(folder_path_search)
    file_total = len(r_paragraph)
    for data in r_paragraph:
        # 断点续查
        n = n + 1
        filename = str(n) + '.txt'
        if file_check(folder_path_search, filename):
            print('载入数据中')
            fn = open(folder_path_search + '\\' + filename, 'r', encoding='utf-8')
            fn_data = fn.readlines()[-1]
            fn.close()
            if data == fn_data:
                print('本条数据效验完成')
            else:
                result_search = []
                error_count = -2
                while 1:
                    error_count = error_count + 1
                    if error_count > 0:
                        print(data + '\n'
                                     '搜索结果错误:第' + str(error_count) + '次')
                    if len(result_search) < 3:  # 可分析内容小于3个就没什么好说的了说明是网络问题
                        time.sleep(5)
                        result_search = get_search_result(url, data)  # ***重要***//get_search_result//***重要***
                    else:
                        break
                fn = open(folder_path_search + '\\' + filename, 'w', encoding='utf-8')
                fn.write('\n'.join(result_search))
                fn.close()
                print('采集数据中')
        else:
            result_search = []
            error_count = -2
            while 1:
                error_count = error_count + 1
                if error_count > 0:
                    print(data + '\n'
                        '搜索结果错误:第' + str(error_count) + '次')
                if len(result_search) < 3:  #可分析内容小于3个就没什么好说的了说明是网络问题
                    time.sleep(5)
                    result_search = get_search_result(url, data)    # ***重要***//get_search_result//***重要***
                else:
                    break
            fn = open(folder_path_search + '\\' + filename, 'w', encoding='utf-8')
            fn.write('\n'.join(result_search))
            fn.close()
            print('采集数据中')
        print('正在执行搜索模块(这只是1/2):\n'
        '已处理完第:' + str(n) + '个数据\n'
        '共' + str(file_total) +'个数据\n'
        '进度为:' + str(round_new(n / file_total * 100, 2)) + '%\n'
        '````````````````````````````我是一条分割线`````````````````````````````')

    # 4.提取search_result进行分析
    search_file_list = list(os.walk(folder_path_search))[0][2]
    n = 0
    for i in search_file_list:
        n = n + 1
        fn = open(folder_path_search + '\\' + i, 'r', encoding='utf-8')
        result_search = fn.readlines()
        result = analyz_result_dup(result_search, duplicate_rate)
        fn = open(folder_path + '\\' + i, 'w', encoding='utf-8')
        fn.write('以下为结果输出:\n')
        fn.write('\n'.join(result))
        fn.close()
        print('正在执行分析模块(这是2/2):\n'
        '已处理完第:' + str(n) + '个数据\n'
        '共' + str(file_total) +'个数据\n'
        '进度为:' + str(round_new(n / file_total * 100, 2)) + '%\n'
        '````````````````````````````我是一条分割线`````````````````````````````')

    return print('分析done!')