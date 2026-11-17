def execute(text):
    from app.pipeline import run
    result=run(text)
    return {"module":5, "report":result["reports"][4], "quarantine":result["quarantine"], "balance":result["balance"]}
