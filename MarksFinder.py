import csv
import os
import Student

class MarksFinder:
    def __init__(self, marks_file):
        my_dir = os.path.dirname(__file__)
        self.students_file = os.path.join(my_dir, marks_file)
        
    def search(self, std_number):
        with open(self.students_file, newline='') as csvfile:

            marksreader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for row in marksreader:
                if std_number == row[0]:
                    return row
        return None

    def find(self, std_number):     
        student_row = self.search(std_number)
        if student_row == None:
            return False, None
        return True, Student.from_row(student_row)
