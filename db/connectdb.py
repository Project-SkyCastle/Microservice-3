import psycopg2
import uuid

def connect():
    conn=psycopg2.connect(
        host="microservice.cyzurhix8mmm.us-east-1.rds.amazonaws.com",
        port="5432",
        user="postgres",
        password="microservice2"
    )
    cur=conn.cursor()
    return conn,cur

conn,cur=connect()

#create a table
# command="""CREATE TABLE IF NOT EXISTS subscriptions (subscription_id VARCHAR(255) PRIMARY KEY, subscriber_id VARCHAR(255), analyst_id VARCHAR(255), report_id VARCHAR(255), feedbacks VarChar(255), notifications VarChar(255), activity VarChar(255))"""
# cur.execute(command)
# conn.commit()

#insert data
# subscription_id="1"
# subscriber_id="1"
# analyst_id="1"
# report_id="1"
# feedbacks="feedbacks: None"
# notifications="notifications: None"
# activity="activity: None"

# command="""INSERT INTO subscriptions (subscription_id, subscriber_id, analyst_id, report_id, feedbacks, notifications, activity) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
# cur.execute(command,(subscription_id, subscriber_id, analyst_id, report_id, feedbacks, notifications, activity))
# conn.commit()

#fetch database
# command="""SELECT * FROM subscriptions"""
# cur.execute(command)
# result=cur.fetchall()
# print(result)

#delete data
# command="""DELETE FROM subscriptions WHERE subscription_id=%s"""
# cur.execute(command,("1"))
# conn.commit()

#delete table
# command="""DROP TABLE subscriptions"""
# cur.execute(command)
# conn.commit()