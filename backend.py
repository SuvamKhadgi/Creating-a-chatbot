import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("student.db")

# Drop the existing student table if it exists
# conn.execute('DROP TABLE IF EXISTS student')

# Create a new student table without the photo column
conn.execute('''
    CREATE TABLE IF NOT EXISTS student(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizenship_no varchar(15),
        full_name varchar(30),
        sex varchar(7),
        dob varchar(15),
        birth_place varchar(30),
        address varchar(30),
        school varchar(50),
        faculty varchar(10),
        gpa int,
        passout_year varchar(15),
        course varchar(15),
        front BLOB,
        back BLOB,
        marksheet BLOB
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Function to convert digital data to binary format
def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

# Function to insert student data into the database and return the new row ID
def insert_student_data(citizenship_no, full_name, sex, dob, birth_place, address, school, faculty, gpa, passout_year, course, front_image_path, back_image_path, marksheet_image_path):
    try:
        conn = sqlite3.connect('student.db')
        cursor = conn.cursor()

        print("Inside insertion")

        # Convert images to binary data
        front_image = convert_to_binary_data(front_image_path)
        back_image = convert_to_binary_data(back_image_path)
        marksheet_image = convert_to_binary_data(marksheet_image_path)

        # Insert data into the table
        cursor.execute('''
            INSERT INTO student (citizenship_no, full_name, sex, dob, birth_place, address, school, faculty, gpa, passout_year, course, front, back, marksheet)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (citizenship_no, full_name, sex, dob, birth_place, address, school, faculty, gpa, passout_year, course, front_image, back_image, marksheet_image))

        conn.commit()
        print("Student data inserted successfully")

        # Get the ID of the newly inserted row
        new_id = cursor.lastrowid
        return new_id
    except sqlite3.Error as error:
        print("Failed to insert data into SQLite table", error)
        return None
    finally:
        if conn:
            conn.close()

# Example usage
# new_id = insert_student_data(
#     citizenship_no="123456789",
#     full_name="John Doe",
#     sex="Male",
#     dob="2000-01-01",
#     birth_place="Hometown",
#     address="123 Main St",
#     school="XYZ High School",
#     faculty="Science",
#     gpa=4,
#     passout_year="2018",
#     course="Physics",
#     front_image_path="path/to/front_image.jpg",
#     back_image_path="path/to/back_image.jpg",
#     marksheet_image_path="path/to/marksheet_image.jpg"
# )
# print("Newly inserted row ID:", new_id)