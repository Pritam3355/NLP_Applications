
# LLM ChatBot

A simple chatbot application that interacts with the user and formats the response.
The chatbot sends messages to a FastAPI backend that processes the input and provides a response, which is displayed in a formatted manner in the frontend.

## Features

- User can type a message, which is sent to the FastAPI backend.
- The bot responds with text that includes:
  - Line breaks
  - Bullet points
  - Bold and italic text
- The conversation is displayed in a chat-style interface.
- Input is sent and received via `POST` requests to the backend.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: FastAPI (Python)
- **Database**: MySQL (for storing chat logs or user messages)

## Setup


```
#### Install dependencies

   ```bash
   pip3 install fastapi uvicorn mysql-connector-python openai=0.28 runpod
   ```

#### Run the FastAPI server

Start the FastAPI development server to run your backend:

```bash
fastapi dev main.py
```

This will run the server on `http://localhost:8000`. The `/` endpoint will accept `POST` requests with a `user_input` field, and return a bot response.

### Setting up MySQL Database

Install MySQL on your system if it’s not installed. Create a .env file and put below details but before that create a DB named "ChatDB"

```
DB_USER="USER_NAME"
DB_PASSWORD="USER_PASSWORD"
DB_HOST="localhost"
DB_NAME="ChatDB"
TOGETHER_API_KEY="YOUR_KEY"
GROQ_API_KEY="YOUR_KEY"
API_USE="RunPod"
RUNPOD_API_KEY="YOUR_RUNPOD_ID"
ENDPOINT_ID ="YOUR_ENDPOINT"
```
For crating tables use ```chatbot-db.sql```

You can set-up a RunPod Inference EndPoint & use that make sure to test it with ```runpod-test.py``` before using it to 

Here is some of the settings for RunPod (it might look a bit overkill)
```
Network Volume - 30GB
Worker Configaration - 48GB GPU (6 cores may be)
Max Workers - 2 (single one can handle almost 20+ request)
Query delay - 4 sec 
Idle time - 120 sec (since you might experiment with the script)
HF_HUB_ENABLE_HF_TRANSFER = 1 (explicitly set this in Environment Variable for faster downlaods)
```

### Folder Structure

The folder structure for your project should look like this:

```
chatbot-project/
│
├── main.py                # FastAPI server (backend)
├── database.py
├── chat_service.py
├── llm_service.py
├── models.py   
├── templates/                # Folder for static files 
│   └── index.html           
└── .env              # API keys,DB connection secrets
```




## How It Works

1. The user types a message into the input box and presses the "Send" button.
2. The message is sent to the FastAPI backend via a `POST` request to the `/chat/` endpoint.
3. The backend processes the input, generates a bot response, and stores the conversation in the MySQL database.
4. The bot's response is returned and displayed on the frontend.
5. The conversation is displayed on the screen with formatted messages.






