import os
import sys

#from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message


from bot.sox import generateSpek
from bot.tgFile import tgInfo
from bot.ddl import ddlinfo
#load_dotenv()

#sys.path.append(os.path.join(os.getcwd(), 'services'))


helpMessage = """MediaInfo support the following services:
`• Telegram files
• Direct download links`

**Example:**
For MediaInfo:
`/info url`
`reply /info to file`

For audio Spek:
`reply /spek or /sox to audio`


Made by @thekvt🧪"""


'''
app = Client('botsession', api_id=os.getenv('api_id'),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token'))
'''
app = Client('botsession', api_id=25092986,
             api_hash='77b4dac018b806e625c3e9b1e1a65b6d',
             bot_token='6349129074:AAGSLe4O37msRykoOUP7BIzeUEJEdxS8B-U')

print("MediaInfo bot started!", flush=True)


@app.on_message(filters.text & filters.private)
def hello(client: Client, message: Message):

    if '/start' in message.text:
        message.reply("Send /help for more info.")
        return

    if '/help' in message.text:
        message.reply(helpMessage)
        return

    try:
        if "/sox" in message.text:
            message.reply("Processing your spectrogram request...")
            generateSpek(message)
            return

        elif "/info" in message.text:
            if message.reply_to_message:
                message.reply("Processing your Telegram file request...")
                tgInfo(client, message)
            elif len(message.text) > 10:
                message.reply("Processing your DDL request...")
                ddlinfo(message)
    except Exception as e:
        message.reply(f"`An error occured!`\n{e}")
        print(e, flush=True)
        return


app.run()
