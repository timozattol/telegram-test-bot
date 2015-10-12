import logging

from datetime import datetime

class ChatHandler:

	def __init__(self, chat_id, bot, imgur_client):
		self.chat_id = chat_id

		self.bot = bot

		self.imgur_client = imgur_client

		# "Snapshot" of the imgur frontpage state, 
		# at the time of the first "/imgur" request
		self.current_gallery = None
		self.current_gallery_day = None
		self.current_gallery_index = 0

	def __print_info(self, info):
		print("Chat #" + str(self.chat_id) + ": " + info)

	def __fetch_next_imgur_image(self):
		# If gallery is outdated, fetch new gallery
		if self.current_gallery == None or \
				self.current_gallery_day != datetime.now().date():
			self.current_gallery = self.imgur_client.gallery()
			self.current_gallery_index = 0
			self.current_gallery_day = datetime.now().date()
			self.__print_info("Daily gallery loaded. Size = " + str(len(self.current_gallery)) + " images")

		# No more images on first page
		if self.current_gallery_index > len(self.current_gallery):
			return None
		else:
			img = self.current_gallery[self.current_gallery_index]
			self.current_gallery_index += 1
			return img

	def __send_message(self, string):
		self.bot.sendMessage(
			chat_id=self.chat_id,
			text=string)

	def __send_help_message(self):
		helpMessage = """
			Available commands:
			/help --> Show this message
			/imgur --> Fetch an image from the frontpage of imgur
			"""

		self.__send_message(helpMessage)

	def log(self, message):
		log_string = "Chat #" + str(self.chat_id) + ": " + message.text
		logging.debug(log_string)
		print(log_string)

	def execute(self, message):
		# Message should be from this chat
		if message.chat_id != self.chat_id:
			raise Exception("Message " + message.message_id + " was sent to wrong ChatHandler")

		# Help command
		if(message.text == "/help"):
			self.__send_help_message()

		# Imgur command
		elif(message.text == "/imgur"):
			img = self.__fetch_next_imgur_image()

			response = img.title + "\n" + img.link if img else "No more image in gallery, shouldn't you go to work? ;)"

			self.__send_message(response)
		else:
			response = "Unfortunately, your command isn't supported yet.\n" + helpMessage

			self.__send_message(response)