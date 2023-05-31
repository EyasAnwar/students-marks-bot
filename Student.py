NAME = 1
MID = 2

def from_row(row):
    student = {'name': row[NAME],
                   'mid': row[MID]
                   }
    return student