import sys, sqlite3, faker, logging
from prettytable import PrettyTable

class Item:
    def __init__(self, name=None):
        self.name = name

'''
** New Data Structure**

courses     [[1, 1, 2, "CS2"]]
course_id INTEGER PRIMARY KEY	student_id PRIMARY KEY	    teacher_id PRIMARY KEY	    course_name TEXT

students    [[1, "Devansh Agrawal"]]			
student_id INTEGER PRIMARY KEY AUTOINCREMENT	student_name TEXT

teachers    [[2, "Dev Ag"]]
teacher_id INTEGER PRIMARY KEY AUTOINCREMENT    teacher_name TEXT

'''


'----------------------------'
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

        if self.input_type == "id":
            while input_valid is False:
                try:
                    user_input = int(input(self.input_disp_text + ": #"))
                    if user_input:
                        input_valid = True
                except:
                    print("Please try again.")
            self.the_user_input = user_input

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

        return
class Controller():
    def __init__(self):
        self.database = Database()
        self.database.create_tables()
        
        #self.school_actions = SchoolActions()
        self.menu = Menu()

        self.done = False

        self.user_choice = 0
        
    def run(self):
        while self.done is False:
            print('---')
            #goes through options dict, prints the data out per entry
            for i, option in self.menu.options.items():
                print(f'{i}) {option["desc"]}')

            print('')
            choice_valid = False
            while choice_valid == False:
                self.user_choice = TakeInput("int", "Insert Choice").the_user_input
                if self.user_choice in range(1,9):
                    choice_valid = True

            self.menu.options.get(self.user_choice)['action']()

class Database():
    def __init__(self, action=None):
        self.conn = sqlite3.connect("school.db")
        self.c =  self.conn.cursor()
        self.action = action

    def create_tables(self):
        self.c.executescript(
            '''
                CREATE TABLE IF NOT EXISTS courses(
                    course_id INTEGER PRIMARY KEY,
                    student_id INTEGER,
                    teacher_id INTEGER,
                    course_name TEXT
                );

                CREATE TABLE IF NOT EXISTS students(
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT
                );

                CREATE TABLE IF NOT EXISTS teachers(
                    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_name TEXT
                )
            '''
        )

        self.conn.commit()

    def read_and_return(self):
        courses = self.c.execute(
            '''
                SELECT * FROM courses
            '''
        )
        courses_data = courses.fetchall()
        
        
        students = self.c.execute(
            '''
                SELECT * FROM students
            '''
        )
        students_data = students.fetchall()
        


        teachers = self.c.execute(
            '''
                SELECT * FROM teachers
            '''
        )
        teachers_data = teachers.fetchall()

        the_data = [courses_data, students_data, teachers_data]
        for data in the_data:
            index = 0
            while index < len(data):
                data[index] = list(data[index])
                index += 1

        return courses_data, students_data, teachers_data

    def wipe_and_update(self, course_list=None, student_list=None, teacher_list=None):
        #updated lists will update db tables
        #delete table data, replace with new

        self.c.executescript(
            '''
                DELETE FROM courses;
                DELETE FROM students;
                DELETE FROM teachers;
            '''
        )
        self.conn.commit()
        for course in course_list:
            self.c.execute(
                f'''
                    INSERT INTO courses(course_id, student_id, teacher_id, course_name)
                    VALUES({course[0]},{course[1]},{course[2]},{course[3]});
                '''
            )
            self.conn.commit()

        for student in student_list:
            self.c.execute(
                f'''
                    INSERT INTO students(student_id, student_name)
                    VALUES({student[0]},{student[1]});
                '''
            )
            self.conn.commit()

        for teacher in teacher_list:
            self.c.execute(
                f'''
                    INSERT INTO teachers(teacher_id, teacher_name)
                    VALUES({teacher[0]},{teacher[1]});
                '''
            )
            self.conn.commit()

    def keep_and_update(self):
        #keep the data, update specific record
        pass

    def remove_item(self, item_type, the_id):
        if item_type == 'course':
            #remove course
            self.c.execute(f'DELETE FROM courses WHERE course_id={the_id}')
            self.conn.commit()

        elif item_type == 'student':
            #remove course
            self.c.execute(f'DELETE FROM students WHERE student_id={the_id}')
            self.conn.commit()

        elif item_type == 'teacher':
            self.c.execute(f'DELETE FROM teachers WHERE teacher_id={the_id}')
            self.conn.commit()

    def insert_item(self, item_type, new_data):
        if item_type == 'course':
            self.c.execute(
                '''
                    INSERT INTO courses(course_name)
                    VALUES(?);
                ''', [new_data]
            )
            self.conn.commit()

        elif item_type == 'student':
            self.c.execute(
                '''
                    INSERT INTO students(student_name)
                    VALUES(?);
                ''', [new_data]
            )
            self.conn.commit()

        elif item_type == 'teacher':
            self.c.execute(
                '''
                    INSERT INTO teachers(teacher_name)
                    VALUES(?);
                ''', [new_data]
            )
            self.conn.commit()

    def testing(self):
        #This is the testing method that will add values to the table when testing.
        self.c.execute(
            '''
                INSERT INTO students(student_name)
                VALUES(
                    "Dev Ag"
                )
            '''
        )
        self.conn.commit()

class SchoolActions():
    def __init__(self):
        self.database = Database()

    def search(self, check_value=None, a_list=None, list_name_index=None):
        #check_value is string value of item name
        #check_id is the index of item name
        #a_list is the list that is being inspected
        #list_name_index is the index in a_list that contains the string value of item name
        '''item_exists = False
        for an_item in a_list:
            if check_value == an_item[list_name_index] and check_id == an_item[list_id_index]:
                item_exists = True
        
        return item_exists'''

        hits = []
        item_exists = False
        for an_item in a_list:
            #print(a_list[list_name_index])
            #print(check_value)
            if check_value == an_item[list_name_index]:
                item_exists = True
                hits.append(an_item)
        
        return item_exists, hits

    def add_course(self):
        course_name = input("What is the name of the new course?: ")
        self.database.insert_item('course', course_name)
    
    def add_person(self):
        print("Is this person a student or a teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student or "t" for teacher').the_user_input
        courses, students, teachers = self.database.read_and_return()
        person_name = input("What is the name of the new person?: ")
        #self.database.testing()
        if person_type.lower() == "s":
            self.database.insert_item('student', person_name)

        elif person_type.lower() == "t":
            self.database.insert_item('teacher', person_name)

    def remove_course(self):
        courses, students, teachers = self.database.read_and_return()

        the_course = input("What course do you wish to remove?: ")
        #first check if exists
        exists, results = self.search(the_course, courses, 3)
        if exists:
            #show hits, ask for id, remove this person
            plurality = ""
            if len(results) > 1:
                plurality1 = "are"
                plurality2 = "courses"
            else:
                plurality1 = "is"
                plurality2 = "course"

            print(f'There {plurality1} {len(results)} {plurality2} with this name.')

            results_table = PrettyTable()
            results_table.field_names = ["ID", "Name"]
            possible_ids = []
            for the_id, the_student_id, the_teacher_id, name in results:
                results_table.add_row([f'#{the_id}', name])
                possible_ids.append(the_id)
            print(results_table)
            
            print(possible_ids)
            id_input_valid = False
            while id_input_valid == False:
                remove_id = TakeInput("id", "Which ID course do you wish to remove?").the_user_input
                print(remove_id)
                if remove_id in possible_ids:
                    id_input_valid = True

            self.database.remove_item('course', remove_id)

        else:
            print("This course does not exist in the system.")

        '''
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
        '''
    def remove_person(self):
        #-------
        #######'STILL NEED TO FINISH'#########
        #TODO: remove from course list

        #remove person from student list with corresponding student id in course list.
        courses, students, teachers = self.database.read_and_return()

        print("Is this person a student or teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student or "t" for teacher').the_user_input
        if person_type.lower() == "s":
            the_list = students
            course_id_index = 1
        else:
            the_list = teachers
            course_id_index = 2

        the_person = input("What is the name of the person?: ")
        #search for person
        exists, results = self.search(the_person, the_list, 1)
        print(exists, results, the_person, the_list)
        if exists:
            #show hits, ask for id, remove this person
            plurality = ""
            if len(results) > 1:
                plurality1 = "are"
                plurality2 = "people"
            else:
                plurality1 = "is"
                plurality2 = "person"

            print(f'There {plurality1} {len(results)} {plurality2} with this name.')

            results_table = PrettyTable()
            results_table.field_names = ["ID", "Name"]
            possible_ids = []
            for the_id, name in results:
                results_table.add_row([f'#{the_id}', name])
                possible_ids.append(the_id)
            print(results_table)
            
            print(possible_ids)
            id_input_valid = False
            while id_input_valid == False:
                remove_id = TakeInput("id", "Which ID person do you want to remove?").the_user_input
                print(remove_id)
                if remove_id in possible_ids:
                    id_input_valid = True
            
            if person_type.lower() == "s":
                self.database.remove_item('student', remove_id)
            else:
                self.database.remove_item('teacher', remove_id)
            
        else:
            print("This person does not exist in the system")

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

    def quit(self):
        print("Have a nice day.")
        sys.exit()

class Menu():
    def __init__(self):
        self.database = Database()
        self.course_list, self.student_list, self.teacher_list = self.database.read_and_return()
        self.school_actions = SchoolActions()
        self.options = {
            1 : {'desc': 'Add a course to the system', 'action': lambda: self.school_actions.add_course()},
            2 : {'desc': 'Add a person (teacher or student)', 'action': lambda: self.school_actions.add_person()},
            3 : {'desc': 'Remove a course from the system', 'action': lambda: self.school_actions.remove_course()},
            4 : {'desc': 'Remove a person (teacher or student)', 'action': lambda: self.school_actions.remove_person()},
            5 : {'desc': 'Assign a course', 'action': lambda: self.school_actions.assign_course()},
            6 : {'desc': 'Unassign a course', 'action': lambda: self.school_actions.unassign_course()},
            7 : {'desc': 'Display the courses, teachers, and students', 'action': lambda: self.disp_info()},
            8 : {'desc': 'Quit', 'action': lambda: self.school_actions.quit()}
        }
    
    def id_to_name(self, id, check_list, list_index_id, list_index_name):
        #check_list is the list that the id is being checked against for the name
        #list_index id is the check_list index that has the id
        #list_index_name is the check_list index that has the name

        for person in check_list:
            if id == check_list[list_index_id]:
                return check_list[list_index_name]

    def string_to_list(self, the_string):
        a_list = the_string.split(',')
        return a_list
        
    def list_to_string(self, the_list):
        a_string = ''
        for item in the_list:
            a_string = a_string + item + ","
        a_string = a_string[:-1]
        return 

    def disp_info(self):
        course_table = PrettyTable()
        student_table = PrettyTable()
        teacher_table = PrettyTable()
        course_table.field_names = ["Course ID", "Students Taking Course", "Teachers in Course", "Course Name"]
        student_table.field_names = ["Student ID", "Student Name"]
        teacher_table.field_names = ["Teacher Id", "Teacher Name"]

        courses, students, teachers = self.database.read_and_return()
        print(courses, students, teachers)

        #student_names_list = self.string_to_list(students)
        #teacher_names_list = self.string_to_list(teachers)
        for course in courses:
            student_names = list()
            teacher_names = list()
            student_names_string = ""
            teacher_names_string = ""

            if course[1]:
                student_ids_list = self.string_to_list(course[1])
                for student_id in student_ids_list:
                    student_name = self.id_to_name(student_id, students, 0, 1)
                    student_names.append(student_name)
                student_names_string = self.list_to_string(student_names)
            
            if course[2]:
                teacher_ids_list = self.string_to_list(course[2])
                for teacher_id in teacher_ids_list:
                    teacher_name = self.id_to_name(teacher_id, teachers, 0, 1)
                    teacher_names.append(teacher_name)
                teacher_names_string = self.list_to_string(teacher_names)

            
            course_table.add_row([course[0], student_names_string, teacher_names_string, course[3]])

        for student in students:
            student_table.add_row(student)

        for teacher in teachers:
            teacher_table.add_row(teacher)

        if students:
            print(student_table)
        else:
            print("There are no students in the system.")

        if teachers:
            print(teacher_table)
        else:
            print("There are no teachers in the system.")

        if courses:
            print(course_table)
        else:
            print("There are no courses in the system.")

program = Controller()
program.run()