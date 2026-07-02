import discord
from discord.ext import tasks
from datetime import datetime
from zoneinfo import ZoneInfo
import os
import random

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

TARGET_DATE = datetime(2027, 1, 16, tzinfo=ZoneInfo("Asia/Tokyo"))

MESSAGES = [
    "知は力なり",
    "早起きだね",
    "ほどほどにいこう",
    "お菓子食べた？"
]

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)


async def send_countdown():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        return

    # Botが過去に送ったカウントダウンメッセージを削除
    async for message in channel.history(limit=50):
        if (
            message.author == client.user
            and "共通テストまであと" in message.content
        ):
            try:
                await message.delete()
            except:
                pass

    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    days_left = (TARGET_DATE.date() - now.date()).days

    if days_left > 0:
        cheer = random.choice(MESSAGES)
        text = (
            f"📚 **共通テストまであと {days_left} 日！**\n\n"
            f"🌅 おはよう！\n"
            f"💡 **今日の一言:** {cheer}\n\n"
            f"📅 試験日：2027年1月16日"
        )
    elif days_left == 0:
        text = (
            "🎉 **今日は共通テスト本番！**\n\n"
            "ここまでまじで頑張ったね。\n"
            "落ち着いて、自分の力を信じていこう！✨"
        )
    else:
        text = "🎓 共通テストは終了しました！お疲れさまでした！"

    await channel.send(text)


@tasks.loop(minutes=1)
async def scheduler():
    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    if now.hour == 5 and now.minute == 0:
        await send_countdown()


@client.event
async def on_ready():
    print(f"ログイン成功: {client.user}")
    scheduler.start()


client.run(TOKEN)
