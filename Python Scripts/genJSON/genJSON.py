from itertools import filterfalse 
import urllib.request as urllib
import codecs
import re
import json

#------------------
# Global Variables
#------------------
URL_CS = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-CS.html"
# URL_STAT = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-STAT.html"
# The course calendar page for STAT courses is extremely inconsistent
# --> See STAT.json for JSON data for STAT courses
URL_MATH = "http://www.ucalendar.uwaterloo.ca/1617/COURSE/course-MATH.html"

#------------------
# MAIN FUNCTIONS
#------------------
def buildDict(URL):
    '''
    Builds a dictionary of courses from the provided URL.
    Key -- Course Code 
    Value -- Un-modified Prerequistes
    '''
    response = urllib.urlopen(URL) # open URL & store object
    file = response.read().decode("utf-8") # Read & convert raw data to string

    #file = open("CSHTML.txt",'r').read() # for offline usage

    # find department
    deptPattern = re.compile(r"course-(.+?).html")
    dept = re.search(deptPattern, URL).group(1)
    
    # patterns only work for CS courses (for now) 
    pattern1 = re.compile(r'<a name = "(%s\d+)"></a>.+?<i>Prereq:(.+?)</i>' % dept) # With Course Prereqs
    pattern2 = re.compile(r'<a name = "(%s\d+)"></a>' % dept) # Course Code only

    # List of (Course Code, Prereq) for courses with prereqs
    parsedWithPreReq = re.findall(pattern1, file)

    parsedOnlyCCode = re.findall(pattern2, file) # List of only course codes

    DictofCourses = dict(parsedWithPreReq) # Key - Course Code, Value - Prereq
    
    # Set Value of "None" if Course does not have prereq
    for ccode in parsedOnlyCCode:
        if (ccode not in DictofCourses):
            DictofCourses[ccode] = "None"

    # Parse through prereqs and transform in meaningful lists
    for key, value in DictofCourses.items():
        DictofCourses[key] = makePrereqList(value)

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
        tempList += pList[i].split('and') 
    pList = tempList

    # Split prereqs at "," (commas) [1]
    tempList = []
    for i in range(len(pList)):
        tempList += pList[i].split("), ")
    pList = tempList
    
    # Split prereqs for "One of" and "Two of" cases
    pList = splitOneofTwoofCase(pList)

    # Split prereqs for "or" case
    tempList = []
    for i in range(len(pList)):
        if (type(pList[i]) == str and pList[i] != "NONE" and "OR" in pList[i]):
            splitList = pList[i].split(" OR ")
            dept = findCourseDept(splitList[0])
            splitList = insertFront(dept, splitList)
            tempList += [[1, splitList]]
        else:
            tempList += [pList[i]]
    pList = tempList
    
    # Split prereqs at "," (commas) [2 - again]
    # This case is necessary, when such prereq strings are given:
    # --> 'CS 240, 241'
    # Such a case cannot be handled before handling the "One of"
    #   and "Two of" cases because those commas stand for OR, while
    #   the commas in this case stand for AND.
    tempList = []
    for i in range(len(pList)): # Yes, I realize there's a lot of repeated code
                                # No, I won't try to make it more abstract
        if (type(pList[i]) == str and pList[i] != "NONE"):
            splitList = pList[i].split(", ")
            dept = findCourseDept(splitList[0])
            splitList = insertFront(dept, splitList)
            tempList += splitList
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

def findPrereqChain(courseCode):
    '''
    returns the prerequistes chain for given course code.
    '''
    courseList = courseDict[courseCode]
    print(courseList)

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

#------------------
# Main Script
#------------------

CS_dict = buildDict(URL_CS)
MATH_dict = buildDict(URL_MATH)

print(CS_dict)
#print("+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~\n")
#print(MATH_dict)
#print("+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~+~++~+~+~+~\n")

# Convert to json and write to file.
#CS_json = json.dumps(CS_dict, sort_keys=True, indent=4, separators=(',', ': '))

#CS_json_file = open("CS2.json", 'w') 
#CS_json_file.write(CS_json)
#CS_json_file.close()



