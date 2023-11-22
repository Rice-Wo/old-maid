from pydantic import BaseSettings


class Config(BaseSettings):
    bot_token:str = ''
    