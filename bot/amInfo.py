import re
import m3u8
import requests
from pyrogram.types import Message

apple_rx = re.compile(r"apple\.com\/(\w\w)\/album\/.+\/(\d+|pl\..+)")


headers = {
    'origin': 'https://music.apple.com',
    'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNjkxNzg4NjU0LCJleHAiOjE2OTkwNDYyNTQsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.fb4RBzciVRzF9EWFvVFML2h6TM26QislDpMaJc_E7equbrE1lq59kQ2vFpuNRn6nrpqAJGmDc1zoswdedml12g',
}

params = {
    'extend': 'extendedAssetUrls',
}

def updateToken():
    response = requests.get("https://music.apple.com/us/album/positions-deluxe-edition/1553944254")
    jspath = re.search("crossorigin src=\"(/assets/index.+?\.js)\"", response.text).group(1)
    my = requests.get("https://music.apple.com"+jspath)
    tkn = re.search(r"(eyJhbGc.+?)\"", my.text).group(1)
    headers['Authorization'] = f'Bearer {tkn}'

def format_duration(duration_in_millis):
    duration_in_seconds = duration_in_millis / 1000
    minutes = int(duration_in_seconds // 60)
    seconds = int(duration_in_seconds % 60)
    return f"{minutes}:{seconds:02}"

def amInfo(message: Message):
    result = apple_rx.search(message.text)
    if not result:
        message.reply("`Improper Apple Music album URL!`")
        return
    region, id_ = result.groups()
    #print(region, id_)
    response = requests.get(f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{id_}/', params=params, headers=headers)
    if response.status_code == 401:
        print("Updating token!")
        updateToken()
        response = requests.get(f'https://amp-api.music.apple.com/v1/catalog/{region}/albums/{id_}/', params=params, headers=headers)
    info = response.json()['data'][0]
    release_date = info['attributes']['releaseDate']
    adm = 'True' if info['attributes']['isMasteredForItunes'] else 'False'
    url = info['attributes']['url']
    name = info['attributes']['name']
    artist = info['attributes']['artistName']
    traits = info['attributes']['audioTraits']
    artwork = info['attributes']['artwork']['url']
    w = str(info['attributes']['artwork']['width'])
    h = str(info['attributes']['artwork']['height'])
    barcode = info['attributes']['upc']
    Copyright = info['attributes']['copyright']
    stream = not info['attributes']['isComplete']
    hls = info['relationships']['tracks']['data'][0]['attributes']['extendedAssetUrls']['enhancedHls']
    #print(hls)
    playlist = m3u8.parse(m3u8.load(hls).dumps())
    alacs = []
    for stream in playlist['playlists']:
        if stream['stream_info']['codecs'] == 'alac':
            temp = stream['stream_info']['audio'].split('-')
            sr = int(temp[-2])/1000
            depth = int(temp[-1])
            alacs.append((sr, depth))
    alacs.sort()
    #print(alacs)
    codecs = ["Lossy AAC"]
    if 'atmos' in traits:
        codecs.append("Dolby Atmos")
    if 'lossless' in traits:
        for i,j in alacs:
            codecs.append(f"ALAC {j}-{i}")

    formatted_lines = []
    for track in response.json()['data'][0]['relationships']['tracks']['data']:
        name = track['attributes']['name']
        duration = format_duration(track['attributes']['durationInMillis'])
        formatted_line = f"{track['attributes']['trackNumber']} {name} {duration}"
        formatted_lines.append(formatted_line)
    formatted_code = "\n".join([line for line in formatted_lines])

    text = f"""Album       : **[{name}]({url}) | [{w}x{h}]({artwork.format(w=w, h=h)})**
Artist      : **{artist}**
Release Date: **{release_date}**
Codecs      : **{' | '.join(codecs)}**
Barcode     : **{barcode}**
Mastered for iTunes: **{adm}**

**Tracklist**:
{formatted_code}

{Copyright}
"""

    message.reply_photo(photo=artwork.format(w=w,h=h), caption=text)
print("appleMusic loaded", flush=True)
