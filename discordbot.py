from discord.ext import commands
import os
import traceback
from datetime import datetime
from discord.ext import tasks

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

channel_id =  os.environ['CHANNEL_ID']#チャンネルID

#投稿する日時
dateTimeList = [
'03/25 02:48',
'07/30 00:00',
'05/18 00:00',
'04/24 00:00',
'05/19 00:00',
'05/17 00:00',
'10/13 00:00',
'06/15 00:00'
]

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    
# 指定時間に走る処理
@bot.event
async def SendMessage():
    channel = client.get_channel(channel_id)
    await channel.send('@everyone\n誕生日おめでとうなんよぉ～\nびっくりした？？？')


# 30秒に一回ループ
@tasks.loop(seconds=30)
async def time_check():
    sleepTime = 0
    # 現在の時刻
    now = datetime.now().strftime('%m/%d %H:%M')
    if now in dateTimeList :
        print(now)
        await SendMessage()
        #該当時間だった場合は２重に投稿しないよう３０秒余計に待機
        await asyncio.sleep(30)

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 使用できるコマンド一覧
    if message.content == '!helpTana':
        await message.channel.send('使用できるコマンドはないんよぉ～')

#ループ処理
time_check.start()    


bot.run(token)
