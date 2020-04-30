import csv
import sys
import os


def voiceMatched(userId, wavFilePath):
	empty = True
	lines = [["filename", "speaker"]]
	for root, dirs, files in os.walk("/opt/mycroft/skills/useridentification-skill/allUsers"):
		for file in files:
			if (userId in file.split('-')[0]):
				lines.append([os.path.join(root, file), userId])
				empty = False
	
	if (empty == False):
		#add the path of the user to check
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/enroll_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		#add current path file to check
		lines = [["filename", "speaker"], [wavFilePath, 0]]
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/test_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)
		

		#run the voice identification
		os.system("python3.7 /opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/scoring.py")

		#get answers from results.csv
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
			if (".wav" in file):
				lines.append([os.path.join(root, file), "0"])
				empty = False
	if (empty == False):
		#add all the voices to check
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/enroll_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		#add current path file to check
		lines = [["filename", "speaker"], [wavFilePath, 0]]
		with open ('/opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/cfg/test_list.csv' , 'w') as writeFile:
			writer = csv.writer(writeFile)
			writer.writerows(lines)

		#run the voice identification
		os.system("python3.7 /opt/mycroft/skills/useridentification-skill/speakerIdentificationProgram/scoring.py")

		#get answers from results.csv
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
