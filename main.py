from fastapi import FastAPI
from db.connectdb import connect

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
    return [{row} for row in result]

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}")
async def get_report_id(report_id: str):
    command="SELECT * FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchall()
    return [{row} for row in result]


# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/analyst")
async def get_analyst_id(report_id: str):
    command="SELECT analyst_id FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchall()
    return [{row} for row in result]

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/content")
async def get_content(report_id: str):
    command="SELECT content FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchall()
    return [{row} for row in result]

# Note: should add check that this is only 0 or 1 size
@app.get("/reports/{report_id}/feedback")
async def get_feedback(report_id: str):
    command="SELECT feedback FROM reports WHERE report_id=%s"
    conn,cur=connect()
    cur.execute(command,(report_id))
    result=cur.fetchall()
    return [{row} for row in result]

# Todo:
# Need to figure everything that goes into a report
# What exactly do these reports consist of?
# This will determine how query is supposed to work
#
# To add:
# - update an existing report's content, verify requesting analyst_id matches
# - delete an existing report

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
