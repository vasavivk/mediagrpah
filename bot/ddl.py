import os
import re
import subprocess
import requests
from pyrogram.types import Message
from bot.utils import manger


URLRx = re.compile(r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])")
nameRx = re.compile(r".+/(.+)")

def download_file(url):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
             
                f.write(chunk)
    return local_filename
    
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
        mediainfo_txt = subprocess.check_output(['mediainfo', ddl]).decode("utf-8")
        checkm = manger(mediainfo_txt)
        reply_msg.edit(f'**[{name}]({checkm})**',
                disable_web_page_preview=False)
    except Exception as e:
        print("Error:", str(e))
    finally:
        os.remove(f"{download_path}")

print("ddl module loaded", flush=True)
