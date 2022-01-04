import re
# 书籍详情链接的规则
# <a class="nbg" href="https://book.douban.com/subject/35044046/" onclick=
findLink = re.compile(r'<a class="nbg" href="(.*?)"\s*onclick')  # 创建正则表达式对象，表示规则（字符串的模式）
# 书籍图片
findImgSrc = re.compile(r'<img class="" src="(.*?)"\s*width',)  # re.S 让换行符包含在字符中
# 书名
findBookName = re.compile(r'<a.*title="(.*?)"')
# 书名补充
findBookNameSupply = re.compile(r'<span style="font-size:12px;"> : (.*?)\s*</span')
# 书籍评分
findBookScore = re.compile(r'<span class="rating_nums">(.*)</span>')
# 找到评价人数
findJudgeAmount = re.compile('<span class="pl">\s*\((.*?)评价')

# 找到出版相关信息
findPublicationInfo = re.compile(r'<div class="pub">\s*(.*?)\s*</div>')
# 概况
findSummary = re.compile(r'<p>(.*)</p>')
