from json import dumps
import html
import csv


def format_committees():
    committees = []

    with open('./Raw Files/Committee List Raw.csv', 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        for line in reader:
            committees.append(
                {
                    "CommitteeID": len(committees),
                    "ComitteeDesignation": line[0].strip(),
                    "ComitteeCode": line[1].strip(),
                    "CommitteeName": line[2].strip(),
                    "ComitteeType": line[3].strip()
                }
            )

    with open('./Clean Files/Committee List.json', 'w', encoding='UTF-8') as f: f.write(dumps(committees, indent=4))
    
def format_faculty():
    faculty = []

    with open('./Raw Files/Faculty List Raw.csv', 'r', encoding='UTF-8') as file:
        reader = csv.reader(file)
        for line in reader:
            line = [l.replace("\u00a0", " ").replace("\u2019", "'").replace("\u00e1", "a").replace("\u00f3", "o") for l in line]
            faculty.append(
                {
                    "FacultyID": len(faculty),
                    "FacultyName": line[0].strip() + ' ' + line[1].strip(),
                    "FacultyDepartment": line[2].strip(),
                    "FacultyAffiliation": None if len(line[3].strip()) == 0 else line[3].strip(),
                    "FacultyTitle": None if len(line[4].strip()) == 0 else line[4].strip()
                }
            )
            items = []
            current_faculty = faculty[len(faculty) - 1]
            for key in current_faculty.keys(): items.append(f'"{current_faculty[key]}"')
                
            
            print("(" + ', '.join(items) + "),")
                
        
        with open('./Clean Files/Faculty List.json', 'w', encoding='UTF-8') as f: f.write(dumps(faculty, indent=4))
        


format_committees()
format_faculty()