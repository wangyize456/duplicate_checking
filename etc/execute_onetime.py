from learn_python_docx import main_app
import os
import win32com
from win32com.client import Dispatch
import time

path = r'C:\Users\admin\Desktop\跃通数控IPO-第六节、业务和技术部分章节（菁亿投顾 2020-5-20）.docx'
duplicate_rate = 0.5

def analyze_result(path, duplicate_rate):
    main_app(path, duplicate_rate)
    folder_path = path[:-5] + r' - 查重log'
    all_file_num = len(list(os.walk(folder_path))[0][2]) - 1
    result = []
    result_list= []
    for i in range(1, all_file_num + 1):
        file = open(folder_path + '\\' + str(i) + '.txt', 'r', encoding='utf-8')
        txt_data = file.readlines()
        if txt_data[-1] == '未见异常':
            pass
        else:
            txt_data_new = []
            for i in txt_data[1:]:
                txt_data_new.append(i.replace('\n', ''))
            result.append(txt_data_new)
            result_list.append(str(i))
    print('当重复率为:' + str(duplicate_rate * 100) + '%')
    print('共有:' + str(len(result)) + '个异常项目\n')
    if result_list:
        print(', '.join(result_list))
    return result

result = analyze_result(path, duplicate_rate)
word = win32com.client.Dispatch('Word.Application')
for analyze_paragraph in result:
    word.Visible = 0
    docx = word.Documents.Open(FileName=path, Encoding='gbk')
    normal_paragraph = '\n'.join(analyze_paragraph[::2])
    text_find = analyze_paragraph[1]
    word.Selection.Find.Execute(text_find)
    docx.Comments.Add(Range=word.Selection.Range, Text=normal_paragraph)
    word.Documents.Close()
# word.Visible = 1


# 1.开始加批注
# # 4.开始合并文件
# pass_result = [i for i in result_list if i != ['未见异常']]
# # 5.开始与结果文件产生关联并开始加批注
# word = win32com.client.Dispatch('Word.Application')
# word.Visible = 0
# docx = word.Documents.Open(FileName=path, Encoding='gbk')
# for analyze_paragraph in pass_result:
#     normal_paragraph = '\n'.join(analyze_paragraph[::2])
#     text_find = analyze_paragraph[1]
#     word.Selection.Find.Execute(text_find)
#     docx.Comments.Add(Range=word.Selection.Range, Text=normal_paragraph)
# word.Visible = 1