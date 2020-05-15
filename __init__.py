from mycroft import MycroftSkill, intent_handler
import os
import sqlite3
import sys

sys.path.append("/opt/mycroft/skills/useridentification-skill")
from .sqlGui import getUserData
from .voiceRecognition import voiceFound, voiceMatched



class Useridentification(MycroftSkill):
	def initialize(self):
		self.db_path = self.root_dir + '/allUsers/Users.db'
		# self.current_user = None

	def converse(self, utterances, lang=None):
		utt = utterances[0]
		is_authenticated = False
		if self.voc_match(utt, 'useridentification'):
			# mock the standard message object to pass it to a standard intent handler
			mock_message = {'data': {'utterance': utt}}

			is_authenticated = self.handle_identify_user(mock_message)
		else:
			return False
		self.log.info("is_authenticated: {}".format(is_authenticated))
		# If authenticated return False to continue processing utterance
		# Else return True to prevent further handling of utterance
		block_utterance = not is_authenticated
		return block_utterance


	#What to do when skill is triggered
	# @intent_handler('useridentification.intent')
	def handle_identify_user(self, message):
		self.log.info("AUTHENTICATING")
		is_authenticated = True
		return is_authenticated

		#connect to database
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		c.execute("SELECT * FROM User")

		if c.fetchone() == None:
			self.speak_dialog('no.registered.users')
			is_authenticated = self.prompt_for_registration()
		else:
			currentUser = ""
			for row in c.execute("SELECT * FROM User"):
				self.speak(row[0])
				if row[3] == '1':
					currentUser = row[0]
			self.speak(currentUser)
			currentUserAnswer = getCurrentUserAnswer()

			if voiceMatched(currentUser, currentUserAnswer):
				is_authenticated = True
			elif voiceFound(currentUserAnswer):
				self.signIn()
				is_authenticated = True
			else:
				is_authenticated = self.prompt_for_registration()

		conn.close()
		return is_authenticated


	def prompt_for_registration(self):
		registered = False
		answer = self.ask_yesno('signup.request')
		if (answer == "yes"):
			registered = self.signUp()
		elif (answer == "no"):
			self.speak_dialog('signup.declined')
		else:
			self.speak_dialog('invalid.response', {'answer': answer})
		return registered


	def signIn(self, userId=None):
		conn = sqlite3.connect(self.db_path)
		c = conn.cursor()
		if userId is None:
			c.execute("SELECT * FROM User")
			if c.fetchone() != None:
				for row in c.execute("SELECT * FROM User"):
					if voiceMatched(row[1], getCurrentUserAnswer()):
						userId = row[0]
						username = row[1]
						password = row[2]
		else:
			for row in c.execute("SELECT * FROM User"):
				if (row[0] == userId):
					username = row[1]
					password = row[2]

		#set current user in database
		c.execute("UPDATE User SET CurrentUser = 0 WHERE CurrentUser = 1")
		c.execute("UPDATE User SET CurrentUser = 1 WHERE ID = " + str(userId))
		conn.commit()
		conn.close()


	def signUp(self):
		try:
			audioFile = getCurrentUserAnswer()
			getUserData(self.db_path)

			conn = sqlite3.connect(self.db_path)
			c = conn.cursor()
			c.execute("SELECT COUNT(*) FROM User")

			self.signIn(c.fetchone()[0])
			return True
		except Exception:
			return False


def getCurrentUserAnswer():
	#get current question sound file
	#/tmp/mycroft_utterance(timestamp).wav
	allWaveFilePaths = []
	for root, dirs, files in os.walk("/tmp/mycroft_utterances"):
		for file in files:
			allWaveFilePaths.append(file)
	return "/tmp/mycroft_utterances/" + sorted(allWaveFilePaths)[0]

def create_skill():
	return Useridentification()
