call conda activate dbtts
uvicorn main:app --reload --port 8001 --host ::
pause