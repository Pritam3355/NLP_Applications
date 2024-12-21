from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_input: str
    u_id: str
