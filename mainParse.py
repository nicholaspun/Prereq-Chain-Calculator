from itertools import filterfalse 
import urllib.request as urllib
import codecs
import re

#------------------
# Global Variables
#------------------
URL = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-CS.html"

#------------------
# MAIN FUNCTIONS
#------------------
def buildDict():
    '''
    Builds a dictionary of courses from the provided URL above.
    Key -- Course Code 
    Value -- Un-modified Prerequistes
    '''
    #response = urllib.urlopen(URL) # open URL & store object
    #file = response.read().decode("utf-8") # Read & convert raw data to string

    file = open("CSHTML.txt",'r').read()
    
    # patterns only work for CS courses (for now) 
    pattern1 = re.compile(r'<a name = "CS(\d+)"></a>.+?<i>Prereq:(.+?)</i>') # With Course Prereqs
    pattern2 = re.compile(r'<a name = "CS(\d+)"></a>') # Course Code only

    # List of (Course Code, Prereq) for courses with prereqs
    parsedWithPreReq = re.findall(pattern1, file)

    parsedOnlyCCode = re.findall(pattern2, file) # List of only course codes

    DictofCourses = dict(parsedWithPreReq) # Key - Course Code, Value - Prereq
    
    # Set Value of "None" if Course does not have prereq
    for ccode in parsedOnlyCCode:
        if (ccode not in DictofCourses):
            DictofCourses[ccode] = "None"

    return DictofCourses


def makePrereqList(prereqStr):
    '''
    returns a list of parsed prerequistes 
    '''
    pList = prereqStr.split(';')
    
    # remove non course-related prereqs
    pList[:] = filterfalse(nonCoursePrereq, pList)

    # Split prereqs at "and"  
    tempList = []
    for i in range(len(pList)):
        tempList += pList[i].split(' and ')   
    pList = tempList

    # Split prereqs at "," (commas)
    tempList = []
    for i in range(len(pList)):
        tempList += pList[i].split("), ")
    pList = tempList
    
    # Split prereqs for "One of" and "Two of" cases
    pList = splitOneofTwoofCase(pList)

    # Split prereqs for "or" case
    tempList = []
    for i in range(len(pList)):
        if (type(pList[i]) == str and pList[i] != "NONE"):
            tempList += [1, pList[i].split(" OR ")]
        else:
            tempList += [pList[i]]
    pList = tempList
          
    return pList

#------------------
# CASE FUNCTIONS
#------------------
def nonCoursePrereq(prereq):
    '''
    returns true if "students" or "Level at least" present in prereq
    '''
    return ('students' in prereq) or ('Level at least' in prereq)

def splitOneofTwoofCase(pList):
    '''
    returns a list where:
      if the prereq contains the phrase "one of", it is formatted like so:
      "One of MATH 116, 136, 146" --> [1, ["MATH 116", "MATH 136", "MATH 146"]]

      if the prereq contains the phrase "one of", it is formatted like so:
      "Two of MATH 116, 136, 146" --> [2, ["MATH 116", "MATH 136", "MATH 146"]] 
    '''
    for i in range(len(pList)):
        # This line just makes things pretty.....
        pList[i] = pList[i].upper().strip().replace("(", "").replace(")", "")

        # Below is horrible code, it splits courses so that
        # they are individual, and inserts the department name
        # in front of each element
        if ("ONE OF" in pList[i]):
            pList[i] = pList[i].replace("ONE OF ", "")
            dept = findCourseDept(pList[i])
            pList[i] = [1, pList[i].split(",")]
            pList[i][1] = insertFront(dept, pList[i][1])
        elif ("TWO OF" in pList[i]):
            pList[i] = pList[i].replace("TWO OF", "")
            dept = findCourseDept(pList[i])
            pList[i] = [2, pList[i].split(",")]
            pList[i][1] = insertFront(dept, pList[i][1])         
    return pList

#------------------
# HELPER FUNCTIONS
#------------------
def findCourseDept(course):
    '''
    returns the department a course belongs to.

    e.g. "MATH 135" -> "MATH"
    '''
    dept = ""
    courseLen = len(course)
    for i in range(courseLen):
        if (course[i] == " "): break
        dept += course[i]
    return dept

def insertFront(dept, lst):
    '''
    returns a lst where the string dept is inserted before the start of
    each element in lst
    '''
    for i in range(len(lst)):
        if (i == 0): continue
        lst[i] = dept + lst[i]
    return lst
            
def findPrereq(courseCode):
    '''
    returns the prerequistes for given course code.
    '''
    pass 

#------------------
# Main Script
#------------------

courses = buildDict()
#print(courses)
for key, value in courses.items():
    courses[key] = makePrereqList(value)
print(courses)

''' Tests:
print("orig:", courses["330"])
print(makePrereqList(courses["330"])) # non course-related prereq
print("orig:", courses["349"])
print(makePrereqList(courses["349"])) # "and" keyword (and "One of")
print("orig:", courses["245"])
print(makePrereqList(courses["245"])) # , (comma)
print("orig:", courses["452"])
print(makePrereqList(courses["452"])) # "or" keyword
'''




