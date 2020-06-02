import os
folder_path = r'C:\Users\admin\Desktop\查重log'
all_file_num = len(list(os.walk(folder_path))[0][2])
file = open(folder_path + '\\' + str(186) + '.txt', 'r', encoding='utf-8')
data = file.readlines()
file.close()
print(data)
print(file.readlines())