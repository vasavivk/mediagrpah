import json
import os
import re
import subprocess

from pyrogram import Client
from pyrogram.types import Message

from utils import *

def tgInfo(client: Client, msg: Message):
    print("processing TG", flush=True)
    message = msg.reply_to_message
    print("ok")
    if message.media.value == "video":
        media = message.video
    elif message.media.value == "audio":
        media = message.audio
    elif message.media.value == "document":
        media = message.document
    elif message.media.value == "voice":
        media = message.voice
    
    else:
        print("This media type is not supported", flush=True)
        raise Exception("`This media type is not supported`")
    print('done')
    mime = media.mime_type
    fileName = media.file_name
    size = media.file_size

    print(fileName, size, flush=True)

    if media == 'document':
        if 'video' not in mime and 'audio' not in mime and 'image' not in mime:
            print("Makes no sense", flush=True)
            raise Exception("`This file makes no sense to me.`")

    if int(size) <= 50000000:
        message.download(os.path.join(os.getcwd(), fileName))

    else:
        for chunk in client.stream_media(message, limit=5):
            # save these chunks to a file
            with open(fileName, 'ab') as f:
                f.write(chunk)

    mediainfo_txt = subprocess.check_output(
        ['mediainfo', fileName]).decode("utf-8")

    print("done! mediainfo")
    try:
        checkm = manger(mediainfo_txt)
        msg.reply_text(f"[{custom_text}]({link_url})", disable_web_page_preview=False)
        
    except:
        message.reply_text(
            "Something bad occurred particularly with this file.")
        print("Something bad occurred for tg file", flush=True)
    finally:
        os.remove(fileName)


print("TG file module loaded", flush=True)
