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
			if(self.handle_useridentification(mock_message) == False):
				return False
			return True
		return False
		


	#What to do when skill is triggered
	@intent_file_handler('useridentification.intent')
	def handle_useridentification(self, message):
		#add files from questions
		#if first time
		#explaining
		#testing
		#get username and password in signUp
		#change file to sql
		UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
		if not (os.stat("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt").st_size == 0):
			currentUser = UsersFile.readline().split(':')[1].split('-')[0][1:]
	
			currentUserAnswer = getCurrentUserAnswer()
		
			if (voiceMatched(currentUser, currentUserAnswer)):
				return False
			else:
				if (voiceFound(currentUserAnswer)):
					answer = self.ask_yesno("do.you.want.to.sign.in?")
					if (answer == "yes"):
						self.signIn("")
						return False
					elif (answer == "no"):
						return True
					else:
						self.speak("Answer Is Invalid")
						return True
				else:
					answer = self.get_response("do.you.want.to.sign.up?")
					if (answer == "yes"):
						self.signUp()
						return False
					elif (answer == "no"):
						return True
					else:
						self.speak("Answer Is Invalid")
						return True
		else:
			answer = get_response("do.you.want.to.sign.up?")
			if (answer == "yes"):
				self.signUp(self)
				return False
			elif (answer == "no"):
				return True
			else:
				self.speak("Answer Is Invalid")
				return True
		UsersFile.close()



	def signIn(self, userId, name):
		if(userId == ""):
			UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
			if not (os.stat("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt").st_size == 0):
				Users.readline()
				for user in UsersFile.readline():
					if (voiceMatched(user.split('-')[0], getCurrentUserAnswer())):
						userId = user.split('-')[0]
						name = user.split('-')[1]
			UsersFile.close()

		UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "w")
		UsersFile.write("Current User: " + userId + name)
		#settingsFile = open("/opt/mycroft/skills/useridentification-skill/settingFile.txt", "r")
		#for directory in settingsFile.readline():
			#find which file to change
			#get password
			#get username
		#	currentSettingsFile = open(os.path.join(derectory + ), "w")
		#	for line in currentSettingsFile.readline():
		#		if ("Username" in line or "username" in line):
		#			nextLine = currentSettingsFile.readline()
		#			if("value" in nextLine):
		#				currentSettingsFile.write('\t\tvalue: ""')
		#		if ("Password" in line or "password" in line):
		#			nextLine = currentSettingsFile.readline()
		#			if("value" in nextLine):
		#				currentSettingsFile.write('\t\tvalue: ""')
		#	currentSettingsFile.close()
		#settingsFile.close()
		UsersFile.close()



	def signUp(self):
		audioFile = getCurrentUserAnswer()
	
		name = get_response("Please.choose.a.name")
		found = True
		numOfUsers = 0
		while (found == True):
			found = False
			numOfUsers = 0		
	
			UsersFile = open("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt", "r")
			if not (os.stat("/opt/mycroft/skills/useridentification-skill/allUsers/Users.txt").st_size == 0):
				Users.readline()
				for user in UsersFile.readline():
					numOfUsers += 1
					if (user.split('-')[1] == name):
						found = True
						self.speak("User.name.is.already.used")
						name = get_response("Please.choose.a.name")
						found = True
						break
			UsersFile.close()
	
		dest = "/opt/mycroft/skills/useridentification-skill/allUsers/" + (numOfUsers + 1) + "-" + name + "-1" + ".wav"
		copyfile(getCurrentUserAnswer(), dest)

		self.signIn(numOfUsers + 1, name)

def voiceMatched(userId, wavFilePath):
	#get files of user id
	empty = True
	lines = [["filename", "speaker"]]
	for root, dirs, files in os.walk("/opt/mycroft/skills/useridentification-skill/allUsers"):
		for file in files:
			if (userId in file.split('-')[0]):
				lines.append([os.path.join(root, file), userId])
				empty = False
	if (empty == False):
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/enroll_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		lines = [["filename", "speaker"], [wavFilePath, 0]]
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/test_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)
		
		os.system("python /opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/scoring.py")

		#get answer	
		found = False
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/res/results.csv' , 'r') as readFile:
			reader = csv.reader(readFile)
			lines = list(reader)
		if (userId == lines[1][-2]):
			found = True

		return found
	return False



def voiceFound(wavFilePath):
	lines = [["filename", "speaker"]]
	empty = True
	for root, dirs, files in os.walk("/opt/mycroft/skills/useridentification-skill/allUsers"):
		for file in files:
			if ("wav" in file):
				lines.append([os.path.join(root, file), "0"])
				empty = False
	if (empty == False):
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/enroll_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		lines = [["filename", "speaker"], [wavFilePath, 0]]
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/test_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		os.system("python /opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/scoring.py")

		#get answer
		found = False
		for line in open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/res/results.csv' , 'r'):
			row = line.split()[2:-2]	
		for num in row:
			if ("opt" not in num):
				if ("E" in num):
					found = True				
				if (float(num) < 0.3):
					found = True
		return found
	return False



def getCurrentUserAnswer():
	#get current question sound file	
	#/tmp/mycroft/mycroft_utterance(timestamp).wav
	allWaveFilePaths = []	
	for root, dirs, files in os.walk("/tmp"):
		for file in files:
			if ("mycroft" in file and ".wav" in file):
				allWaveFilePaths.append(file)
	return sorted(allWaveFilePaths)[0]

def create_skill():
	return Useridentification()
