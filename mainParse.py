from html.parser import HTMLParser
import urllib.request as urllib
import codecs
import re

courseNameLen = 6 
URL = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-CS.html"
response = urllib.urlopen(URL) # open URL & store object
file = response.read().decode("utf-8") # Read & convert raw data to string


# pattern only works for CS courses for now 

pattern1 = re.compile(r'<a name = "CS(\d+)"></a>.+?<i>(Prereq: .+?)</i>') # With Course Prereqs
pattern2 = re.compile(r'<a name = "CS(\d+)"></a>') # Course Code only 
parsedWithPreReq = re.findall(pattern1, file)
parsedOnlyCCode = re.findall(pattern2, file)
print(parsedWithPreReq)
print(parsedOnlyCCode)


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
