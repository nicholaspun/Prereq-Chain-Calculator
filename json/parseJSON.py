import json

#-------------------
# Read in JSON files
#-------------------
depts = ["CS", "MATH", "STAT"]
data = {}
for dept in depts:
    filename = dept + ".json"
    data[dept] = json.loads(open(filename).read())

#-------------------
# MAIN FUNCTIONS
#-------------------
def printPrereqs(course):
    dept = findCourseDept(course)
    courseData = data[dept][course]
    print(course)
    for ele in courseData:
        if (type(ele) == list): listHandler(ele)
        else: print(ele)


#-------------------
# HELPER FUNCTIONS
#-------------------
def findCourseDept(course):
    '''
    returns the department a course belongs to.

    e.g. "MATH135" -> "MATH"
    '''
    dept = ""
    courseLen = len(course)
    for i in range(courseLen):
        if (course[i].isdigit()): break
        dept += course[i]
    return dept

def listHandler(courseList):
    '''
    '''
    print(courseList[0], "of:\n")
    for cour in courseList[1]:
        printPrereqs(cour)


printPrereqs("CS246")        

    
