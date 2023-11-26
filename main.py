from fastapi import FastAPI
from db.connectdb import connect
from report import Report


# I like to launch directly and not use the standard FastAPI startup
import uvicorn
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello SkyCastle Team, im microservice 3 on Google Cloud"}

@app.get("/reports")
async def get_all_reports(analyst: string = "", limit: int = 0):
    conn,cur=connect()
    command="SELECT * FROM reports"
    if (analyst != "" and limit > 0) {
        command="SELECT * FROM reports WHERE analyst_id=%s LIMIT %d"
        cur.execute(command, analyst, limit)
    }

    elif (analyst != "") {
        command="SELECT * FROM reports WHERE analyst_id=%s"
        cur.execute(command, analyst)
    }

    elif (limit != -1) {
        command="SELECT * FROM reports LIMIT %d"
        cur.execute(command, limit)
    }

    else {
        cur.execute(command)
    }

    result=cur.fetchall()

    return [
        {
            "report_id": row["report_id"],
            "analyst_id": row["analyst_id"],
            "content": row["content"],
            "feedback": row["feedback"],
            "user_id_list": get_user_list(row["user_id_list"]),
        }
        for row in result
    ]

# Filtering additions:
# - to add,

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}")
async def get_report_id(report_id: str):
    command="SELECT * FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {
            "report_id": result["report_id"],
            "analyst_id": result["analyst_id"],
            "content": result["content"],
            "feedback": result["feedback"],
            "user_id_list": get_user_list(result["user_id_list"]),
        }


# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/analyst")
async def get_analyst_id(report_id: str):
    command="SELECT analyst_id FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {"analyst_id": result["analyst_id"]}

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/content")
async def get_content(report_id: str):
    command="SELECT content FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {"content": result["content"]}

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/feedback")
async def get_feedback(report_id: str):
    command="SELECT feedback FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {"feedback": result["feedback"]}

# Comma seperated user_id_list, consider formatting this differently
@app.get("/reports/{report_id}/users")
async def get_user_id_list(report_id: str):
    command="SELECT user_id_list FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    print(result)
    return {"user_id_list": get_user_list(result["user_id_list"])}

def get_user_list(user_list: dict):
    if (user_list is None) or (user_list == "null") :
        return []

    return user_list.split(",")

# Todo:
# Need to figure everything that goes into a report
# What exactly do these reports consist of?
# This will determine how query is supposed to work
#
# To add:
# - update an existing report's content, verify requesting analyst_id matches
# - delete an existing report

# Create a report, db assigns report_id
@app.post("/reports")
async def create_report(rep: Report):
    sql1 = (
        "INSERT into reports(analyst_id, content, feedback) "
        "VALUES (%(analyst_id)s, %(content)s, %(feedback)s)"
    )
    sql2 = "SELECT LAST_INSERT_ID()"

    conn,cur=connect()
    try:
        # Perform the addition
        cur.execute(
            sql1,
            {
                "analyst_id": rep.analyst_id,
                "content": rep.content,
                "feedback": rep.feedback,
            },
        )

        # Get the inserted record primary key
        cur=conn.cursor()
        cur.execute(sql2)

        this_report = cur.fetchone()
        print(this_report)

    except Exception as ex:
        print(ex)
        conn.rollback()
        return ex

    return {
            "report_id": this_report["LAST_INSERT_ID()"],
            "analyst_id": rep.analyst_id,
            "content": rep.content,
            "feedback": rep.feedback,
            "user_id_list": [],
        }

# Update existing report's content with report_id
@app.put("/reports")
async def update_report(rep: Report):
    sql1 = "SELECT * FROM reports WHERE report_id=%(report_id)s"
    sql2 = "UPDATE reports SET content=%(content)s, feedback=%(feedback)s WHERE report_id=%(report_id)s"

    conn,cur=connect()
    try:
        # Check exists
        cur.execute(
            sql1,
            {
                "report_id": rep.report_id,
            },
        )
        orig_report = cur.fetchone()
        if orig_report is None:
            return "Report does not exist"

        # Perform update
        conn,cur=connect()
        cur.execute(
            sql2,
            {
                "content": rep.content,
                "feedback": rep.feedback,
                "report_id": rep.report_id,
            },
        )

        # Get updated record
        conn,cur=connect()
        cur.execute(
            sql1,
            {
                "report_id": rep.report_id,
            },
        )
        updated_report = cur.fetchone()

    except Exception as ex:
        traceback.print_exc()
        print(ex)
        print("hit exception")
        conn.rollback()
        return ex

    return {
            "report_id": updated_report["report_id"],
            "analyst_id": updated_report["analyst_id"],
            "content": updated_report["content"],
            "feedback": updated_report["feedback"],
            "user_id_list": get_user_list(updated_report["user_id_list"]),
        }

# Delete a report with the specified report_id
@app.delete("/reports/{report_id}")
async def delete_report(report_id: str):
    sql1 = "SELECT * FROM reports WHERE report_id=%(report_id)s"
    sql2 = "DELETE FROM reports WHERE report_id=%(report_id)s"

    conn,cur=connect()
    try:
        cur.execute(
            sql1,
            {
                "report_id": report_id,
            },
        )
        this_report = cur.fetchone()
        if this_report is None:
            return "Report does not exist"

        conn,curr=connect()
        cur.execute(
            sql2,
            {
                "report_id": report_id,
            },
        )

    except Exception as ex:
        print(ex)
        conn.rollback()
        return ex

    return {"Deleted": report_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
