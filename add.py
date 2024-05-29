# CLI tool that lets you quickly add items to storage

import sys, json, random
import sqlite3 
from sqlite3 import Error

OBJECTS_FILE = "objects.json"
SQLITE_DATABASE = "objects.db"

def parse_argstring():
    """Make sense of whatever has been passed in"""
    argstring = sys.argv[1:]
    

    # smash into one single line
    entry = " ".join(argstring)

    return entry

def save_object():
    """Save object passed in to disk"""
    object = parse_argstring()
    object = attach_entry_id(object)
    json_data = []

    try: # read from existing file
        with open(OBJECTS_FILE, 'r') as file:
            json_data = json.load(file)
            # print(f"File loaded")
    except:
        print(f"File `{OBJECTS_FILE}` not loaded into memory")

    # combine existing file object and new object
    object_list = [object]
    object = json_data + object_list
    #print(f"JSON + OBJECT: {object}")

    with open(OBJECTS_FILE, 'w') as file:
        json.dump(object, file, indent=4)
        print(f"Item added\n\t {len(object)} entries present")

def list_objects():
    """Output what's saved to disk"""
    try: # read from existing file
        with open(OBJECTS_FILE, 'r') as file:
            json_data = json.load(file)
            print(f"File loaded")
    except:
        print(f"File `{OBJECTS_FILE}` not loaded into memory")

    print(json.dumps(json_data, indent=4, sort_keys=True))

def attach_entry_id(entry):
    """Adds a random 6-character numeric id to the entry"""
    number = random.randrange(999999)
    entry_id = str(number).zfill(6)
    
    entry = {"id": entry_id, "entry": entry}
    # print(f"ENTRY OBJECT: {entry}")

    return entry

def connect_sqlite_database(filename):
    """Create a database connection to a SQLite database"""
    connection = None
    try:
        connection = sqlite3.connect(filename)
        #print(sqlite3.sqlite_version)
    except sqlite3.Error as error:
        print(error)
    finally:
        if connection:
            print("Connected successfully!")
            #connection.close()

    return connection

# where code actually runs
save_object()

# https://docs.python.org/3/library/sqlite3.html#tutorial
connection = connect_sqlite_database(SQLITE_DATABASE)
cursor = connection.cursor()
cursor.execute("CREATE TABLE things(id, entry)")

result = cursor.execute("SELECT entry FROM sqlite_master")
result.fetchone()

data = [id, entry]
cursor.executemany("""
    INSERT INTO things VALUES
        (?, ?)
""", data)
connection.commit()

result = cursor.execute("SELECT entry FROM things")
result.fetchall()