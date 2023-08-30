import os
import re
import subprocess
import httpx
from pyrogram.types import Message
from bot.utils import manger
import requests

URLRx = re.compile(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
nameRx = re.compile(r".+/(.+)")

def ddlinfo(msg: Message):
    print("Got the DDL request!", flush=True)
    try:
        ddl = URLRx.search(msg.text).group(0)
        name = nameRx.search(ddl).group(1)
        gen_ddl_mediainfo(msg, ddl, name)
    except:
        print("Enter a valid ddl", flush=True) 
        raise Exception("`Something went wrong.\nPlease make sure you used a valid URL.`")

def gen_ddl_mediainfo(msg: Message, ddl: str, name: str):
    #reply_msg = message.reply_text("Generating Mediainfo, Please wait...")
    try:
        download_path = f"download/{name}"
        
        session = requests.Session()
        headers = {"user-agent":"Mozilla/5.0 (Linux; Android 12; 2201116PI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36"}

        response = session.get(url, stream=True, headers=headers, timeout=15)

        with open(download_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=10000000):
                file.write(chunk)

        mediainfo_txt = subprocess.check_output(['mediainfo', download_path]).decode("utf-8")
        checkm = manger(mediainfo_txt)
        reply_msg.edit(f'**[{name}]({checkm})**',
                disable_web_page_preview=False)
    except Exception as e:
        print("Error:", str(e))
    finally:
        os.remove(f"{download_path}")

print("ddl module loaded", flush=True)
