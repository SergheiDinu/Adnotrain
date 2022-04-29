import uvicorn
from fastapi import FastAPI

app = FastAPI()

import nlp

app.include_router(nlp.router)


if __name__ == '__main__':
    uvicorn.run(app)
