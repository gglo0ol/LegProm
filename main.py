from DataBase import DatabaseHandler
from rqst import Request as R


from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
GLOBAL_KEY = None

# Подключаем БД
db = DatabaseHandler(host='mysql', port=3306, user='root')

# Подключение шаблонов
templates = Jinja2Templates(directory="templates")

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Стартовая страница с вводом ключа
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Сзодание таблицы c_risks
    db.create_table('c_risks')
    return templates.TemplateResponse("start.html", {"request": request})

# Главная страница с формой ввода
@app.get("/index", response_class=HTMLResponse)
async def read_root(request: Request, key: str = None):
    
    global GLOBAL_KEY
    if not GLOBAL_KEY:
        GLOBAL_KEY = key
        r = R(GLOBAL_KEY)
        start(r)
    return templates.TemplateResponse("index.html", {"request": request})

# Страница для обработки введенных данных
@app.post("/process_data", response_class=HTMLResponse)
async def process_data(request: Request, inn: str = Form(...)):
    
    if not db.get_by_inn(inn):
        return templates.TemplateResponse("error.html", {"request": request, "error": "Данной компании нет в БД"})
    row = db.get_by_inn(inn)
    return templates.TemplateResponse("result.html", {"request": request, "row": row})

@app.get("/get_all_data", response_class=HTMLResponse)
async def show_all(request: Request):
    
    if not db.get_all():
        return templates.TemplateResponse("error.html", {"request": request, "error": "Данной компании нет в БД"})
    row = db.get_all()
    return templates.TemplateResponse("result.html", {"request": request, "row": row})

@app.get("/delete", response_class=HTMLResponse)
async def show_all(request: Request, inn: str):
    
    sql_q = f'DELETE FROM legpromtest.c_risks ' \
            f'WHERE inn={inn};'
    db.execute_insert(sql_q)
    if not db.get_all():
        return templates.TemplateResponse("error.html", {"request": request, "error": "Данной компании нет в БД"})
    row = db.get_all()
    return templates.TemplateResponse("result.html", {"request": request, "row": row})

def start(request):

    select_inn = db.execute_query(sql='SELECT DISTINCT inn ' \
                                  'from legpromtest.c_company;')
    for row in select_inn:
        inn = str(*row)
        data = request.get_positive_and_negative(inn)
        positive, negativ = data.positive, data.negative
        sql = f'INSERT INTO legpromtest.c_risks(inn , positive, negative) VALUES(%s, %s, %s);'
        db.execute_insert(sql, (inn, positive, negativ))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
