import telegram
import time

from token import bot_token

bot = telegram.Bot(bot_token)

def main():
	# Find the last fetched update id
	updates = bot.getUpdates()

	if len(updates) > 0:
		last_update_id = updates[-1].update_id
	else:
		last_update_id = None


	while(True):

		updates = bot.getUpdates(offset=last_update_id, timeout=20)

		for update in updates:
			message = update.message

			if (message):
				if(message.text[0] == '/'):
					execute(message)
				else:
					bot.sendMessage(
						chat_id=message.chat_id,
						text='Thanks for your message: "' +
							message.text + '"')

			last_update_id = update.update_id + 1


def execute(message):
	bot.sendMessage(
		chat_id=message.chat_id, 
		text="Thanks for your command! Unfortunately it isn't supported yet.")

if __name__ == '__main__':
	main()