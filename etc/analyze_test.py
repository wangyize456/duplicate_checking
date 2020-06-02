import re
from search_in_baidu import get_search_result
def round_new(a, b=2):
    return round(a, b)

def analyz_result_dup(result_search, duplicate_rate):
    reg = r'<em>(.*?)</em>'
    dup_rate = duplicate_rate
    dup_rate_list = []
    for i in result_search[:-2]:
        all_len = len(i)
        dup_list = re.findall(reg, i)
        dup_str = ''.join(dup_list)
        dup_len = len(dup_str)
        dup_rate_list.append(dup_len / (all_len - len(dup_list) * 9))
    if max(dup_rate_list) < dup_rate:
        result = ['未见异常']
    else:
        rate_result = str(round(max(dup_rate_list), 4))
        result = [result_search[-2], result_search[-1], rate_result[2:4] + '.' + rate_result[4:6] + '%']
    return result

url = r'https://www.baidu.com/'
date = r'业内人士指出，随着智慧矿山的建设，我国矿业将发生根本性变革'
duplicate_rate = 0.60
result_search = get_search_result(url, date)
analyz_result_dup(result_search, duplicate_rate)