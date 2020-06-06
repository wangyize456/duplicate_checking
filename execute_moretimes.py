import os
import shutil
from learn_python_docx import main_app
import win32com
from win32com.client import Dispatch, DispatchEx
import time

# 1.开始执行
def analyze_result(path, duplicate_rate, granularity):
    main_app(path, duplicate_rate, granularity)
    folder_path = path[:-5] + r' - 查重log'
    all_file_num = len(list(os.walk(folder_path))[0][2]) - 1
    result = []
    result_output = []
    result_final = []
    for i in range(1, all_file_num + 1):
        file = open(folder_path + '\\' + str(i) + '.txt', 'r', encoding='utf-8')
        txt_data = file.readlines()
        if txt_data[-1] == '未见异常':
            pass
        else:
            result_new = []
            for i in txt_data[1:]:
                result_new.append(i.replace('\n', ''))
            result.append(result_new)
    result_output.append('当重复率为:' + str(duplicate_rate * 100) + '%')
    result_output.append('共有:' + str(len(result)) + '个异常项目\n')
    result_final.append(result)
    result_final.append(result_output)
    return result_final

path = os.getcwd() + r'\etc\result_file\【定稿版本】跃通数控IPO招股书-第六节-业务与技术（2020-6-6）.docx'
duplicate_rate_list = [0.3, 0.4, 0.5, 0.6, 0.7]
granularity = 25

l = []
path_result_output = path[:-5] + r' - 查重log\result_output_file'
# 文件夹检查
if os.path.exists(path_result_output):
    shutil.rmtree(path_result_output)
    os.makedirs(path_result_output)
else:
    os.makedirs(path_result_output)
# 开始计算并输出结果
for duplicate_rate in duplicate_rate_list:
    result_final = analyze_result(path, duplicate_rate, granularity)
    l.append('\n'.join(result_final[1]))
    path_each = path_result_output + '\重复率为【' + str(duplicate_rate * 100) + '%】版本.docx'
    shutil.copy(path, path_each)
    word = win32com.client.DispatchEx('Word.Application')
    docx = word.Documents.Open(FileName=path_each, Encoding='gbk')
    for analyze_paragraph in result_final[0]:
        word.Visible = 0
        word.DisplayAlerts = 0
        normal_paragraph = '\n'.join(analyze_paragraph[::2])
        text_find = analyze_paragraph[1][:30]
        s = word.Selection
        s.Start = 0
        s.End = 0
        s.Find.Execute(text_find)
        docx.Comments.Add(Range=s.Range, Text=normal_paragraph)
    docx.Close()
    word.Quit()

print('\n'.join(l))