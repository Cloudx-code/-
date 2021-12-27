import re
# 书籍详情链接的规则
# <a class="nbg" href="https://book.douban.com/subject/35044046/" onclick=
findLink = re.compile(r'<a class="nbg" href="(.*?)" onclick')  # 创建正则表达式对象，表示规则（字符串的模式）
# 书籍图片
findImgSrc = re.compile(r'<img src="(.*?)"', re.S)  # re.S 让换行符包含在字符中
# 书名
findTitle = re.compile(r'<a.*title="(.*?)"')
# 书籍评分
findRating = re.compile(r'<span class="rating_nums">(.*)</span>')
# 找到评价人数
findJudge = re.compile(r'<span class="pl">\(\n                    (.*?)人评价',re.S)
# 英文名：<span style="font-size:12px;">Nineteen Eighty-Four</span>
findEnName = re.compile(r'<span style="font-size:12px;">(.*?)</span>')
# 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 找到书籍的相关内容
findBd = re.compile(r'<p class="pl">(.*?)</p>', re.S)