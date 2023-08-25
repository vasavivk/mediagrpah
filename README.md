# MediaInfoBot
Multi-Utility bot for telegram!

## Features
- Generates MediaInfo of video/audio files from the following services:     
 [G-Drive, Mega.nz, AppDrive, GDTOT, DDL, Telegram files]
- Can generate audio spectrogram of a telegram audio file.
- Can show all the available codecs of an AppleMusic album.

#### Setup procedure:

- Follow [this guide](https://www.iperiusbackup.net/en/how-to-enable-google-drive-api-and-get-client-credentials/), but at the last step instead of selecting application as `web application` use `desktop app`   

<img src="https://user-images.githubusercontent.com/67633271/177330592-c686e8f6-2e16-4461-9e50-f84effd66969.png" width="500"/>    

- Download the json and save it as `credentials.json`.    
- `git clone https://github.com/bunnykek/MediaInfoBot`     
- Navigate into the `TokenGeneration` directory and follow the [readme.txt](https://github.com/bunnykek/MediaInfoBot/blob/main/TokenGeneration/readme.txt) for further procedure.
- Deploy to heroku 
#### Heroku Deploy
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/bunnykek/MediaInfoBot)
#### Bot commands:
- `/help` - Helps
- `/info` - For generating MediaInfo or AppleMusic album codecs info.
- `/spek` - Generates audio spectrogram.

##### Make sure to star/fork my projects if you enjoy using it. Thanks

