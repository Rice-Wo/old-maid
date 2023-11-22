from pydantic_settings import BaseSettings
from pydantic import validator
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
    version: str = None  # 預設為 None，表示尚未初始化
    admin_server: int = 0
    online_message: int = 0


    @classmethod
    def get_version(cls):
        response = requests.get("https://api.github.com/repos/Rice-Wo/Rice-Wo-maid/releases/latest")
        latest_release = response.json()

        if response.status_code == 200 and not latest_release.get("prerelease"):
            return latest_release["tag_name"]
        return None

    @validator('version', pre=True, always=True)
    def set_version(cls, v):
        if v is None:
            return cls.get_version()
        return v


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
config = Config()  