import sys, sqlite3, faker, logging
from prettytable import PrettyTable

class Item:
    def __init__(self, name=None):
        self.name = name

'''
** New Data Structure**

courses     [[1, 1, 2, "CS2"]]
course_id INTEGER PRIMARY KEY AUTOINCREMENT     student_ids TEXT	    teacher_ids TEXT	    course_name TEXT

students    [[1, "Devansh Agrawal"]]			
student_id INTEGER PRIMARY KEY AUTOINCREMENT	student_name TEXT

teachers    [[2, "Dev Ag"]]
teacher_id INTEGER PRIMARY KEY AUTOINCREMENT    teacher_name TEXT

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

        return self.the_user_input
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
                    student_ids TEXT,
                    teacher_ids TEXT,
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

    """
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
                    INSERT INTO courses(course_id, student_ids, teacher_ids, course_name)
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
    """

    def update_data(self, update_id, new_data, item_type):
        #update_id: id of course
        #new_data: the new student and teacher ids strings
        
        if item_type == "course":
            print(update_id, new_data, item_type)
            #update data
            self.c.execute(
                f'''
                    UPDATE courses
                    SET
                        student_ids = '{new_data[1]}', 
                        teacher_ids = CASE
                            WHEN '{new_data[2]}' = 'None'
                                THEN NULL
                            WHEN '{new_data[2]}' = ''
                                THEN NULL
                            ELSE '{new_data[2]}'
                        END
                    WHERE course_id = {update_id};
                '''
            )
            self.conn.commit()

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
        #a_list is the list that is being inspected
        #list_name_index is the index in a_list that contains the string value of item name

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
        course_exists, the_remove_id = self.item_remover("course")
        if course_exists:
            self.database.remove_item('course', the_remove_id)

    def print_search_results(self, results, item_type):
        plurality = ""
        if len(results) > 1:
            plurality1 = "are"
            if item_type == "student" or item_type == "teacher":
                plurality2 = "people"
            else:
                plurality2 = "courses"
        else:
            plurality1 = "is"
            if item_type == "student" or item_type == "teacher":
                plurality2 = "person"
            else:
                plurality2 = "course"

        print(f'There {plurality1} {len(results)} {plurality2} with this name.')

        results_table = PrettyTable()
        results_table.field_names = ["ID", "Name"]
        possible_ids = []
        if item_type == "student" or item_type == "teacher":
            print(results)
            for the_id, name in results:
                results_table.add_row([f'#{the_id}', name])
                possible_ids.append(the_id)
        else:
            for the_id, the_student_id, the_teacher_id, name in results:
                results_table.add_row([f'#{the_id}', name])
                possible_ids.append(the_id)
        print(results_table)
        return possible_ids

    def item_remover(self, item_type):
        #This will condense remove_person() and remove_course()
        print('students')
        print(item_type)
        courses, students, teachers = self.database.read_and_return()
        if item_type == "course":
            the_list = courses
            item_index = 3
        elif item_type == "student":
            the_list = students
            item_index = 1
        elif item_type == "teacher":
            the_list = teachers
            item_index = 1

        the_item = input(f"What is the name of the {item_type}?: ")
        #search for person
        exists, results = self.search(the_item, the_list, item_index)
        print(exists, results, the_item, the_list)
        if exists:
            possible_ids = self.print_search_results(results, item_type)
            
            print(possible_ids)
            remove_id = self.get_item_id(item_type, possible_ids)
            
            return exists, remove_id

        else:
            print(f"This {item_type} does not exist in the system")
            return exists, None

    def get_item_id(self, item_type, possible_ids):
        id_input_valid = False
        while id_input_valid == False:
            item_id = TakeInput("id", f"Which ID {item_type} do you wish to act on?").the_user_input
            print(item_id)
            if item_id in possible_ids:
                id_input_valid = True
        
        return item_id

    def check_person_in_course(self, courses, course_id, person_id, search_index):
        #checks if person is in course
        #get course people string, convert to list, check if person_id in this list
        for course in courses:
            if course[0] == course_id:
                the_course = course
        
        person_exists_in_course = False
        string_options = Menu()
        ids_list = string_options.string_to_list(the_course[search_index])
        print(ids_list)
        print(person_id)
        if str(person_id) in ids_list:
            person_exists_in_course = True
        
        return person_exists_in_course

    def course_actions(self, person_type, person_id, action_type, course_id=None):
        courses, students, teachers = self.database.read_and_return()
        for a_course in courses:
            if a_course[0] == course_id:
                the_course = a_course

        if person_type.lower() == "s":
            people_ids_string = a_course[1]
        else:
            people_ids_string = a_course[2]

        string_options = Menu()
        people_ids_list = string_options.string_to_list(people_ids_string)
        
        if action_type == 'remove':
            for a_person_id in people_ids_list:
                if int(a_person_id) == person_id:
                    people_ids_list.remove(a_person_id)
        
        elif action_type == 'assign':
            print(person_id, people_ids_list)
            if str(person_id) in people_ids_list:
                print("This person already is in this course.")
                return
            else:
                people_ids_list.append(person_id)
        
        new_people_ids_string = string_options.list_to_string(people_ids_list)
        
        if person_type.lower() == "s":
            the_course[1] = new_people_ids_string
        else:
            the_course[2] = new_people_ids_string
        
        '''
        for course_index in range(len(courses)):
            if courses[course_index][0] == course_id:
                courses[course_index] = the_course
        '''

        self.database.update_data(course_id, the_course, "course")

    def remove_person(self):
        #-------
        #######'STILL NEED TO FINISH'#########
        #TODO: remove from course list

        #courses, students, teachers = self.database.read_and_return()

        print("Is this person a student or teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student or "t" for teacher').the_user_input
        if person_type.lower() == "s":
            #the_list = students
            the_person_type = 'student'
        else:
            #the_list = teachers
            the_person_type = 'teacher'

        person_exists, the_remove_id = self.item_remover(the_person_type)

        if person_exists:
            if person_type.lower() == "s":
                self.database.remove_item('student', the_remove_id)
            else:
                self.database.remove_item('teacher', the_remove_id)

    def assign_course(self):
        courses, students, teachers = self.database.read_and_return()

        course_exists = False
        while course_exists is False:
            course_name = input("What is the name of the course?: ")
            course_exists, course_results = self.search(course_name, courses, 3)
        
        course_possible_ids = self.print_search_results(course_results, "course")
        course_id = self.get_item_id('course', course_possible_ids)

        print('Is this course being assigned to a student or teacher?')
        person_type = TakeInput('person_type', 'Input "s" for student and "t" for teacher').the_user_input
        
        if person_type.lower() == "s":
            the_person_type = 'student'
            the_list = students
            search_index = 1
        else:
            the_person_type = 'teacher'
            the_list = teachers
            search_index = 2
        
        person_exists = False
        while person_exists is False:
            person_name = input("What is the name of this person?: ")
            person_exists, person_results = self.search(person_name, the_list, 1)
            if person_exists is False:
                print(f'Person {person_name} does not exist the system. Please try again.')
            
        person_possible_ids = self.print_search_results(person_results, the_person_type)
        #get_item_id, change course person ids.
        person_id = self.get_item_id(the_person_type, person_possible_ids)
        
        #see if person exists in course. If so, then exit out of method
        
        self.course_actions(person_type, person_id, 'assign', course_id)
        '''
        person_exists_course, results = self.search(str(person_name), courses, int(search_index))
        print(person_exists_course, results)
        if person_exists_course:
            print(f'Person {person_name} already exists in course {course_name}. You will now be redirected to the main menu.')

        
        if person_exists_course is False:
            self.course_actions(person_type, person_id, 'assign', course_id)
        else:
            return
        '''
    def unassign_course(self):
        courses, students, teachers = self.database.read_and_return()
        course_exists = False
        while course_exists is False:
            course_name = TakeInput("str", "What is the name of the course?").the_user_input
            course_exists, course_results = self.search(course_name, courses, 3)
            if course_exists is False:
                print("This course does not exist in the system. Please try again.")
            if course_exists is True:
                break
        
        course_possible_ids = self.print_search_results(course_results, "courses")
        the_remove_course_id = self.get_item_id('course', course_possible_ids)

        print("Is the course being unassigned from a student or teacher?")
        person_type = TakeInput("person_type", 'Input "s" for student and "t" for teacher').the_user_input
        if person_type == "s" or person_type == "S":
            #the_list = self.student_list
            the_person_type = 'student'
            search_index = 1
        elif person_type == "t" or person_type == "T":
            the_person_type = 'teacher'
            #the_list = self.teacher_list
            search_index = 2

        person_exists = False
        while person_exists is False:
            #person_id = self.get_item_id(the_person_type, person_possible_ids)
            person_name = input("What is the name of the person?: ")
            #need to split up string
            person_exists, person_results = self.search(person_name, students, 1)
            if person_exists is False:
                print(f'Person {person_name} does not exist in the system. Please try again.')
        
        print(person_results)
        person_possible_ids = self.print_search_results(person_results, the_person_type)
        the_remove_person_id = self.get_item_id(the_person_type, person_possible_ids)

        #check if person in course through ids
        person_in_course = self.check_person_in_course(courses, the_remove_course_id, the_remove_person_id, search_index)
        if person_in_course:
            self.course_actions(person_type, the_remove_person_id, 'remove', the_remove_course_id)
        else:
            print(f'Person {person_name} does not exist in course {course_name}.')
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
    
    def id_to_name(self, the_id, check_list, list_index_id, list_index_name):
        #the_id is the id of the item in general
        #check_list is the list that the id is being checked against for the name
        #list_index_id is the check_list index that has the id
        #list_index_name is the check_list index that has the name
        print("checklist", check_list)
        for person in check_list:
            print("id stuff: ", person[list_index_name])
            print("checking", the_id, person[list_index_id])
            #print(int(the_id) is int(person[list_index_id]))
            if int(the_id) == int(person[list_index_id]):
                print('it works')
                #return_value = person[list_index_name]
                return person[list_index_name]

    def string_to_list(self, the_string):
        if the_string is not None:
            a_list = the_string.split(',')
        else:
            a_list = list()
        return a_list
        
    def list_to_string(self, the_list):
        if not the_list:
            return ''
            
        for item in the_list:
            if item == '':
                the_list.remove(item)
        a_string = ''
        for item in the_list:
            a_string = a_string + str(item) + ","
            print("first part", a_string)
        a_string = a_string[:-1]
        print("a_string: ", a_string)
        return a_string

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
                print("student_ids_list:", student_ids_list)
                for student_id in student_ids_list:
                    student_name = self.id_to_name(student_id, students, 0, 1)
                    print(student_name)
                    student_names.append(student_name)
                    print(student_name)
                student_names_string = self.list_to_string(student_names)
            
            if course[2] is not None:
                print('course[2] is ', course[2])
                teacher_ids_list = self.string_to_list(course[2])
                for teacher_id in teacher_ids_list:
                    teacher_name = self.id_to_name(teacher_id, teachers, 0, 1)
                    teacher_names.append(teacher_name)
                teacher_names_string = self.list_to_string(teacher_names)
            
            print([course[0], student_names_string, teacher_names_string, course[3]])
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