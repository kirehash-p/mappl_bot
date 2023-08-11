import data_operation, jst_time
import discord
from discord.ext import tasks
from logging import getLogger

logger = getLogger("Log").getChild("discord_bot")

def run_bot(TOKEN, CHANNEL_ID, jsonf, sheet_key):
    logger.debug("Executing run_bot...")
    # Googleスプレッドシートからリマインドする時間、何日後まで入力欄を設けるかの値を取得
    prefix = data_operation.get_data(jsonf, sheet_key)[1]
    notify_time, margin = prefix[4][1], int(prefix[5][1])

    # botを起動する前にGoogleスプレッドシートの表の整理
    data_operation.auto_arrange(jsonf, sheet_key, margin)

    client = discord.Client(intents=discord.Intents.all())
    # リマインドする時間になったかを60秒ごとに確認し、時間になったら通知を送信してスプレッドシートのひょうを整理する。
    @tasks.loop(seconds=60)
    async def loop():
        if jst_time.now_minute() == notify_time:
            announce_channel = (client.get_channel(CHANNEL_ID) or await client.fetch_channel(CHANNEL_ID))
            await send_schedule(announce_channel, jsonf, sheet_key, jst_time.now_day())
            data_operation.auto_arrange(jsonf, sheet_key, margin)
    
    # Bot起動時に行う処理。BotのステータスをSystem onlineにし、上のtasks.loopを開始する。
    @client.event
    async def on_ready():
        logger.debug("Bot started")
        await client.change_presence(activity=discord.Game(name="System online"))
        loop.start()
    
    # /scheduleから始まるメッセージを取得し、実行する。
    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.content[:9] == '/schedule':
            try:
                await client.change_presence(activity=discord.Game(name="Executing search query..."))
                command = message.content
                if command == '/schedule':
                     command += " " + jst_time.now_day()
                logger.debug(f"command claimed: {message.content}")
                reply_channel = message.channel
                await send_schedule(reply_channel, jsonf, sheet_key, day=command.split(" ")[-1])
                await client.change_presence(activity=discord.Game(name="System online"))
            except Exception as e:
                logger.warning(e)
                await send_error(reply_channel, m="Undefined argument")

    client.run(TOKEN)
    logger.info("run_bot executed.")
    return

# botが送信するテキストを作成する。
def send_info(information, day, prefix):
    logger.debug("Executing send_info...")
    # informationとprefixからbotが送信するメッセージのテキストを作成する。作業部屋予告、イベント告知、メッセージの順。
    if any(information[0][1]):
            content = prefix[1][1]
            for i in range(len(information[0][1])):
                if information[0][1][i]:
                    content += "\n・**"+information[0][0][i]+"  "+information[0][1][i]+"**   "+information[0][2][i]
    else:
            content = prefix[1][2]
    content += "\n"
    if any(information[1][0]):
            content += prefix[2][1]
            for i in range(len(information[1][0])):
                content += "\n・**"+information[1][0][i]+"  "+information[1][1][i]+"**   "+information[1][2][i]
    else:
            content += prefix[2][2]
    if information[2][0]:
          content += "\n"+prefix[3][1] +"\n"+information[2][0]
    elif prefix[3][2]:
          content += "\n"+prefix[3][2]

    embed = discord.Embed(
        title=day,
        color=0x00ff00,
        description=content
    )
    logger.debug("send_info executed.")
    return embed

# 指定されたチャンネルに指定された日時の予定を投稿する。
async def send_schedule(channel, jsonf, sheet_key, day):
    logger.debug("Executing send_schedule...")
    sheet_data, prefix = data_operation.get_data(jsonf, sheet_key)
    information = data_operation.search(sheet_data, day)
    if information != None:
        await channel.send(embed=send_info(information, day, prefix=prefix))
    else:
        await send_error(channel, m="data not found")
    logger.debug("send_schedule executed.")
    return

# エラーが起きたとき呼び出され、指定されたチャンネルにエラーの内容を投稿する。
async def send_error(channel, m):
    logger.debug("Executing send_error...")
    embed = discord.Embed(
         title="エラーにより、正常に処理されませんでした!",
         color=0xff6347,
         description=f"エラー文:{m}"
    )
    await channel.send(embed=embed)
    logger.debug("send_error executed.")
    return