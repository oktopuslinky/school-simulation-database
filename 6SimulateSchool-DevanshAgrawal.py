import sys

class Item:
    def __init__(self, name=None):
        self.name = name
'''
** DATA STRUCTURE **

courses=[
    {
        Course: "courseName", 
        Students: [students], 
        Teachers: [teachers]
    }, 
    ETC
]

students[
    {
        Name: "name",
        Courses: {
            Course1: [Teacher1],
            course2: [teacher2],
            etc
        }
    },
    ETC
]

teachers[
    {
        Name: "name",
        Courses: {
            course1: [students],
            course2: [students]
        }
    }
]
'''

'''
** OUTPUT TABLE STRUCTURE **

|-------------------------|
|COURSES|TEACHERS|STUDENTS|
|-------------------------|
|Course1|Teacher1|Student1|
|       |        |Student2|
|       |Teacher2|Student1|
|-------------------------|
|Course2|        |        |
|-------------------------|
'''
class Course(Item):
    def __init__(self, name):
        super().__init__(name)
        self.teachers = []
        self.students = []

        self.identity = {"Course": self.name, "Teachers": self.teachers, "Students": self.students}

class Person(Item):
    def __init__(self, name):
        super().__init__(name)
        self.related_people = []

        self.identity = {"Name": self.name, "Courses": {}}
'''
class Student(Item):
    def __init__(self, name):
        super().__init__(name)
        self.teachers = []

        self.identity = {"Name": self.name, "Courses": {}}

class Teacher(Item):
    def __init__(self, name):
        super().__init__(name)
        self.students = []

        self.identity = {"Name": self.name, "Courses": {}}
'''
class TakeInput():
    def __init__(self, input_type, input_disp_text):
        self.input_type = input_type
        self.input_disp_text = input_disp_text
        self.the_user_input = None
        self.take_input()

    def take_input(self):
        input_valid = False
        if self.input_type == "int":
            while input_valid is False:
                try:
                    user_input = int(input(self.input_disp_text + ": "))
                    if user_input:
                        input_valid = True
                except:
                    print("Please try again.")
            
            self.the_user_input = user_input
            return

        if self.input_type == "verify":
            possible_values = ["Y", "N", "y", "n"]
            input_valid = False
            while input_valid is False:
                try:
                    user_input = str(input(self.input_disp_text + " (Y/N): "))
                    if user_input and user_input in possible_values:
                        input_valid = True
                except:
                    print("Please try again.")
            
            self.the_user_input = user_input
            return
        
        if self.input_type == "str":
            input_valid = False
            while input_valid is False:
                try:
                    user_input = str(input(self.input_disp_text + ": "))
                    if user_input:
                        input_valid = True
                except:
                    print("Please try again.")

            self.the_user_input = user_input
            return

        if self.input_type == "person_type":
            possible_values = ["s", "S", "t", "T"]
            input_valid = False
            while input_valid is False:
                try:
                    user_input = str(input(self.input_disp_text + ": "))
                    if user_input and user_input in possible_values:
                        input_valid = True
                except:
                    print("Please try again.")
            self.the_user_input = user_input

class MenuController():
    def __init__(self):
        #[{name: "", courses: ["", ""], students: ["", ""]}]
        self.teacher_list = list()

        #[{name: "", courses: ["", ""], teachers: ["",""]}]
        self.student_list = list()

        #["courseName1", etc]
        self.course_list = list()
        self.done = False

        self.user_choice = 0

    def search(self, the_type=None, the_item=None, the_list=None, the_key=None):
        item_exists = False
        for an_item in the_list:
            if the_type == "list":
                if an_item == the_item:
                    item_exists = True

            elif the_type == "dict_in_list":
                if an_item[the_key] == the_item:
                    item_exists = True

        return item_exists
        
    def run(self):
        print("Running")
        
        while self.done is False:
            self.disp_action_menu()
            possible_choices = [1,2,3,4,5,6,7]

            self.user_choice = TakeInput("int", "Insert Choice").the_user_input
            self.redirect_user()

    def add_course(self):
        course_name = input("What is the name of the new course?")
        course_exists = self.search("dict_in_list", course_name, self.course_list, "Course")
        if course_exists:
            print("This course already exists in the system.")
            print("You will be redirected to the main menu.")
        else:
            new_course = Course(course_name)
            self.course_list.append(new_course.identity)
    
    def add_person(self):
        #Create person and append to list
        print("Is this person a student or a teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student or "t" for teacher').the_user_input
                
        if person_type == "s" or person_type == "S":
            the_list = self.student_list
        elif person_type == "t" or person_type == "T":
            the_list = self.teacher_list

        person_name = input("What is the name of the new person?: ")
        student_exists = self.search("dict_in_list", person_name, self.student_list, "Name")
        if student_exists:
            print("This student already exists in the system.")
        else:
            new_person = Person(person_name).identity
            the_list.append(new_person)
            print("The new person has been added to the system.")

        if person_type == "s" or person_type == "S":
            self.student_list = the_list
        elif person_type == "t" or person_type == "T":
            self.teacher_list = the_list

    def remove_course(self):
        the_course = input("What course do you want to remove?: ")
        course_exists = self.search("dict_in_list", the_course, self.course_list, "Course")
        if course_exists:
            #do two passes, one for student list, one for teacher list
            passes = 0
            while passes < 2:
                if passes == 0:
                    the_list = self.student_list
                elif passes == 1:
                    the_list = self.teacher_list

                for person in the_list:
                    person_courses = person["Courses"]
                    for course in person_courses:
                        if course == the_course:
                            person_courses.pop(the_course)
                
                passes += 1

            for a_course in self.course_list:
                if a_course["Course"] == the_course:
                    self.course_list.remove(a_course)
            print("The course has successfully been removed from the system.")

        else:
            print("This course does not exist in the system.")
            print("You will be redirected to the main menu.")

    def remove_person(self):
        #remove person from course, student, and teacher lists
        print("Is this person a student or teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student or "t" for teacher').the_user_input

        if person_type == "s" or person_type == "S":
            the_list = self.student_list
            person_course_key = "Students"
            the_person_type = "student"

        elif person_type == "t" or person_type == "T":
            the_list = self.teacher_list
            person_course_key = "Teachers"
            the_person_type = "teacher"

        the_person = input("What is the name of the person?: ")
        #remove the student from all lists
        person_exists = self.search("dict_in_list", the_person, the_list, "Name")
        if person_exists:
            #remove student from all lists
            for a_course in self.course_list:
                people_in_course = a_course[person_course_key]
                for a_person in people_in_course:
                    if a_person == the_person:
                        people_in_course.remove(the_person)

            student_done = False
            teacher_done = False
            for person in the_list:
                if person["Name"] == the_person:
                    the_list.remove(person)

            if the_person_type == "student":
                student_done = True
            elif the_person_type == "teacher":
                teacher_done = True
            
            if student_done == False:
                the_list = self.student_list
            elif teacher_done == False:
                the_list = self.teacher_list

            for person in the_list:
                courses = person["Courses"]
                for course_key in courses:
                    people_in_course = courses[course_key]
                    for a_person in people_in_course:
                        if a_person == the_person:
                            people_in_course.remove(a_person)

            print("Person", the_person, "has been removed.")
        else:
            print("This person does not exist in the system.")
    
    def assign_course(self):
        #Get course name first
        course_exists = False
        while course_exists is False:
            course_name = TakeInput("str", "What is the name of the course?").the_user_input
            course_exists = self.search("dict_in_list", course_name, self.course_list, "Course")
            if course_exists is False:
                print("This course does not exist in the system. Please try again.")

        print("Is the course being assigned to a student or a teacher?")
        
        person_type = TakeInput("person_type", 'Input "s" for student and "t" for teacher').the_user_input
        if person_type == "s" or person_type == "S":
            the_list = self.student_list
        elif person_type == "t" or person_type == "T":
            the_list = self.teacher_list
            
        person_exists = False
        while person_exists is False:    
            person_name = input("What is the name of the person?: ")
            person_exists = self.search("dict_in_list", person_name, the_list, "Name")
            if person_exists is False:
                print("This person does not exist in the system. Please try again.")
        
        for person in the_list:
            if person["Name"] == person_name:
                person["Courses"][course_name] = []
            
        if person_type == "s" or person_type == "S":
            self.student_list = the_list
            for course in self.course_list:
                if course["Course"] == course_name:
                    course["Students"].append(person_name)

            # other_type_list = self.teacher_list
        elif person_type == "t" or person_type == "T":
            self.teacher_list = the_list
            for course in self.course_list:
                if course["Course"] == course_name:
                    course["Teachers"].append(person_name)
            # other_type_list = self.student_list

    def unassign_course(self):
        course_exists = False
        while course_exists is False:
            course_name = TakeInput("str", "What is the name of the course?").the_user_input
            course_exists = self.search("dict_in_list", course_name, self.course_list, "Course")
            if course_exists is False:
                print("This course does not exist in the system. Please try again.")
        
        print("Is the course being unassigned from a student or teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student and "t" for teacher').the_user_input

        if person_type == "s" or person_type == "S":
            the_list = self.student_list
        elif person_type == "t" or person_type == "T":
            the_list = self.teacher_list

        person_exists = False
        while person_exists is False:    
            person_name = input("What is the name of the person?: ")
            person_exists = self.search("dict_in_list", person_name, the_list, "Name")
            if person_exists is False:
                print("This person does not exist in the system. Please try again.")

        for person in the_list:
            if person["Name"] == person_name:
                person["Courses"].pop(course_name)
        
        #Unassign course in the course list for person
        #TODO
        if person_type == "s" or person_type == "S":
            self.student_list = the_list
            key = "Students"
        elif person_type == "t" or person_type == "T":
            self.teacher_list = the_list
            key = "Teachers"
        
        for course in self.course_list:
            for person in course[key]:
                if person == person_name:
                    course[key].remove(person)

    def get_max_lengths(self):
        #courses, teachers, students
        max_lengths = [7,8,8]

        for row in self.course_list:
            if len(row["Course"]) > max_lengths[0]:
                max_lengths[0] = len(row["Course"])

            for item in row["Teachers"]:
                if len(item) > max_lengths[1]:
                    max_lengths[1] = len(item)

            for item in row["Students"]:
                if len(item) > max_lengths[2]:
                    max_lengths[2] = len(item)

        passes = 0
        while passes < 2:
            if passes == 0:
                the_list = self.student_list
                compare_value = max_lengths[2]
                other_person_length = max_lengths[1]
            elif passes == 1:
                the_list = self.teacher_list
                compare_value = max_lengths[1]
                other_person_length = max_lengths[2]

            for row in the_list:
                if len(row["Name"]) > compare_value:
                    compare_value = len(row["Name"])

                for course in row["Courses"]:
                    if len(course) > max_lengths[0]:
                        max_lengths[0] = len(course)

                    if len(row["Courses"][course]) > other_person_length:
                        other_person_length = len(row["Courses"][course])
            
            if passes == 0:
                max_lengths[2] = compare_value
                max_lengths[1] = other_person_length
            elif passes == 1:
                max_lengths[1] = compare_value
                max_lengths[2] = other_person_length
            
            passes +=1
        
        return max_lengths
        
    def disp_info(self):
        print("ALL STUDENTS AND TEACHERS ENROLLED IN A COURSE")
        max_lengths = self.get_max_lengths()

        print(
            "╔" + max_lengths[0] * "═" +
            "╦" + max_lengths[1] * "═" +
            "╦" + max_lengths[2] * "═" +
            "╗"
        )
        print(
            "║" +
            "Course" + " " * (max_lengths[0]-6) + "║" + 
            "Teachers" + " " * (max_lengths[1]-8) + "║" +
            "Students" + " " * (max_lengths[2]-8) + 
            "║"
        )
        print(
            "╠" + (max_lengths[0] * "═") +
            "╬" + (max_lengths[1] * "═") +
            "╬" + (max_lengths[2] * "═") +
            "╣"
        )
        
        for course in self.course_list:
            print(
                "║" + course["Course"] + " " * (max_lengths[0]-len(course["Course"])) +
                "║" + " " * max_lengths[1] +
                "║" + " " * max_lengths[2] + "║"
            )
            for teacher in course["Teachers"]:
                print(
                    "║" + " " * max_lengths[0] + 
                    "║" + teacher + " " * (max_lengths[1]-len(teacher)) +
                    "║" + " " * max_lengths[2] + "║"
                )

            for student in course["Students"]:
                print(
                    "║" + " " * max_lengths[0] +
                    "║" + " " * max_lengths[1] +
                    "║" + student + " " * (max_lengths[2]-len(student)) + "║"
                )
            print(
                "╟" + (max_lengths[0] * "═") +
                "╫" + (max_lengths[1] * "═") +
                "╫" + (max_lengths[2] * "═") +
                "╫"
            )
        print(
            "╚" + (max_lengths[0] * "═") +
            "╩" + (max_lengths[1] * "═") +
            "╩" + (max_lengths[2] * "═") +
            "╝"
        )

        print("---")

        print("ALL COURSES:")
        print("╔" + max_lengths[0] * "═" + "╗")
        for course in self.course_list:
            print("║" + course["Course"] + " " * (max_lengths[0] - len(course["Course"])) + "║")

        print("╚" + (max_lengths[0] * "═") + "╝")

        print("---")

        print("ALL TEACHERS:")
        print("╔" + max_lengths[1] * "═" + "╗")
        for teacher in self.teacher_list:
            print("║" + teacher["Name"] + " " * (max_lengths[1] - len(teacher["Name"])) + "║")

        print("╚" + (max_lengths[1] * "═") + "╝")

        print("---")

        print("ALL STUDENTS:")
        print("╔" + max_lengths[2] * "═" + "╗")
        for student in self.student_list:
            print("║" + student["Name"] + " " * (max_lengths[2] - len(student["Name"])) + "║")

        print("╚" + (max_lengths[2] * "═") + "╝")

        print("---")

    def disp_action_menu(self):
        print(
            '''
            Welcome to the school simulation!

            1) Add a course to the system
            2) Add a person (teacher or student)
            3) Remove a course from the system
            4) Remove a person (teacher or student)
            5) Assign a course
            6) Unassign a course
            7) Display the courses, teachers, and students
            8) Quit
            '''
        )
    
    def redirect_user(self):
        if self.user_choice == 1:
            self.add_course()

        elif self.user_choice == 2:
            self.add_person()

        elif self.user_choice == 3:
            self.remove_course()

        elif self.user_choice == 4:
            self.remove_person()

        elif self.user_choice == 5:
            self.assign_course()

        elif self.user_choice == 6:
            self.unassign_course()
        
        elif self.user_choice == 7:
            self.disp_info()
        
        elif self.user_choice == 8:
            self.quit()

    def quit(self):
        print("Have a nice day.")
        sys.exit()

the_menu = MenuController()
the_menu.run()