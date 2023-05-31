import os

class TemplateFiller:
    def __init__(self, template_file):
            my_dir = os.path.dirname(__file__)
            self.message_file = os.path.join(my_dir, template_file)
            self.message = self.read_message()
            
    def read_message(self):
        with open(self.message_file, 'r') as file:
            data = file.read().rstrip()
            return data
            
    def fill(self, student):
        name = student['name']
        mid = student['mid']
        return self.message.format(name, mid)