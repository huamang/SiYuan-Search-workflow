import json
import sys
import requests


def fullTextSearchBlock(q):
    searchJson = {}
    searchJson["query"] = q
    searchJson["method"] = 0
    type = {}
    type["blockquote"] = True
    type["codeBlock"] = True
    type["document"] = True
    type["embedBlock"] = True
    type["heading"] = True
    type["htmlBlock"] = True
    type["list"] = True
    type["listItem"] = True
    type["mathBlock"] = True
    type["paragraph"] = True
    type["superBlock"] = True
    type["table"] = True
    searchJson["type"] = type
    searchJson["path"] = []
    searchJson["groupBy"] = 0
    searchJson["orderBy"] = 0
    
    data = json.dumps(searchJson)
    url = "http://127.0.0.1:6806/api/search/fullTextSearchBlock"
    res = requests.post(url, data)
    resJson = json.loads(res.text)
    return resJson

def parseRes(resJson):
    itemList = []
    uid = 1
    for block in resJson["data"]["blocks"]:
        item = {}
        item["uid"] = uid
        item["title"] = block["content"].replace("<mark>", "").replace("</mark>", "")[:50]
        item["subtitle"] = block["hPath"]
        item["arg"] = "siyuan://blocks/" + block["id"]
        itemList.append(item)
        uid += 1
    items = {}
    items["items"] = itemList
    items_json = json.dumps(items)
    sys.stdout.write(items_json)

def getRecentDocs():
    url = "http://127.0.0.1:6806/api/storage/getRecentDocs"
    res = requests.post(url, json={})
    resJson = json.loads(res.text)
    return resJson

def parseRecentDocs(resJson):
    itemList = []
    uid = 1
    for doc in resJson["data"]:
        item = {}
        item["uid"] = uid
        item["title"] = doc["title"]
        item["arg"] = "siyuan://blocks/" + doc["rootID"]
        itemList.append(item)
        uid += 1
    items = {}
    items["items"] = itemList
    items_json = json.dumps(items)
    sys.stdout.write(items_json)

def main():
    alfredQuery = str(sys.argv[1])
    if alfredQuery:
        resJson = fullTextSearchBlock(alfredQuery)
        parseRes(resJson)
    else:
        resJson = getRecentDocs()
        parseRecentDocs(resJson)


if __name__ == '__main__':
    main()
