import sqlite3
import json
import datetime
from django.db import connections


# connections.close_all()


def daily():
    conn = connections['default']
    with connections['default'].cursor() as cursor:
        cursor = conn.cursor()
        # conn = sqlite3.connect('db.sqlite3')
        # cursor = conn.cursor()
        cursor.execute('SELECT * FROM data_students ORDER BY created_at DESC LIMIT 1')
        row = cursor.fetchone()

    if row is not None:
        # Extract the necessary information from the record
        created_at, record_id, students_info_json, week, class_id = row
        print(created_at, 'bu yaratildi')
        created_at_parts = str(created_at).split('-')
        print(created_at_parts, 'shu')
        year, month, day = int(created_at_parts[0]), int(created_at_parts[1]), int(created_at_parts[2])
        print(year, month, day)
        # Convert the students information from JSON to Python objects
        students_info = json.loads(students_info_json)

        results = []
        week_names = []
        for student_info in students_info:
            name = student_info['name']
            absent = student_info['absent']
            cleanly = student_info['cleanly']
            uniform = student_info['uniform']

            absent_ball = 5 if absent else 0
            jami_ball = absent_ball + cleanly + uniform
            weekday_name = datetime.date(year, month, day).strftime("%A")
            week_names.append(weekday_name)
            # Create a dictionary representing the result for this student
            result = {'name': name, 'overall': jami_ball}
            results.append(result)

        # Convert the results to JSON
        results_json = json.dumps(results)
        print(results_json)

        # Insert the results into the daily table
        cursor.execute(
            "INSERT INTO daily (student_object, created_at, weekday, class_group_id) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            (results_json, created_at, week_names[0], class_id))
        conn.commit()
        cursor.execute("UPDATE data_students SET weekday = %s WHERE id = %s", (week_names[0], record_id))
        conn.commit()
        # cursor.execute("SELECT * FROM data_students")
        # row2 = cursor.fetchone()
        # print(row2)
    else:
        print("No records found in data_students table.")


daily()

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

# def daily1():
#     todays_date = date.today()
#     # Connect to the database
#     with sqlite3.connect('db.sqlite3') as conn:
#         # Create a cursor
#         cursor = conn.cursor()
#
#         # Get the latest row from the data_students table
#         cursor.execute("SELECT MAX(id),students_information, created_at,class_group_id, weekday FROM data_students")
#         row = cursor.fetchone()
#         row_id = row[0]
#         row_json = row[1]
#         created_at = row[2].split('-')
#         # class_id = row[3]
#         # week = row[4]
#
#         # Convert the JSON data to Python objects
#         students = json.loads(row_json)
#         # print(row)
#         # Process each student
#         results1 = {}
#         for student in students:
#             absent = student['absent']
#             cleanly = student['cleanly']
#             uniform = student['uniform']
#             name = student['name']
#             absent_ball = 5 if absent else 0
#             jami_ball = absent_ball + cleanly + uniform
#
#             # Convert the date string to a datetime object and get the weekday name
#             year, month, day = map(int, created_at)
#
#             # date_obj = datetime.datetime(year, month, day)
#             date_obj = todays_date
#             # print(date_obj)
#             weekday_name = date_obj.strftime("%A")
#             # print(weekday_name)
#             # Create a dictionary for the student's result and convert it to JSON
#             result = {'name': name, 'overall': jami_ball}
#             results1.update(result)
#             json_result = json.dumps(results1)
#         print(json_result)
#         # Insert the student's data into the daily table
#         # cursor.execute(
#         #     "INSERT INTO daily (student_object, created_at, weekday, class_group_id) VALUES (?, ?, ?, ?)",
#         #     (json_result, date_obj, weekday_name, class_id))
#
#         # Update the weekday column in the data_students table
#         cursor.execute('UPDATE data_students SET weekday=? WHERE id=?', (weekday_name, row_id))
#
#         # Commit the changes to the database
#         conn.commit()
#
#         # Print the latest row from the data_students table
#         cursor.execute("SELECT MAX(id),students_information, created_at,class_group_id, weekday FROM data_students")
#         row = cursor.fetchone()
#         conn.close()
# print(row)

# daily1()
