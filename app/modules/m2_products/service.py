def execute(text):
    from app.pipeline import run
    result=run(text)
    return {"module":2, "report":result["reports"][1], "quarantine":result["quarantine"], "balance":result["balance"]}
