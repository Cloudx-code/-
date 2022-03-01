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
    # # 生活
    # title = "生活"
    # tags = ["爱情","成长","生活","心理","女性","旅行","励志","教育",
    #         "摄影","职场","美食","游记","灵修","健康","情感","人际关系",
    #         "两性","养生","手工","家居","自助游"]
    # title = "文化"
    # tags =["历史","心理学","哲学","社会学","传记","文化","艺术","社会",
    #         "政治","设计","政治学","宗教","建筑","电影","中国历史","数学",
    #         "回忆录","思想","人物传记","艺术史","国学","人文","音乐","绘画",
    #        "西方哲学","戏剧","近代史","二战","军事","佛教","考古","自由主义",
    #        "美术"]
    # title = "流行"
    # tags =["漫画","推理","绘本","悬疑","东野圭吾","青春","科幻","言情",
    #         "推理小说","奇幻","武侠","日本漫画","耽美","科幻小说","网络小说","三毛",
    #         "韩寒","亦舒","阿加莎·克里斯蒂","金庸","穿越","安妮宝贝","魔幻","轻小说",
    #        "郭敬明","青春文学","几米","J.K.罗琳","幾米","张小娴","校园","古龙",
    #        "高木直子","沧月","余秋雨","张悦然"]
    # title = "文学"
    # tags =["小说","文学","外国文学","经典","中国文学","随笔","日本文学","散文",
    #         "村上春树","诗歌","童话","名著","儿童文学","古典文学","余华","王小波",
    #         "当代文学","杂文","张爱玲","外国名著","鲁迅","钱钟书","诗词","茨威格",
    #        "米兰·昆德拉","杜拉斯","港台"]
    title = "文学"
    tags = ["张爱玲", "外国名著", "鲁迅", "钱钟书", "诗词", "茨威格",
            "米兰·昆德拉", "杜拉斯", "港台"]







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