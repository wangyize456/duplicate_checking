import requests
main_url = r'https://www.baidu.com/'
response = requests.get(main_url)
response.encoding = 'utf-8'
print(response.text)