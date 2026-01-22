import fastapi

app = fastapi.FastAPI()


@app.get('/')
async def index():
    return {'hello': 'world'}


@app.get("/healthcheck")
async def health_check():
    return {"status": "healthy"}
