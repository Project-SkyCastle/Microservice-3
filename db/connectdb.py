# import uuid
import pymysql

def connect():
    conn=pymysql.connect(
        host="34.71.37.85",
        port="3306",
        user="root",
        password="microservice-3",
        autocommit=True
    )
    cur=conn.cursor()
    return conn,cur

#vconn,cur=connect()

#create a table
# command="CREATE TABLE IF NOT EXISTS reports (report_id VARCHAR(255) PRIMARY KEY,
#                                     analyst_id VARCHAR(255), content VARCHAR(4000),
#                                     feedback VARCHAR(255))""
# cur.execute(command)
# conn.commit()

#insert data
# report_id="1"
# analyst_id="1"
# content="empty"
# feedbacks="empty"


# command="""INSERT INTO reports (report_id, analyst_id, content, feedback) VALUES (%s, %s, %s, %s)"""
# cur.execute(command,(report_id, analyst_id, content, feedback))
# conn.commit()

#fetch database
# command="""SELECT * FROM reports"""
# cur.execute(command)
# result=cur.fetchall()
# print(result)

#delete data
# command="""DELETE FROM reports WHERE report_id=%s"""
# cur.execute(command,("1"))
# conn.commit()

#delete table
# command="""DROP TABLE reports"""
# cur.execute(command)
# conn.commit()