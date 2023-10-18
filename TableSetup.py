import argparse
import sqlite3
import os


dbfile = os.path.join(os.getcwd(), "instance", "database.db")
tablefile = "CreateTables.sql"

def Connection():
    """
    Connection object to the database file.

    Trys to open database file
    If it fails it trys to create a new database file
    If it succeeds it creates a cursor object and returns the database connection object and cursor objects
    """
    try:
        with sqlite3.connect(dbfile) as db:
            cur = db.cursor()
            return db, cur
    except Exception as e:
        print(f"{e}: Error connecting to database file, trying to create file")
        try:
            f = open(dbfile, "w").close()
        except Exception as e:
            print(f"{e}: Error creating database file")

def CreateTables(db, cur):
    """
    Takes database connections and cursor object

    Opens the CreateTables.sql file, splits at every double new line character, the end of a line and a blank line, and iterates over that list and executes each statement.
    """
    print('Creating Tables')
    with open(tablefile, 'r') as f:
        l = f.read().split("\n\n")
        for command in l:
            #print(command)
            cur.executescript(command)

def RecreateDBFile():
    """
    Brute force way to make a db backup before recreating a fresh instance, must not be connected to the database is VSCode or any other viewer. Should be used cautiously could delete data accidentally
    """
    print("Recreating DB File")
    if os.path.exists(dbfile):
        os.replace(dbfile, dbfile + ".bak")
        f = open(dbfile, "w").close()
    else:
        f = open(dbfile, "w").close()

roles = {
    "None": 1,
    "Student": 2,
    "Grader": 3,
    "Lab Instructor": 4,
    "Admin": 5
}

majors = {
    "CS": 1,
    "IT": 2,
    "ECE": 3,
    "EE": 4,
    "BTEC": 5,
    "BSCS": 6,
    "Other": 7
}

degrees = {
    "BS": 1,
    "MS": 2,
    "PhD": 3,
    "Other": 4
}

# https://sse.umkc.edu/docs/degree-sheets/ms-comp-sci-22-23.pdf

courses = {
    'CS 101': {'course': {'name': "Problem Solving and Programming I", 'major': 1}},
    'CS 191': {'course': {'name': "Discrete Structures I", 'major': 1}},
    'CS 201R': {'course': {'name': "Problem Solving and Programming II", 'major': 1}},
    'CS 291': {'course': {'name': "Discrete Structures II", 'major': 1}},
    'CS 303': {'course': {'name': "Data Structures", 'major': 1}},
    'CS 320': {'course': {'name': "Data Communications and Networking", 'major': 1}},
    'CS 349': {'course': {'name': "Java Programming with Applications", 'major': 1}},
    'CS 394R': {'course': {'name': "Applied Probability", 'major': 1}},
    'CS 404': {'course': {'name': "Introduction to Algorithms and Complexity", 'major': 1}},
    'CS 441': {'course': {'name': "Programming Languages: Design and Implementation", 'major': 1}},
    'CS 449': {'course': {'name': "Foundations of Software Engineering", 'major': 1}},
    'CS 456': {'course': {'name': "Human Computer Interface", 'major': 1}},
    'CS 457': {'course': {'name': "Software Architecture: Requirements & Design", 'major': 1}},
    'CS 458': {'course': {'name': "Software Testing and Verification", 'major': 1}},
    'CS 461': {'course': {'name': "Introduction to Artificial Intelligence", 'major': 1}},
    'CS 465R': {'course': {'name': "Introduction to Statistical Learning", 'major': 1}},
    'CS 470': {'course': {'name': "Introduction to Database Management Systems", 'major': 1}},
    'CS 5520': {'course': {'name': "Network Architecture", 'major': 1}},
    'CS 5525': {'course': {'name': "Cloud Computing", 'major': 1}},
    'CS 5552A': {'course': {'name': "Formal Software Specification", 'major': 1}},
    'CS 5565': {'course': {'name': "Introduction to Statistical Learning", 'major': 1}},
    'CS 5573': {'course': {'name': "Information Security & Assurance", 'major': 1}},
    'CS 5590PA': {'course': {'name': "Special Topics", 'major': 1}}, # No Clue what PA is
    'CS 5592': {'course': {'name': "Design & Analysis of Algorithms", 'major': 1}},
    'CS 5596A': {'course': {'name': "Computer Security I: Cryptology", 'major': 1}},
    'CS 5596B': {'course': {'name': "Computer Security II: Applications", 'major': 1}},
    'ECE 216': {'course': {'name': "Engineering Computation", 'major': 3}},
    'ECE 226': {'course': {'name': "Logic Design", 'major': 3}},
    'ECE 228': {'course': {'name': "Introduction to Computer Design", 'major': 3}},
    'ECE 241': {'course': {'name': "Applied Engineering Analysis I", 'major': 3}},
    'ECE 276': {'course': {'name': "Circuit Theory I", 'major': 3}},
    'ECE 302': {'course': {'name': "Electromagnetic Waves and Fields", 'major': 3}},
    'ECE 330': {'course': {'name': "Electronic Circuits", 'major': 3}},
    'ECE 341R': {'course': {'name': "Applied Engineering Analysis II", 'major': 3}},
    'ECE 428R': {'course': {'name': "Embedded Systems", 'major': 3}},
    'ECE 458': {'course': {'name': "Automatic Control System Design", 'major': 3}},
    'ECE 466': {'course': {'name': "Power Systems I", 'major': 3}},
    'ECE 477': {'course': {'name': "Introduction to Wireless Networking", 'major': 3}},
    'ECE 486': {'course': {'name': "Pattern Recognition", 'major': 3}},
    'ECE 5558': {'course': {'name': "Automatic Control System Design", 'major': 3}},
    'ECE 5560': {'course': {'name': "Electric Power Distribution Systems", 'major': 3}},
    'ECE 5567': {'course': {'name': "Power Systems II", 'major': 3}},
    'ECE 5577': {'course': {'name': "Wireless Communications", 'major': 3}},
    'ECE 5578': {'course': {'name': "Multimedia Communication", 'major': 3}},
    'ECE 5586': {'course': {'name': "Pattern Recognition", 'major': 3}},
    'IT 222': {'course': {'name': "Multimedia Production and Concepts", 'major': 2}},
    'IT 321': {'course': {'name': "Introduction to Computing Resources Administration", 'major': 2}},
}

base = [roles, majors, degrees, courses]
names = ["Roles", "Majors", "Degrees", "Courses"]
snames = ["role_name", "major_name", "degree_name", "course_name"]

def PopulateBase(db, cur):
    """
    Takes database and cursor object

    Iterates over each dictionary and inserts that into the respective name
    """
    for k,v in roles.items():
        sql = """INSERT INTO Roles (`role_name`) Values(?)"""
        data = [k,]
        cur.execute(sql, data)
    db.commit()
    for k, v in majors.items():
        sql = """INSERT INTO Majors (`major_name`) Values(?)"""
        data = [k,]
        cur.execute(sql, data)
    db.commit()
    for k, v in degrees.items():
        sql = """INSERT INTO Degrees (`degree_name`) Values(?)"""
        data = [k,]
        cur.execute(sql, data)
    db.commit()
    for k, v in courses.items():
        sql = """INSERT INTO Courses (`course_name`, `major_id`, `course_level`) Values(?, ?, ?)"""
        data = [k,v['course']['major'], v['course']['name']]
        cur.execute(sql, data)
    db.commit()

if __name__ == "__main__":
    # Arg parser for command line arguments
    def initargp() -> argparse.ArgumentParser():
        parser = argparse.ArgumentParser()
        parser.add_argument("--recreate", action="store_true", help="Recreate database.db file, create tables, and repopulate with default data.")
        parser.add_argument("--createtables", "-c", action="store_true", help="Creates Tables.")
        parser.add_argument("--populatebase", action="store_true", help="Populates base tables with no records added.")
        return parser
    
    parser = initargp()
    args = parser.parse_args()

    if args.recreate:
        RecreateDBFile()
    db, cur = Connection()
    if args.createtables:
        CreateTables(db, cur)
    if args.populatebase:
        PopulateBase(db, cur)