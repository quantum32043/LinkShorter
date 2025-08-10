import uvicorn
from fastapi import FastAPI

from routes import routes

app = FastAPI()
app.include_router(routes)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)