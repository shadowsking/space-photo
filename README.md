# space-photo

Downloads images from SpaceX and NASA.

Telegram bot was used for publish to telegram channel.

## Installing

1) Clone project
```bash
git clone https://github.com/shadowsking/space-photo.git
cd space-photo
```

2) Create virtual environments
```bash
source install.sh
```
or
```bash
python -m venv venv
source venv/scripts/activate
```

3) Create new '.env' file from '.env.example' <br/>
   Fill in environment variable
   - NASA_TOKEN - generate API key from https://api.nasa.gov/
   - TELEGRAM_TOKEN
   - TELEGRAM_CHAT_ID
   - DELEY_SECONDS - default 4 hours


## Running
```bash
source start.sh
```

### telegram_bot
Downloads images from SpaceX and NASA and sends to telegram channel.
```bash
source venv/scripts/activate
python telegram_bot.py
```
Arguments:
- -с (--count) : str - Count NASA APOD
- -d (--dir_name) : str - Directory name, default "images".


### spacex_api
Downloads images from the last SpaceX launch.

```bash
source venv/scripts/activate
python spacex_api.py
```
Arguments:
- -u (--uuid) : str - UUID SpaceX launch

### nasa_api
Downloads APOD and Epic images from the NASA

```bash
source venv/scripts/activate
python nasa_api.py
```
Arguments:
- -d (--dir_name): str - Directory name, default "images"
- -a (--apod) : bool - Downloads APOD images
- -e (--epic) : bool - Downloads Epic images
- -c (--count): int - Apod count
