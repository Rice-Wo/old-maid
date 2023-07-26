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

def writeJson(file, item): #JSON寫入
    file_path = os.path.join(main_script_directory, file + '.json')
    with open(file_path, "w+") as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=4))


def readJson(file): #JSON讀取
    file_path = os.path.join(main_script_directory, file + '.json')
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data


async def get_data(location): #取得天氣預報資料
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


class weather_select(discord.ui.View): #天氣選單
  SelectOption = discord.SelectOption
  @discord.ui.select(
    placeholder="地區",
    options=[
    SelectOption(label="宜蘭縣", description='宜蘭縣預報'),
    SelectOption(label="花蓮縣", description='花蓮縣預報'),
    SelectOption(label="臺東縣", description='臺東縣預報'),
    SelectOption(label="澎湖縣", description='澎湖縣預報'),
    SelectOption(label="金門縣", description='金門縣預報'),
    SelectOption(label="連江縣", description='連江縣預報'),
    SelectOption(label="臺北市", description='臺北市預報'),
    SelectOption(label="新北市", description='新北市預報'),
    SelectOption(label="桃園市", description='桃園市預報'),
    SelectOption(label="臺中市", description='臺中市預報'),
    SelectOption(label="臺南市", description='臺南市預報'),
    SelectOption(label="高雄市", description='高雄市預報'),
    SelectOption(label="基隆市", description='基隆市預報'),
    SelectOption(label="新竹縣", description='新竹縣預報'),
    SelectOption(label="新竹市", description='新竹市預報'),
    SelectOption(label="苗栗縣", description='苗栗縣預報'),
    SelectOption(label="彰化縣", description='彰化縣預報'),
    SelectOption(label="南投縣", description='南投縣預報'),
    SelectOption(label="雲林縣", description='雲林縣預報'),
    SelectOption(label="嘉義縣", description='嘉義縣預報'),
    SelectOption(label="嘉義市", description='嘉義市預報'),
    SelectOption(label="屏東縣", description='屏東縣預報')          
  ],
  custom_id='weather'
  )
  async def select_callback(self, select, interaction):
    data = await get_data(select.values[0]) 
    await interaction.response.edit_message(embed=data, view=weather_select())


def changeLog(): #取得更新內容
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

def chat_update(url):
    destination = "chat.json"
    try:
        response = requests.get(url)
        with open(destination, 'w', encoding='utf-8') as file:
            file.write(response.text)
        logger.info("成功下載並替換 JSON 檔案")
    except requests.exceptions.RequestException as e:
        logger.error("下載檔案時發生錯誤: %s", str(e))
    except Exception as e:
        logger.error("處理檔案時發生錯誤: %s", str(e))

def prerelease(): #取得更新內容
    response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases")
    release = response.json()
    latest_release = release[0]

    if response.status_code == 200:
        if latest_release.get("prerelease"):
            changelog = latest_release["body"]
            version = latest_release["tag_name"]

            output = f'# {version} \n{changelog}'
    else:
        print("无法获取最新发布信息。")
    return output