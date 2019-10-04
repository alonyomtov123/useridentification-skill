import os

def main():	
	myIntentFile = open("vocab/en-us/useridentification.intent", "w+")
	#find all skills
	for root, dirs, files in os.walk("/opt/mycroft/skills"):
		for file in files:
			#find all specific skills
			if("settingsmeta.yaml" == file or "settingsmeta.json" == file):
				currentFile = open(os.path.join(root, file), "r")
				if("email" in currentFile.read()):
					#find all the intents (triggers) of specific skill
					for secondRoot, secondDirs, secondFiles in os.walk(root):
						for allCurrentFiles in secondFiles:
							if ("intent" in allCurrentFiles):
								#add all intents from specific skill
								intentFile = open(os.path.join(secondRoot, allCurrentFiles), "r")
								if ("intent" not in intentFile.read()):
									intentFile.seek(0)
									myIntentFile.write(intentFile.read())
									myIntentFile.write("\n")
								intentFile.close()

	myIntentFile.close()

if __name__ == "__main__":
	main()
