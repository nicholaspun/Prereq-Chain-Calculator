from html.parser import HTMLParser
import urllib.request as urllib
import codecs
import re


'''
with open('miniHTML.txt', 'r') as file:
    contents = file.read() #.split('<center><table border=0 width=80%><tr><td align=left>')
pattern = re.compile(r'<a name = "(CS\d+)"></a>')
parsedContents = re.findall(pattern, contents)


parsedContents = []
for line in contents:
    parsedContents.append(re.search(pattern, line))
print(parsedContents)
'''

courseNameLen = 6 
URL = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-CS.html"
response = urllib.urlopen(URL) # open URL & store object
file = response.read().decode("utf-8") # Read & convert raw data to string


# pattern only works for CS courses for now 

pattern = re.compile(r'<a name = "CS(\d+)"></a>.*(Prereq: .+?)(?=</i></td></tr><tr><td colspan=2><i>)')
parsedFile = re.findall(pattern, file)
print(parsedFile)


'''
course_names = []
prereqs = []


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if (data.startswith("CS ")):
            course_names.append(data[0:courseNameLen])
        if (data.startswith("Prereq: ")):
            prereqs.append(data)

parser = MyHTMLParser()
parser.feed(file)

courses = dict(zip(course_names, prereqs))

def find_prereq(course_name):
    print(courses[course_name])

## Tests:
find_prereq("CS 448")
find_prereq("CS 135")
find_prereq("CS 100")
'''
