def execute(text):
    from app.pipeline import run
    result=run(text)
    return {"module":1, "report":result["reports"][0], "quarantine":result["quarantine"], "balance":result["balance"]}
