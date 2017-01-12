from html.parser import HTMLParser
import urllib.request as urllib
import codecs

courseNameLen = 6
URL = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-CS.html"
response = urllib.urlopen(URL)
file = response.read().decode("utf-8")


class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        if (data.startswith("CS ")):
            print("Course:", data[0:courseNameLen])
        if (data.startswith("Prereq: ")):
            print(data)

parser = MyHTMLParser()
parser.feed(file) 
