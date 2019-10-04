from mycroft import MycroftSkill, intent_file_handler
import os
from shutil import copyfile
import csv
import os

class Useridentification(MycroftSkill):
	def __init__(self):
	        MycroftSkill.__init__(self)
	
	def converse(self, utterances):
		utt = utterances[0]
		if self.voc_match(utt, 'useridentification.intent'):
		# mock the standard message object to pass it to a standard intent handler
			mock_message = {'data': {'utterance': utt}}
			if(self.my_intent_handler(mock_message) == False):
				return False
			return True
		return False
		


	#What to do when skill is triggered
	@intent_file_handler('useridentification.intent')
	def handle_useridentification(self, message):
		#add files from questions
		UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
		if not (os.stat("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt").st_size == 0):
			currentUser = UsersFile.readline().split(':')[1].split('-')[0][1:]
	
			currentUserAnswer = getCurrentUserAnswer()
		
			if (voiceMatched(currentUser, currentUserAnswer)):
				return False
			else:
				if (voiceFound(currentUserAnswer)):
					answer = get_response("do.you.want.to.sign.in?")
					if (answer == "yes"):
						signIn(self, "")
						return False
					elif (answer == "no"):
						return True
					else:
						self.speak("Answer Is Invalid")
						return True
				else:
					answer = get_response("do.you.want.to.sign.up?")
					if (answer == "yes"):
						signUp(self)
						return False
					elif (answer == "no"):
						return True
					else:
						self.speak("Answer Is Invalid")
						return True
		else:
			answer = get_response("do.you.want.to.sign.up?")
			if (answer == "yes"):
				signUp(self)
				return False
			elif (answer == "no"):
				return True
			else:
				self.speak("Answer Is Invalid")
				return True



	def create_skill():
	    return Useridentification()



	def signIn(self, userId, name):
		if(userId == ""):
			UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
			if not (os.stat("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt").st_size == 0):
				Users.readline()
				for user in UsersFile.readline():
					if (voiceMatched(user.split('-')[0], getCurrentUserAnswer())):
						userId = user.split('-')[0]
						name = user.split('-')[1]

		UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
		UsersFile.write("Current User: " + userId + name)
		#edit skill files



	def signUp(self):
		audioFile = getCurrentUserAnswer()
	
		name = ""
		found = False
		numOfUsers = 0
		while (name == "" or found == True):
			found = False
			numOfUsers = 0		
			name = get_response("Please.choose.a.name")
	
			UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
			if not (os.stat("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt").st_size == 0):
				Users.readline()
				for user in UsersFile.readline():
					numOfUsers += 1
					if (user.split('-')[1] == name):
						found = True
						self.speak("User.name.is.already.used")
	
		dest = "/opt/mycroft/skills/useridentification-skill/allUsers/" + (numOfUsers + 1) + "-" + name + "-1" + ".wav"
		copyfile(getCurrentUserAnswer(), dest)

		signIn(self, numOfUsers + 1, name)

	def voiceMatched(userId, wavFilePath):
		#get files of user id
		lines = [["filename", "speaker"]]
		for root, dirs, files in os.walk("/opt/mycroft/skills/useridentification-skill/allUsers"):
			for file in files:
				if (userId in file.split('-')[0]):
					lines.append([os.path.join(root, file), userId])
	
		with open ('/speakerIdentificationProgram/cfg/enroll_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		lines = [["filename", "speaker"], [wavFilePath, 0]]
		with open ('/speakerIdentificationProgram/cfg/test_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		execfile('speakerIdentificationProgram.scoring.py')
		#get answer	
		found = False
		with open ('/speakerIdentificationProgram/res/results.csv' , 'r') as readFile:
			writer = csv.writer(readFile)
			lines = list(reader)
		if (userID == lines[1][-2]):
			found = True
			
		return found
	


	def voiceFound(wavFilePath):
		lines = [["filename", "speaker"]]
		for root, dirs, files in os.walk("/opt/mycroft/skills/useridentification-skill/allUsers"):
			for file in files:
				if ("wav" in file):
					lines.append([os.path.join(root, file), "0"])
	
		with open ('/speakerIdentificationProgram/cfg/enroll_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		lines = [["filename", "speaker"], [wavFilePath, 0]]
		with open ('/speakerIdentificationProgram/cfg/test_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		execfile('speakerIdentificationProgram.scoring.py')

		#get answer	
		with open ('/speakerIdentificationProgram/res/results.csv' , 'r') as readFile:
			writer = csv.writer(readFile)
			lines = list(reader)
		found = False
		for num in lines[1]:
			if ("E" not in num and "opt" not in num):
				if (int(num) < 0.3):
					found = True
		return found



	def getCurrentUserAnswer():
		#get current question sound file	
		#/tmp/mycroft/mycroft_utterance(timestamp).wav
		allWaveFilePaths = []	
		for root, dirs, files in os.walk("/tmp/mycroft"):
			for file in files:
				if ("mycroft_utterance" in file):
					allWaveFilePaths.append(file)
		return allWaveFilePaths.sort()[0]
