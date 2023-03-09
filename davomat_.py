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


# daily()


def daily_new():
    conn = connections['default']
    with conn.cursor() as cursor:
        # Get the latest record from the data_students table
        cursor.execute('SELECT * FROM data_students ORDER BY created_at DESC LIMIT 1')
        row = cursor.fetchone()

        if row is not None:
            # Extract the necessary information from the record
            created_at, record_id, students_info_json, week, class_id = row
            created_at_parts = str(created_at).split('-')
            year, month, day = map(int, created_at_parts)

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

            # Insert the results into the daily table
            insert_query = "INSERT INTO daily (student_object, created_at, weekday, class_group_id) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
            cursor.execute(insert_query, (results_json, created_at, week_names[0], class_id))
            conn.commit()

            # Update the weekday field in the data_students table
            update_query = "UPDATE data_students SET weekday = %s WHERE id = %s"
            cursor.execute(update_query, (week_names[0], record_id))
            conn.commit()
        else:
            print("No records found in data_students table.")
