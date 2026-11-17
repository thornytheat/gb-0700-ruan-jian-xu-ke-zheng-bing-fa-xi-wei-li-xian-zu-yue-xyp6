def execute(text):
    from app.pipeline import run
    result=run(text)
    return {"module":7, "report":result["reports"][6], "quarantine":result["quarantine"], "balance":result["balance"]}
