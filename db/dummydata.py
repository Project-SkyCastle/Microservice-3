import pymysql
from datetime import datetime

# Note: data as it's formatted in the table
# NOTE: report_id's will be increasing but not be
# these exact numbers due to the table persisting
dummy_data = [
    {
        # "report_id": 1,
        "title": "the first title",
        "analyst_id": "1",
        "content": "first report content",
        "feedback": " first report feedback",
        "subscribers": "2;3",
    },
    {
        # "report_id": 2,
        "title": "yet another title",
        "analyst_id": "1",
        "content": "It was the best of times, it was the worst of times",
        "feedback": "acceptable feedback",
        "subscribers": "1",
    },
    {
        # "report_id": 3,
        "title": "the third title",
        "analyst_id": "2",
        "content": "hello i am the third report",
        "feedback": "this is good feedback",
        "subscribers": "",
    },
    {
        # "report_id": 4,
        "title": "wow another title",
        "analyst_id": "8",
        "content": "content talking about stuff",
        "feedback": "not so good feedback",
        "subscribers": "1;2",
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
            "INSERT into reports (title, analyst_id, content, feedback, user_id_list) "
            "VALUES (%(title)s, %(analyst_id)s, %(content)s, %(feedback)s, %(user_id_list)s)"
        )
        for row in dummy_data:
            cur.execute(insert, row)
            print(row)