import discord_bot, data_operation
import os, sys
from logging import getLogger, StreamHandler, DEBUG, Formatter, FileHandler

# ログ周りの設定
logger = getLogger('Log')
handler = StreamHandler()
logger.setLevel(DEBUG)
handler.setLevel(DEBUG)
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
fh = FileHandler(filename='botlog.txt')
fh.setLevel(DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)


# 定数の宣言
try:
    TOKEN = os.environ('BOT_TOKEN')
    CHANNEL_ID = os.environ('CHANNEL_ID')
    jsonf = "credential.json"
    sheet_key = os.environ('SHEET_KEY')
    logger.info("Variable set.")
except Exception as e:
    logger.error("Variable not found.")
    logger.error(e)
    sys.exit(1)

logger.info("System started!")
discord_bot.run_bot(TOKEN, CHANNEL_ID, jsonf, sheet_key)