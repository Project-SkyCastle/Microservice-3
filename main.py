from fastapi import FastAPI
from db.connectdb import connect
from report import Report

# I like to launch directly and not use the standard FastAPI startup
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello SkyCastle Team, im microservice 3 on Google Cloud"}

@app.get("/reports")
async def get_all_reports():
    command="SELECT * FROM reports"
    conn,cur=connect()
    cur.execute(command)
    result=cur.fetchall()
    print(result)
    return [
        row for row in result
    ]

    """
            "report_id": row[report_id],
            "analyst_id": row[analyst_id],
            "content": row[content],
            "feedback": row[feedback],
            "user_id_list": row[user_id_list], """

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}")
async def get_report_id(report_id: str):
    command="SELECT * FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()

    return {
            "report_id": row[report_id],
            "analyst_id": row[analyst_id],
            "content": row[content],
            "feedback": row[feedback],
            "user_id_list": row[user_id_list],
        }


# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/analyst")
async def get_analyst_id(report_id: str):
    command="SELECT analyst_id FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {"analyst_id": row[analyst_id]}

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/content")
async def get_content(report_id: str):
    command="SELECT content FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {"content": row[content]}

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/feedback")
async def get_feedback(report_id: str):
    command="SELECT feedback FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchone()
    return {"feedback": row[feedback]}

# Comma seperated user_id_list, consider formatting this differently
@app.get("/reports/{report_id}/user_id_list")
async def get_user_id_list(report_id: str):
    command="SELECT user_id_list FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchall()
    return {"user_id_list": row[user_id_list]}

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
    sql = (
        "INSERT into reports(analyst_id, content, feedback) "
        "VALUES (%(analyst_id)s, %(content)s, %(feedback)s)"
    )

    conn,cur=connect()
    try:
        cur.execute(
            sql,
            {
                "analyst_id": rep[analyst_id],
                "content": rep[content],
                "feedback": rep[feedback],
            },
        )
        this_report = cur.fetchone()

    except Exception as ex:
        print(ex)
        conn.rollback()
        return ex

    return {
            "report_id": this_report[report_id],
            "analyst_id": this_report[analyst_id],
            "content": this_report[content],
            "feedback": this_report[feedback],
            "user_id_list": this_report[user_id_list],
        }

# Update existing report's content with report_id
@app.put("/reports")
async def update_report(rep: Report):
    sql1 = "SELECT * FROM reports WHERE report_id=%(report_id)s"
    sql2 = "UPDATE reports SET content=%(content)s, feedback=%(feedback)s WHERE report_id=%(report_id)s"

    conn,cur=connect()
    try:
        # Todo: add logic to only update content and feedback if new values present
        # otherwise keep the values the same as the original
        cur.execute(
            sql1,
            {
                "report_id": rep[report_id],
            },
        )
        orig_report = cur.fetchone()
        if orig_report is None:
            return "Report does not exist"

        cur.execute(
            sql2,
            {
                "content": rep[content],
                "feedback": rep[feedback],
            },
        )
        updated_report = cur.fetchone()

    except Exception as ex:
        print(ex)
        conn.rollback()
        return ex

    return {
            "report_id": updated_report[report_id],
            "analyst_id": updated_report[analyst_id],
            "content": updated_report[content],
            "feedback": updated_report[feedback],
            "user_id_list": updated_report[user_id_list],
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
