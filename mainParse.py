from itertools import filterfalse 
import urllib.request as urllib
import codecs
import re

#------------------
# Global Variables
#------------------
courseNameLen = 6 
URL = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-CS.html"

#------------------
# HELPER FUNCTIONS
#------------------
def nonCoursePrereq(prereq):
    '''
    returns true if "students" or "Level at least" present in prereq
    '''
    return ('students' in prereq) or ('Level at least' in prereq)

def makePrereqList(prereqStr):
    '''
    returns a list of parsed prerequistes 
    '''
    pList = prereqStr.split(';')
    print(pList)
    # remove non course-related prereqs
    pList[:] = filterfalse(nonCoursePrereq, pList)
    print(pList)
    for x in pList:
        x = x.split('and'))
        
    print(pList)
    # Split prereqs for "One of" and "Two of" cases
    '''
    for p in pList:
        p = p.upper().strip()
        if ("ONE OF" in p):
            p.replace("ONE OF", "")
            p = p.split(', ')
            p = [1, prereq]
        elif ("TWO OF" in prereq):
            p.replace("TWO OF", "")
            p = p.split(', ')
            p = [2, prereq]
            '''
                
    return pList

def findPrereq(courseCode):
    '''
    returns the prerequistes for given course code.
    '''
    pass 

def buildDict():
    '''
    Builds a dictionary of courses from the provided URL above.
    Key -- Course Code 
    Value -- Un-modified Prerequistes
    '''
    response = urllib.urlopen(URL) # open URL & store object
    file = response.read().decode("utf-8") # Read & convert raw data to string

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


#------------------
# Main Script
#------------------

courses = buildDict()

# Tests:
print(makePrereqList(courses["330"])) # non course-related prereq
print(makePrereqList(courses["349"])) # "and" keyword 




