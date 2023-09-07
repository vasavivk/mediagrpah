import re
import m3u8
import requests
from pyrogram.types import Message
from bot.utils import katbin_paste
apple_rx = re.compile(r"apple\.com\/(\w\w)\/album\/.+\/(\d+|pl\..+)")
applemv_rx = re.compile(r"https://music\.apple\.com/(\w+)/music-video/.+\/(\d+)")

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
    artwork = info['attributes']['artwork']['url'].format(w=3000, h=3000).replace('bb.jpg', 'bb-999.jpg')
    artlink = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "urlupload", "url": {artwork}}).text
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
    trkplst = katbin_paste(formatted_code)

    text = f"""Album       : **[{name}]({url}) | [3000x3000]({artlink})**
Artist      : **{artist}**
Release Date: **{release_date}**
Codecs      : **{' | '.join(codecs)}**
Barcode     : **{barcode}**
Mastered for iTunes: **{adm}**
**[Tracklist]({trkplst})**
{Copyright}
"""

    message.reply_photo(photo=artwork, caption=text)


def amvInfo(message: Message):
    result = applemv_rx.search(message.text)
    if not result:
        message.reply("`Improper Apple Music album URL!`")
        return
    region, id_ = result.groups()
    response = requests.get(f'https://amp-api.music.apple.com/v1/catalog/{region}/music-videos/{id_}/', params=params, headers=headers)
    if response.status_code == 401:
        print("Updating token!")
        updateToken()
        response = requests.get(f'https://amp-api.music.apple.com/v1/catalog/{region}/music-videos/{id_}/', params=params, headers=headers).json()
    mv = response['data'][0]['attributes']['name']
    url = response['data'][0]['attributes']['url']
    dura = response['data'][0]['attributes']['durationInMillis']
    fdura = f"{dura // 60000}:{dura // 1000 % 60:02}"

    artist = response['data'][0]['attributes']['artistName']
    artwork = response['data'][0]['attributes']['artwork']['url'].format(w=3000, h=3000).replace('mv.jpg', 'mv-999.jpg')
    artlink = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "urlupload", "url": {artwork}}).text

    genre = ','.join(response['data'][0]['attributes']['genreNames'])
    hires = '🟢' if response['data'][0]['attributes']['has4K'] else '🔴'
    hdr = '🟢' if response['data'][0]['attributes']['hasHDR'] else '🔴'
    isrc = response['data'][0]['attributes']['isrc']
    date = response['data'][0]['attributes']['releaseDate']
    maxres = f"{response['data'][0]['attributes']['previews'][0]['artwork']['width']}x{response['data'][0]['attributes']['previews'][0]['artwork']['height']}"
    format = f"4K:{hires} | HDR:{hdr}"

    text = f"""
    Music Video : **[{mv}]({url}) | [3000x3000]({artlink})**
    Duration    : **{fdura} min**
    Artist      : **{artist}**
    Genre       : **{genre}**
    Release Date: **{date}**
    Formats     : **{format}**
    Max Resolution: **{maxres}**\n
    ISRC        : {isrc}
    """
    message.reply_photo(photo=artwork, caption=text)


print("appleMusic loaded", flush=True)
