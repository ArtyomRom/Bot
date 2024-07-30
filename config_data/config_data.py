from dataclasses import dataclass
from environs import Env
import os


@dataclass
class TgBot:
    token: str
    admin_id: list[int]


@dataclass
class Config:
    tg_bot: TgBot


# Создаем ф-цию, которая будем получать данные из .env
def load_config_data() -> Config:
    env = Env()
    env.read_env()
    return Config(TgBot(token=env('Token_telegram'),
                        admin_id=list(map(int, env('Admin_id')))))

