# telegram-test-bot
A testing purpose telegram bot, written in python using the [python-telegram-bot wrapper](https://pypi.python.org/pypi/python-telegram-bot)

## Commands

* `/help` Send help message
* `/imgur` Send an image from the main gallery of imgur
* `/imgur search some words` Search an image on imgur based on "some words"

## Install your own bot

To install the bot on your server, clone the repo, rename the `tokens.py.example` file to `tokens.py`. Create a telegram bot with [Botfather](https://telegram.me/botfather), and fill in the `bot_token` in tokens.py. You should also ask for [imgur API tokens](https://api.imgur.com/oauth2/addclient) and fill the `client_id` and `client_secret` in tokens.py. 

You also need to install the dependencies: 
```bash
pip install python-telegram-bot
pip install imgurpython
```

Your bot is ready! Launch it with `./main.py` or `python3 main.py`.
