import argparse
import sqlite3
import os


dbfile = "database.db"
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

courses = {
    'CS 101': 1,
    'CS 191': 2, 
    'CS 201R': 3,
    'CS 291': 4,
    'CS 303': 5,
    'CS 320': 6,
    'CS 349': 7,
    'CS 394R': 8,
    'CS 404': 9,
    'CS 441': 10,
    'CS 449': 11,
    'CS 456': 12,
    'CS 457': 13,
    'CS 458': 14,
    'CS 461': 15,
    'CS 465R': 16,
    'CS 470': 17,
    'CS 5520': 18,
    'CS 5525': 19,
    'CS 5552A': 20,
    'CS 5565': 21,
    'CS 5573': 22,
    'CS 5590PA': 23,
    'CS 5592': 24,
    'CS 5596A': 25,
    'CS 5596B': 26,
    'ECE 216': 27,
    'ECE 226': 28,
    'ECE 228': 29,
    'ECE 241': 30,
    'ECE 276': 31,
    'ECE 302': 32,
    'ECE 330': 33,
    'ECE 341R': 34,
    'ECE 428R': 35,
    'ECE 458': 36,
    'ECE 466': 37,
    'ECE 477': 38,
    'ECE 486': 39,
    'ECE 5558': 40,
    'ECE 5560': 41,
    'ECE 5567': 42,
    'ECE 5577': 43,
    'ECE 5578': 44,
    'ECE 5586': 45,
    'IT 222': 46,
    'IT 321': 47
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
        sql = """INSERT INTO Courses (`course_name`) Values(?)"""
        data = [k,]
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