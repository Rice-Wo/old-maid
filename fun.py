import sys
import os
import json
import requests
import discord
import logging.config

#logging設定
with open('log_config.json', "r", encoding='utf-8') as f:
    log = json.load(f)
logging.config.dictConfig(log)
logger = logging.getLogger()


# 定義全域變數
main_script_path = os.path.abspath(sys.argv[0])
main_script_directory = os.path.dirname(main_script_path)

def writeJson(file, item):
    file_path = os.path.join(main_script_directory, file + '.json')
    with open(file_path, "w+") as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=4))

def readJson(file):
    file_path = os.path.join(main_script_directory, file + '.json')
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data

async def get_data(location):
  token = readJson('Token')
  url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
  params = {
      "Authorization": token['CWB-TOKEN'],
      "locationName":location      
  }

  response = requests.get(url, params=params)
  logging.info(f'中央氣象局資料狀態碼: {response.status_code}')

  if response.status_code == 200:
      # print(response.text)
      data = json.loads(response.text)
           
      locationName = data["records"]["location"][0]["locationName"]
      weather_elements = data["records"]["location"][0]["weatherElement"]
      start_time = weather_elements[0]["time"][0]["startTime"]
      end_time = weather_elements[0]["time"][0]["endTime"]
      weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
      rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
      min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
      comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
      max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

      embed=discord.Embed(title=f"{locationName} 的天氣預報", description=f"本預報時段為 {start_time} 到 {end_time}")
      embed.add_field(name="最高溫", value=f"{max_tem} °C" , inline=True)
      embed.add_field(name="最低溫", value=f"{min_tem} °C" , inline=True)
      embed.add_field(name="降雨機率", value=f"{rain_prob} %", inline=False)
      embed.add_field(name=weather_state, value=comfort, inline=True)
      embed.set_footer(text="以上資料由中央氣象局提供")
           
  else:
    logging.warning("Can't get data!")
    embed=discord.Embed(title=f"錯誤!", description=f"無法取得資料", color = 0xff0000)
    embed.set_footer(text="請稍後再試或是聯繫 稻禾Rice_Wo#3299")
  return embed


def changeLog():
    response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases/latest")
    latest_release = response.json()

    if response.status_code == 200:
        if not latest_release.get("prerelease"):
            changelog = latest_release["body"]
            version = latest_release["tag_name"]
            output = f'# {version} \n{changelog}'
        else:
            print("最新发布为预发布版本。")
    else:
        print("无法获取最新发布信息。")
    return output