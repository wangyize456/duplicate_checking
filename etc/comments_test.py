import win32com
from win32com.client import Dispatch
word = win32com.client.Dispatch('Word.Application')
word.Visible = 1
path = r'C:\Users\admin\Desktop\test_comments.docx'
doc = word.Documents.Open(FileName=path, Encoding='gbk')
# 主要关键的是这一句
l = ['1', '2', '3']
lt = '\n'.join(l)
find_t = r'据《战略性新兴产业分类（2018）》，美腾科技业务属'
word.Selection.Find.Execute(find_t)
doc.Comments.Add(Range=word.Selection.Range, Text=lt)

print(doc.paragraphs[0])