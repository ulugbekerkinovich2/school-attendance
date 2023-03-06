import datetime
import json
import sqlite3
from datetime import date
import sqlite3
import json
import datetime
connect = sqlite3.connect('db.sqlite3')
cursor = connect.cursor()


# def by_day():
#     now = datetime.datetime.now()
#     year_ = now.year
#     month_ = now.month
#     day_ = now.day
#     created_ats = f'{year_}-{month_}-{day_}'
#     cursor.execute("SELECT * FROM mytable")
#     row = cursor.fetchall()
#     for i in row:
#         print(i)
#         absent = i[1]
#         cleanly = i[2]
#         uniform = i[3]
#         table_id = i[6]
#         name_id = i[5]
#         if absent == 1:
#             ball_absent = 5
#         elif absent == 0:
#             ball_absent = 0
#         jami_bali = ball_absent + cleanly + uniform
#         print(
#             f'table_id-->{table_id}\n kelganligi-->{absent}\n {cleanly}, {uniform}, \nism_id-->{name_id}\n -->jami: {jami_bali}')
#         cursor.execute("""
#             INSERT INTO by_day (student_name_id, overall, table_id_id, created_at)
#             SELECT ?, ?, ?,?
#
#             WHERE NOT EXISTS (
#                 SELECT 1 FROM by_day WHERE student_name_id = ? AND table_id_id = ?
#             )
#         """, (name_id, jami_bali, table_id, created_ats, name_id, table_id))
#         connect.commit()


def daily():

    # Get today's date
    today = date.today()

    # Connect to the database
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()

    # Get the latest record from the data_students table
    cursor.execute("SELECT MAX(id), students_information, created_at, class_group_id, weekday FROM data_students")
    row = cursor.fetchone()

    # Extract the necessary information from the record
    record_id, students_info_json, created_at, class_id, week = row
    created_at_parts = created_at.split('-')
    year, month, day = int(created_at_parts[0]), int(created_at_parts[1]), int(created_at_parts[2])

    # Convert the students information from JSON to Python objects
    students_info = json.loads(students_info_json)

    results = []
    for student_info in students_info:
        name = student_info['name']
        absent = student_info['absent']
        cleanly = student_info['cleanly']
        uniform = student_info['uniform']

        absent_ball = 5 if absent else 0
        jami_ball = absent_ball + cleanly + uniform
        weekday_name = datetime.date(year, month, day).strftime("%A")

        # Create a dictionary representing the result for this student
        result = {'name': name, 'overall': jami_ball}
        results.append(result)

    # Convert the results to JSON
    results_json = json.dumps(results)
    print(results_json)
    # Insert the results into the daily table
    cursor.execute("INSERT INTO daily (student_object, created_at, weekday, class_group_id) VALUES (?, ?, ?, ?)",
                   (results_json, created_at, weekday_name, class_id))
    connection.commit()

    # Update the weekday field in the data_students table
    cursor.execute("UPDATE data_students SET weekday = ? WHERE id = ?", (weekday_name, record_id))
    connection.commit()

    # Close the database connection
    # connection.close()


# daily()

# obj = json.loads(row_json)
# def weekly():
#     today = date.today()
#     year = today.year
#     month = today.month
#     day = today.day
#     connect = sqlite3.connect('db.sqlite3')
#     cursor = connect.cursor()
#     cursor.execute("SELECT id,created_at, students_information, class_group_id,weekday FROM data_students ")
#     row = cursor.fetchall()
#     for i in row:
#         row_id = i[0]
#         created = i[1]
#         row_json = i[2]
#         class_group = i[3]
#         weekday = i[4]
#         obj = json.loads(row_json)
#         # print(obj, weekday, created, row_id)
#     y = str(created).split('-')
#     if y[1].startswith('0') or y[2].startswith('0'):
#         y[1] = y[1].replace('0', '')
#         y[2] = y[2].replace('0', '')
#     time = f"{year}-{month}-{day}"
#     now = datetime.now()
#     if int(y[0]) == year and int(y[1]) == month:
#         cursor.execute(
#             "SELECT id, weekday, created_at,students_information  FROM data_students WHERE created_at =?",
#             (now.strftime("%Y-%m-%d"),))
#         row = cursor.fetchone()
#         print(row)
#
#     print(year, month, day)
#
#
# weekly()

def daily1():

    todays_date = date.today()
    # Connect to the database
    with sqlite3.connect('db.sqlite3') as conn:
        # Create a cursor
        cursor = conn.cursor()

        # Get the latest row from the data_students table
        cursor.execute("SELECT MAX(id),students_information, created_at,class_group_id, weekday FROM data_students")
        row = cursor.fetchone()
        row_id = row[0]
        row_json = row[1]
        created_at = row[2].split('-')
        class_id = row[3]
        week = row[4]

        # Convert the JSON data to Python objects
        students = json.loads(row_json)
        # print(row)
        # Process each student
        results1 = {}
        for student in students:
            absent = student['absent']
            cleanly = student['cleanly']
            uniform = student['uniform']
            name = student['name']
            absent_ball = 5 if absent else 0
            jami_ball = absent_ball + cleanly + uniform

            # Convert the date string to a datetime object and get the weekday name
            year, month, day = map(int, created_at)

            # date_obj = datetime.datetime(year, month, day)
            date_obj = todays_date
            # print(date_obj)
            weekday_name = date_obj.strftime("%A")
            # print(weekday_name)
            # Create a dictionary for the student's result and convert it to JSON
            result = {'name': name, 'overall': jami_ball}
            results1.update(result)
            json_result = json.dumps(results1)
        print(json_result)
        # Insert the student's data into the daily table
        # cursor.execute(
        #     "INSERT INTO daily (student_object, created_at, weekday, class_group_id) VALUES (?, ?, ?, ?)",
        #     (json_result, date_obj, weekday_name, class_id))

        # Update the weekday column in the data_students table
        cursor.execute('UPDATE data_students SET weekday=? WHERE id=?', (weekday_name, row_id))

        # Commit the changes to the database
        conn.commit()

        # Print the latest row from the data_students table
        cursor.execute("SELECT MAX(id),students_information, created_at,class_group_id, weekday FROM data_students")
        row = cursor.fetchone()
        conn.close()
        # print(row)


# daily1()
