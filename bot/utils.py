from telegraph import Telegraph
import re
import subprocess
import requests
from bs4 import BeautifulSoup

def katbin_paste(text: str) -> str:
    """
    Paste the text on katb.in website.
    """
    
    katbin_url = "https://katb.in"
    
    # Send a GET request to katb.in
    response = requests.get(katbin_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the CSRF token
    csrf_token = soup.find("input", {"name": "_csrf_token"}).get("value")
    
    try:
        # Send a POST request to paste the text
        paste_post = requests.post(
            katbin_url,
            data={"_csrf_token": csrf_token, "paste[content]": text},
            allow_redirects=False,
        )
        
        # Construct the output URL
        output_url = f"{katbin_url}{paste_post.headers['location']}"
        
        return output_url
    
    except Exception as e:
        return f"Something went wrong while pasting text in katb.in: {str(e)}"

def create_telegraph_page(html_text, title):
    telegraph = Telegraph(access_token="df37be0d94ded1eff095b0c9d5e43268dcf039f597e110433945b83f5aac", domain="graph.org")
    
    response = telegraph.create_page(f'MediaInfo of {title}',author_name='MediaInfoBot', author_url="https://t.me/applemuiscdlBot", html_content=html_text)
    return response["url"]

def format_sections(input_text):
    sections = re.split(r'\n(?=(?:General|Audio|Video|Text))', input_text.strip())

    formatted_output = ''
    for section in sections:
        lines = section.strip().split('\n')
        header = lines[0]
        content = '\n'.join(lines[1:])
        formatted_output += f"<h4>{header}</h4>\n<pre>\n"
        formatted_output += content
        formatted_output += "\n</pre>\n"

    return formatted_output 


def manger(raw_info, title):
    format_info= format_sections(raw_info)
    pre_link= create_telegraph_page(format_info, title)
    return pre_link
    



def get_soxcap(file_path,mime):
    mime_type = mime
    mediainfo_cmd = (f'mediainfo --Output="Audio;%Format% %Compression_Mode% | {mime_type}\\n\\n'
                     'Duration: %Duration/String%\\n'
                     'Stream: %StreamSize/String%\\n'
                     '%BitRate_Mode% %BitRate/String%, %BitDepth/String% %SamplingRate/String%, %Channel(s)% channels" '
                     f'"{file_path}"')
    return subprocess.check_output(mediainfo_cmd, shell=True, text=True)
