import re
import os
a = r'<div class="c-abstract"><span class=" newTimeFactor_before_abs m">3天前&nbsp;-&nbsp;</span>天津<em>美腾科技</em>有限公司是一家高新科技企业。<em>主要从事矿业</em>设备、人工智能产品<em>的研发</em>、设计、<em>制造和销售</em>。 15秒前 空街落叶 发布 3个回答 广告...</div><div class="f13">'
reg = r'<div class="c-abstract">(.*?)</div><div class="f13">'
r = re.findall(reg, a)[0]
reg = r'<span(.*?)</span>'
del_text = re.findall(reg, r)[0]
r_new = r.replace('<span', '').replace('</span>', '').replace(del_text, '')
print(r_new)
