from fastapi import FastAPI
import uvicorn # -> devemos reconhecer como um servidor assíncrono
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    await asyncio.sleep(20)
    return {"Hello":"World"}

if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000,workers=1)

#agora se eu fizer duas chamadas as duas durarão 20 segundos.