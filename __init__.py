from mycroft import MycroftSkill, intent_file_handler


class Useridentification(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('useridentification.intent')
    def handle_useridentification(self, message):
        self.speak_dialog('useridentification')


def create_skill():
    return Useridentification()

