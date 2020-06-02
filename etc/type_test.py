#该脚本主要用于doc文档利用百度搜索引擎自动查寻并返回类似文本进行高亮批注
#只能读取[.docx]文件，不能读取[.doc]文件
from docx import Document
#此处在r'xxxx'中输入绝对路径
path = r'C:\Users\admin\Desktop\未完整版：美腾科技所处行业分析报告（菁亿投顾-2020-05-25).docx'

document = Document(path)
for i in document.paragraphs:
    print(i.text)
    print(i.style.name)     #突破性进展
