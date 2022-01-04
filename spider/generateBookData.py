from bookSpider import getBookDataByTag
from util.csvUtil import saveToCsv,addAuthorInfoToCsv,addBookTypeInfoToCsv


def main():
    bookHeaders = ("书籍详情链接", "图片链接", "书名", "书名简述", "评分", "评价数", "出版相关信息", "概况")
    # 科技
    tags = ["科普","互联网","科学","编程","交互设计","算法","用户体验","web","交互","通信","UE","神经网络","UCD","程序"]


    for tag in tags:
        allBookData = getBookDataByTag(tag)
        loadPath = r"../bookData/科技/book-list-" + tag+ ".csv"
        savePath = r"../bookData/科技/book-list-" + tag+ ".csv"
        saveToCsv(allBookData,loadPath, bookHeaders )
        print(tag, "类型共", len(allBookData), "条数据全部存入成功")
        # 添加作者类型
        addAuthorInfoToCsv(loadPath=loadPath,savePath=savePath)
        print(tag, "类型增加作者列执行完毕")
        addBookTypeInfoToCsv(loadPath=loadPath,savePath=savePath)
        print(tag, "类型增加用户标签执行完毕")


if __name__ == '__main__':
    main()