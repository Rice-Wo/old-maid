import json
import requests
import discord
import logging.config
from .config import config















def embed_text_adjustment(input):
    max_line_length = 15

    # 初始化結果列表
    result = []
    current_line = []

    # 遍歷原始列表
    for name in input:
        # 檢查將當前名字添加到當前行是否超出最大字數
        if len(', '.join(current_line + [name])) <= max_line_length:
            current_line.append(name)
        else:
            # 如果超出最大字數，將當前行添加到結果列表中，並初始化新的當前行
            result.append(', '.join(current_line))
            current_line = [name]

    # 將剩餘的當前行添加到結果列表
    result.append(', '.join(current_line))

    # 將結果列表中的元素使用'\n'分隔成最終字符串
    final_result = '\n'.join(result)

    # 輸出結果
    return final_result