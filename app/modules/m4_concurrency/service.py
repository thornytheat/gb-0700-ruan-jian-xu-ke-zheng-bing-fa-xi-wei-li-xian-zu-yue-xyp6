def execute(text):
    from app.pipeline import run
    result=run(text)
    return {"module":4, "report":result["reports"][3], "quarantine":result["quarantine"], "balance":result["balance"]}
