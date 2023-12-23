# CLI tool that lets you quickly add items to storage

import sys, json, random

OBJECTS_FILE = "objects.json"

def parse_argstring():
    """Make sense of whatever has been passed in"""
    argstring = sys.argv[1:]
    

    # smash into one single line
    entry = " ".join(argstring)
    print(f"Parsing string:\n\t`{argstring}` \nas \n\t`{entry}`")

    return entry

def save_object():
    """Save object passed in to disk"""
    object = parse_argstring()
    object = attach_entry_id(object)
    json_data = []

    try: # read from existing file
        with open(OBJECTS_FILE, 'r') as file:
            json_data = json.load(file)
            print(f"File loaded")
    except:
        print(f"File `{OBJECTS_FILE}` not loaded into memory")

    # combine existing file object and new object
    object_list = [object]
    object = json_data + object_list
    #print(f"JSON + OBJECT: {object}")

    with open(OBJECTS_FILE, 'w') as file:
        json.dump(object, file)
        print(f"File saved! \n\t {len(object)} entries present")

def list_objects():
    """Output what's saved to disk"""

def attach_entry_id(object):
    # random 6 character numeric id
    number = random.randrange(999999)
    entry_id = str(number).zfill(6)
    print(f"ENTRY ID: {entry_id}")
    entry = {"id": entry_id, "entry": object}
    #print(f"ENTRY OBJECT: {entry}")

    return entry


# where code actually runs
save_object()