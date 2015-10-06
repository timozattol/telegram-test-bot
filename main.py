import telegram
import time

from datetime import datetime

from imgurpython import ImgurClient

from tokens import bot_token
from tokens import imgur_client_id
from tokens import imgur_client_secret

bot = telegram.Bot(bot_token)
imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

# "Snapshot" of the imgur frontpage state, 
# at the time of the first "/imgur" request
current_gallery = None
current_gallery_day = None
current_gallery_index = 0

def main():
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
				if(message.text[0] == '/'):
					execute(message)
				else:
					pass

			last_update_id = update.update_id + 1

def execute(message):
	helpMessage = """
		Available commands:
		/help --> Show this message
		/imgur --> Fetch an image from the frontpage of imgur
		"""

	# Help command
	if(message.text == "/help"):
		bot.sendMessage(
			chat_id=message.chat_id,
			text=helpMessage)

	# Imgur command
	elif(message.text == "/imgur"):
		img = fetchNextImgurImage()

		response = img.title + "\n" + img.link if img else "No more image in gallery, shouldn't you go to work? ;)"

		bot.sendMessage(
			chat_id=message.chat_id,
			text=response)
	else:
		response = "Unfortunately, your command isn't supported yet.\n" + helpMessage

		bot.sendMessage(
		chat_id=message.chat_id, 
		text=response)

def fetchNextImgurImage():
	global current_gallery, current_gallery_day, current_gallery_index

	# If gallery is outdated, fetch new gallery
	if current_gallery == None or current_gallery_day != datetime.now().date():
		current_gallery = imgur_client.gallery()
		current_gallery_index = 0
		current_gallery_day = datetime.now().date()
		print("Daily gallery loaded. Size: " + str(len(current_gallery)))

	# No more image on first page
	if current_gallery_index > len(current_gallery):
		return None
	else:
		img = current_gallery[current_gallery_index]
		current_gallery_index += 1
		return img

if __name__ == '__main__':
	main()