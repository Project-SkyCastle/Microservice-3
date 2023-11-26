import pymysql
from datetime import datetime

# Note: data as it's formatted in the table
# NOTE: report_id's will be increasing but not be
# these exact numbers due to the table persisting
dummy_data = [
    {
        # "report_id": 1,
        "analyst_id": "1",
        "content": "first report content",
        "feedback": " first report feedback",
        "user_id_list": "2,3",
    },
    {
        # "report_id": 2,
        "analyst_id": "1",
        "content": "It was the best of times, it was the worst of times",
        "feedback": "acceptable feedback",
        "user_id_list": "1",
    },
    {
        # "report_id": 3,
        "analyst_id": "2",
        "content": "hello i am the third report",
        "feedback": "this is good feedback",
        "user_id_list": "",
    },
    {
        # "report_id": 4,
        "analyst_id": "8",
        "content": "content talking about stuff",
        "feedback": "not so good feedback",
        "user_id_list": "1,2",
    },
]

with pymysql.connect(
    host="34.71.37.85",
    user="root",
    password="microservice-3",
    database="reportsdb",
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
) as conn:
    with conn.cursor() as cur:
        insert = (
            "INSERT into reports (analyst_id, content, feedback, user_id_list) "
            "VALUES (%(analyst_id)s, %(content)s, %(feedback)s, %(user_id_list)s)"
        )
        for row in dummy_data:
            cur.execute(insert, row)
            print(row)