import os
folder_path = r'C:\Users\admin\Desktop\查重log\search_data'
for i in list(os.walk(folder_path))[0][2]:
    file = open(folder_path + '\\' + i, 'r', encoding='utf-8')
    txt_data = file.readlines()
    file.close()
    file = open(folder_path + '\\' + i, 'w', encoding='utf-8')
    new_data = [i for i in txt_data if i != '\n']
    file.write(''.join(new_data))

print('done')
