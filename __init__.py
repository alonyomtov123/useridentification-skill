from mycroft import MycroftSkill, intent_file_handler
import os
from shutil import copyfile
import os
import sqlite3
import sys

sys.path.append("/opt/mycroft/skills/useridentification-skill")
from sqlGui import getUserData
from voiceRecognition import voiceFound, voiceMatched



class Useridentification(MycroftSkill):
	def __init__(self):
	        MycroftSkill.__init__(self)
	
	def converse(self, utterances):
		utt = utterances[0]
		if self.voc_match(utt, 'useridentification.intent'):
		# mock the standard message object to pass it to a standard intent handler
			mock_message = {'data': {'utterance': utt}}
			if(self.handle_useridentification(mock_message) == False):
				return False
			return True
		return False
		


	#What to do when skill is triggered
	@intent_file_handler('useridentification.intent')
	def handle_useridentification(self, message):

		#connect to database
		conn = sqlite3.connect('/opt/mycroft/skills/useridentification-skill/allUsers/Users.db')
		c = conn.cursor()		
		c.execute("SELECT * FROM User")

		if not (c.fetchone() == None):
			currentUser = ""
			for row in c.execute("SELECT * FROM User"):
				self.speak(row[0])
				if (row[3] == '1'):
					currentUser = row[0]
			self.speak(currentUser)
			currentUserAnswer = getCurrentUserAnswer()
			self.speak("voice matched")
			
			if (voiceMatched(currentUser, currentUserAnswer)):
				return False
			else:
				self.speak("voice found")
				if (voiceFound(currentUserAnswer)):
					self.signIn("")
					return False
				else:
					answer = self.get_response("Do you want to sign up?")
					if (answer == "yes"):
						self.signUp()
						return False
					elif (answer == "no"):
						return True
					else:
						self.speak(answer)
						self.speak("Answer is invalid")
						return True
		else:
			self.speak("No user is currently registered")
			answer = self.get_response("Do you want to sign up?")
			if (answer == "yes"):
				self.signUp()
				return False
			elif (answer == "no"):
				self.speak("Goodbye")
				return True
			else:
				self.speak(answer)
				self.speak("Answer is invalid.")
				return True
		conn.close()



	def signIn(self, userId):
		conn = sqlite3.connect('/opt/mycroft/skills/useridentification-skill/allUsers/Users.db')
		c = conn.cursor()	
		if(userId == ""):
			c.execute("SELECT * FROM User")
			if not (c.fetchone() == None):
				for row in c.execute("SELECT * FROM User"):
					if (voiceMatched(row[1], getCurrentUserAnswer())):
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

		settingsFile = open("/opt/mycroft/skills/useridentification-skill/settingFile.txt", "r")
		for directory in settingsFile.readlines():
			#find which file to change
			
			currentSettingsFile = open(os.path.join(directory.rstrip()), "r+")
			allFileData = currentSettingsFile.readlines()
			for line in range(len(allFileData)):
				if ("Username" in allFileData[line] or "username" in allFileData[line] and "value" in allFileData[line + 1]):
					allFileData[line + 1] = '          value: "' + username + '"\n'
				if ("Password" in allFileData[line] or "password" in allFileData[line]  and "value" in allFileData[line + 1]):
					allFileData[line + 1] = '          value: "' + password + '"\n'

			currentSettingsFile.seek(0)
			for line in allFileData:
				currentSettingsFile.write(line)
			currentSettingsFile.close()
		settingsFile.close()
		conn.close()
		print("\n\n\n\n\n\nfinished signIn\n\n\n\n\n\n")


	def signUp(self):
		audioFile = getCurrentUserAnswer()
		getUserData('/opt/mycroft/skills/useridentification-skill/allUsers/Users.db')
		
		conn = sqlite3.connect('/opt/mycroft/skills/useridentification-skill/allUsers/Users.db')
		c = conn.cursor()		
		c.execute("SELECT COUNT(*) FROM User")

		self.signIn(c.fetchone()[0])


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
