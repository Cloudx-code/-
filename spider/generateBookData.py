from bookSpider import getBookDataByTag
from util.csvUtil import saveToCsv,addAuthorInfoToCsv,addBookLabelInfoToCsv,addPublisherToCsv


def main():
    bookHeaders = ("书籍详情链接", "图片链接", "书名", "书名简述", "评分", "评价数", "出版相关信息", "概况")
    # # 科技
    # title = "科技"
    # tags = ["科普","互联网","科学","编程","交互设计","算法","用户体验","web","交互","通信","UE","神经网络","UCD","程序"]
    # # 经管
    # title = "经管"
    # tags = ["经济学","管理","经济","商业","金融","投资","营销","理财","创业","股票","广告","企业史","策划"]
    # 生活
    title = "生活"
    tags = ["爱情","成长","生活","心理","女性","旅行","励志","教育",
            "摄影","职场","美食","游记","灵修","健康","情感","人际关系",
            "两性","养生","手工","家居","自助游"]
    tags = ["旅行","励志","教育",
            "摄影","职场","美食","游记","灵修","健康","情感","人际关系",
            "两性","养生","手工","家居","自助游"]



    for tag in tags:
        allBookData = getBookDataByTag(tag)
        loadPath = r"../bookData/"+title+"/book-list-" + tag+ ".csv"
        savePath = r"../bookData/"+title+"/book-list-" + tag+ ".csv"
        saveToCsv(allBookData,loadPath, bookHeaders )
        print(tag, "类型共", len(allBookData), "条数据全部存入成功")
        # 添加作者类型
        addAuthorInfoToCsv(loadPath=loadPath,savePath=savePath)
        print(tag, "类型增加作者列执行完毕")
        # 添加用户标签
        addBookLabelInfoToCsv(loadPath=loadPath, savePath=savePath)
        print(tag, "类型增加用户标签执行完毕")
        # 添加出版社
        addPublisherToCsv(loadPath=loadPath, savePath=savePath)
        print(tag, "类型增加出版社执行完毕")


if __name__ == '__main__':
    main()