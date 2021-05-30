import sqlite3


class GroupDataBase:

    def __init__(self, file):
        self.groupFile = file
        self.conn = sqlite3.connect(self.groupFile)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS students (FIO text NOT NULL PRIMARY KEY, Group_Name text NOT NULL, ID int NOT NULL UNIQUE)''')
        self.conn.commit()

    def insert_data(self,  FIO, Group_Name, ID):
        self.c.execute('''INSERT INTO students(FIO, Group_Name, ID) VALUES (?, ?, ?)''', (FIO, Group_Name, ID))
        self.conn.commit()

    def reopen(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.groupFile)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS students (FIO text NOT NULL PRIMARY KEY, Group_Name text NOT NULL, ID int NOT NULL UNIQUE)''')
        self.conn.commit()

    def save(self, file):
        save = sqlite3.connect(file)
        with save:
            self.conn.backup(save)
        save.close()


class SubjectDataBase:

    def __init__(self, file):
        self.subjectFile = file
        self.conn = sqlite3.connect(self.subjectFile)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS info (GROUP_NAME text  PRIMARY KEY)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS subject (ID int NOT NULL PRIMARY KEY, DATES text NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS lessons (DATES text NOT NULL PRIMARY KEY)''')
        self.conn.commit()

    def insert_data(self, ID, DATES):
        self.c.execute('''INSERT INTO subject(ID, DATES) VALUES (?, ?)''', (ID, DATES))
        self.conn.commit()

    def add_lesson(self, DATE):
        self.c.execute('''INSERT INTO lessons(DATES) VALUES (?)''', (DATE,))
        self.conn.commit()

    def set_group_name(self, GROUP_NAME):
        self.c.execute('''INSERT INTO info(GROUP_NAME) VALUES (?)''', (GROUP_NAME,))
        self.conn.commit()

    def reopen(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.subjectFile)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS info (Group_Name text  PRIMARY KEY)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS subject (ID int NOT NULL PRIMARY KEY, VISIT_DATES text NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS lessons (DATE text NOT NULL PRIMARY KEY)''')
        self.conn.commit()

    def save(self, file):
        save = sqlite3.connect(file)
        with save:
            self.conn.backup(save)
        save.close()