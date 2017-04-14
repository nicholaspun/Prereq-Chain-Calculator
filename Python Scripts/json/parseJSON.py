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
    printPrereqsHelper(course, 0)


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

def printPrereqsHelper(course, spaces):
    dept = findCourseDept(course)
    courseData = data[dept][course]
    if (spaces == 0):
        print(course)
    else: 
        print(" "*spaces + "+", course)
    for ele in courseData:
        if (type(ele) == list): listHandler(ele, spaces + 1)
        else: print(" "*spaces + "+", ele) 

def listHandler(courseList, spaces):
    print(" "*spaces + str(courseList[0]), "of:")
    for cour in courseList[1]:
        printPrereqsHelper(cour, spaces + 1)


printPrereqs("CS246")
printPrereqs("CS452")  

    
