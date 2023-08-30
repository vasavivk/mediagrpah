from telegraph import Telegraph
import re
import subprocess

def create_telegraph_page(html_text):
    telegraph = Telegraph(access_token="df37be0d94ded1eff095b0c9d5e43268dcf039f597e110433945b83f5aac", domain="graph.org")
    
    response = telegraph.create_page('MediaInfo',author_name='MediaInfoBot', author_url="https://telegram.dog/applemuiscdlBot, html_content=html_text)
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


def manger(raw_info):
    format_info= format_sections(raw_info)
    pre_link= create_telegraph_page(format_info)
    return pre_link
    



def get_soxcap(file_path,mime):
    mime_type = mime
    mediainfo_cmd = (f'mediainfo --Output="Audio;%Format% %Compression_Mode% | {mime_type}\\n\\n'
                     'Duration: %Duration/String%\\n'
                     'Stream: %StreamSize/String%\\n'
                     '%BitRate_Mode% %BitRate/String%, %BitDepth/String%, %SamplingRate/String%, %Channel(s)% channels" '
                     f'"{file_path}"')
    return subprocess.check_output(mediainfo_cmd, shell=True, text=True)
