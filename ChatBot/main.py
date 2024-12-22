
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from models import ChatRequest
from chat_service import ChatService

# FastAPI app initialization
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates for HTML responses
templates = Jinja2Templates(directory="templates")

chat_service = ChatService()

# Endpoint for serving frontend
@app.get("/", response_class=HTMLResponse)
async def get_chat_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat endpoint
@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    user_input = chat_request.user_input
    u_id = chat_request.u_id
    bot_response = chat_service.handle_chat(user_input,u_id)
    return JSONResponse(content={"response": bot_response})
