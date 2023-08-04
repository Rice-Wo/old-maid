# 稻禾專用女僕
稻禾專屬的Discord bot   

## todo list
- [ ] 21點
- [ ] 原神抽卡
- 待新增...

## 使用
1.  須建立chat.json作為自動回覆資料     
    格式為  
    ```json
    [
    {
        "user_input": [
        "A",
        "B"
        ],
        "bot_response": [
        "1",
        "2",
        ]
    }
    ]
    ```
    其中A、1、2皆為str  
    這樣就是當對話中含有A"或"B時，機器人會隨機回覆1或2
2.  須建立token.json放置Token等東西  
    格式為
    ```json
    {
    "online":12345678,
    "server":[12345678],
    "TOKEN":"ABCD1234",
    "CWB-TOKEN":"ABCD1234"
    }
    ```
    其中online為機器人上線通知的頻道id，server是測試用或是管理員專用指令的伺服器id  
    TOKEN為你的機器人TOKEN，CWB-TOKEN是你的中央氣象局TOKEN

## 貢獻

- [pycord API](https://github.com/Pycord-Development/pycord) : 作為Discord Bot 的框架   
- [jieba 結巴中文分詞](https://github.com/fxsjy/jieba) : 用於為句子分詞來達成取得句子關鍵字並回覆的功能