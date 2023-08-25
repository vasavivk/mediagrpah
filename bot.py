import os
import sys

from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message


from services.sox import generateSpek
from services.tgFile import tgInfo

load_dotenv()

#sys.path.append(os.path.join(os.getcwd(), 'services'))


helpMessage = """MediaInfo support the following services:
`• Direct download links
• Telegram files`

**Example:**
For MediaInfo:
`/info url`
`reply /info to file`

For audio Spek:
`reply /spek to audio`



Made by @thekvt🧪"""



app = Client('botsession', api_id=os.getenv('api_id'),
             api_hash=os.getenv('api_hash'),
             bot_token=os.getenv('bot_token'))

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
        if "/spek" in message.text:
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
