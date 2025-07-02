from fastapi import FastAPI
from routes import tools, ga4

app = FastAPI(title="MCP GA4 Tool Server")

@app.get("/")
async def root():
    return {"status": "Eliott MCP is live"}

app.include_router(tools.router, prefix="/mcp")
app.include_router(ga4.router, prefix="/ga4")
