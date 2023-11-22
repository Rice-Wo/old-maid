from pydantic import BaseSettings
import requests


def get_version(): #取得更新內容
    response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases/latest")
    latest_release = response.json()

    if response.status_code == 200:
        if not latest_release.get("prerelease"):
            version = latest_release["tag_name"]
    return version


class Config(BaseSettings):
    bot_token: str = ''
    weather_token: str = ''
    version: int = get_version()



    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
config = Config()  