#!/usr/bin/python3

import telegram

import logging

from datetime import datetime

from imgurpython import ImgurClient

from tokens import bot_token
from tokens import imgur_client_id
from tokens import imgur_client_secret

from chathandler import ChatHandler

bot = telegram.Bot(bot_token)
imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

# Dict of {chat_id: ChatHandler}
id_chat_handlers = {}

def main():
	# Set up the logging
	logging.basicConfig(filename='logging.log', level=logging.DEBUG)
	logging.info('== Bot started at ' + str(datetime.now()) + ' ==')

	# Find the last fetched update id
	updates = bot.getUpdates()

	if len(updates) > 0:
		last_update_id = updates[-1].update_id
	else:
		last_update_id = None

	print("Starting main loop")

	# Main loop
	while(True):

		updates = bot.getUpdates(offset=last_update_id, timeout=20)

		for update in updates:
			message = update.message

			if (message):
				# If first message from chat, create a ChatHandler
				if message.chat_id not in id_chat_handlers:
					id_chat_handlers[message.chat_id] = \
						ChatHandler(message.chat_id, bot, imgur_client)

				chat_handler = id_chat_handlers[message.chat_id]

				chat_handler.log(message)

				if(message.text[0] == '/'):
					chat_handler.execute(message)
				else:
					pass

			last_update_id = update.update_id + 1

if __name__ == '__main__':
	main()