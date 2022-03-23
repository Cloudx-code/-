# 注意事项！！！这个1.csv可以直接通过Excel编辑（gbk编码），但是其他的会出现乱码问题。（utf-8编码）

import json
import csv

def getCsv(savepath:str):
    res = []
    with open(savepath, 'r',encoding='utf-8') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        res.append(headers)
        for row in f_csv:
            res.append(row)
    return res

# dataType:train,dev,test
def handleAllDiologue(dataType:str):
    dialogueData = getCsv("../bookData/语料/"+dataType+".csv")
    dialogueAllLists = []
    dialogueDict = {}
    dialogueMessages = []
    for singleDialogue in dialogueData:
        # 判断对话是否结束。赋值name，结束后开启新一轮
        if "&" in singleDialogue[0]:
            # 应该还有个赋值添加的操作,将上轮的Message填入字典
            print(dialogueMessages)
            dialogueDict["messages"] = dialogueMessages
            # 赋值name
            dislogueName = singleDialogue[0].split('&')[1]
            dialogueDict["name"] = dislogueName
            print(dialogueDict)
            print(111)
            # 清空上一轮对话的Dic以及Message
            dialogueAllLists.append(dialogueDict)
            dialogueDict = {}
            dialogueMessages = []
        else:
            # 这里将单轮对话处理成字典格式：
            # singleDialogue=['用户2:看过啊，这是我认为中国近代最受欢迎的科幻小说之一了，豆瓣上这本小说的评分高达9.4分。', '"三体","标签","科幻"', '"三体","标签","小说"', '"三体","信息","豆瓣评分9.4分"', '']
            sentenceDict = {}
            attrsList = []
            for sentence in singleDialogue:
                # dialogueMessages:List的每一个元素是一个Dict,Dict中包含attrs:List和message:str
                if sentence == "":
                    continue
                if sentence.startswith("用户"):
                    # 处理message
                    sentenceDict["message"]=sentence[4:]
                else:
                    # 处理attrs,attrs中的每一个元素又是一个Dict(attrname:relation,attrvalue:tail Entity,name:head Entity)
                    attrsValue = sentence.split(",")
                    print("\n\n",sentence)
                    attrsDict = {}
                    attrsDict["attrname"]=attrsValue[1]
                    attrsDict["attrvalue"]=attrsValue[2]
                    attrsDict["name"]=attrsValue[0]
                    attrsList.append(attrsDict)
            if sentenceDict:
                if len(attrsList)!=0:
                    sentenceDict["attrs"]=attrsList
                dialogueMessages.append(sentenceDict)

    dialogueJson = json.dumps(dialogueAllLists, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    return dialogueJson

# 如果用1.csv的话需要改格式，好像不是utf-8的格式。
if __name__ == '__main__':
    # dataTypes = ["train","dev","test"]
    dataTypes = ["sentence"]
    for dataType in dataTypes:
        dialogueJson = handleAllDiologue(dataType)
        print('\n\n\n', dialogueJson)
        with open(dataType+".json", 'w', newline="", encoding='utf-8') as f:
            f.write(dialogueJson)
    print("存入成功!")




