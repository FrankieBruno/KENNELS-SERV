from multiprocessing.connection import _ConnectionBase
import sqlite3
import json
from models import Employee
from models.location import Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    },
    {
        "id": 2,
        "name": "Frankie Bruno"
    },
    {
        "id": 3,
        "name": "Wesley Hughes"
    },
    {
        "id": 4,
        "name": "Vision Filler"
    }
]


# def get_all_employees():
#     """this gets employees"""
#     return EMPLOYEES

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
        e.id,
        e.name,
        e.address,
        e.location_id,
        l.name location_name,
        l.address location_address
    FROM Employee e
    JOIN Location l
            ON l.id = e.location_id
        """)

        # Initialize an empty list to hold all customer representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an animal instance from the current row
            employee = Employee(row['id'], row['name'],
                                row['address'], row['location_id'])

        # Create a Location instance from the current row
            location = Location(
                row['location_id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__
            employees.append(employee.__dict__)
    return employees

# def get_single_employee(id):
#     """id to find a single employee object"""
#     # Variable to hold the found animal, if it exists:
#     requested_employee = None

#     # Iterate the ANIMALS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for employee in EMPLOYEES:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if employee["id"] == id:
#             requested_employee = employee

#     return requested_employee


def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        employee = Employee(data['id'], data['name'], data['address'],
                            data['location_id'])

        return employee.__dict__


def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            e.id,
            e.name,
            e.address,
            e.location_id
        from Employee e
        WHERE e.location_id = ?
        """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return employees


# def create_employee(employee):
#     """create animal"""
#     # Get the id value of the last animal in the list
#     max_id = EMPLOYEES[-1]["id"]

#     # Add 1 to whatever that number is
#     new_id = max_id + 1

#     # Add an `id` property to the animal dictionary
#     employee["id"] = new_id

#     # Add the animal dictionary to the list
#     EMPLOYEES.append(employee)

#     # Return the dictionary with `id` property added
#     return employee



def create_employee(new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id)
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_employee['name'], new_employee['address'],
            new_employee['location_id']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_employee['id'] = id


    return new_employee

# def delete_employee(id):
#     """delete a employee"""
#     # Initial -1 value for animal index, in case one isn't found
#     employee_index = -1

#     # Iterate the ANIMALS list, but use enumerate() so that you
#     # can access the index value of each item
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the animal. Store the current index.
#             employee_index = index

#     # If the animal was found, use pop(int) to remove it from list
#     if employee_index >= 0:
#         EMPLOYEES.pop(employee_index)

def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))

# def update_employee(id, new_employee):
#     """Iterate the employee list"""
#     # but use enumerate() so that
#     # you can access the index value of each item.
#     for index, employee in enumerate(EMPLOYEES):
#         if employee["id"] == id:
#             # Found the animal. Update the value.
#             EMPLOYEES[index] = new_employee
#             break


def update_employee(id, new_employee):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Employee
            SET
                name = ?,
                address = ?,
                email = ?,
                password = ?
        WHERE id = ?
        """, (new_employee['name'], new_employee['address'],
              new_employee['email'], new_employee['password'],
              id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
