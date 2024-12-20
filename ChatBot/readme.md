
# Chatbot Project

A simple chatbot application that interacts with the user and formats the response using HTML, CSS, JavaScript, and FastAPI for the backend. The chatbot sends messages to a FastAPI backend that processes the input and provides a response, which is displayed in a formatted manner in the frontend.

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

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/chatbot-project.git
cd chatbot-project
```

### 2. Frontend

- Open the `index.html` file in a browser to interact with the chatbot.

### 3. Backend: Setting Up FastAPI


#### Install dependencies

1. Install the required dependencies:

   ```bash
   pip install fastapi uvicorn mysql-connector-python
   ```

#### Run the FastAPI server

Start the FastAPI development server to run your backend:

```bash
uvicorn main:app --reload
```

This will run the server on `http://localhost:8000`. The `/` endpoint will accept `POST` requests with a `user_input` field, and return a bot response.

### 4. Setting up MySQL Database

1. Install MySQL on your system if it’s not installed. Create a .env file and put below details but before that create a DB named "ChatDB"

```
DB_USER="USER_NAME"
DB_PASSWORD="USER_PASSWORD"
DB_HOST="localhost"
DB_NAME="ChatDB"
TOGETHER_API_KEY="YOUR_KEY"
GROQ_API_KEY="YOUR_KEY"
```

### 5. Folder Structure

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

### 6. Optional: Requirements File


```txt
fastapi
uvicorn
mysql-connector
```



## How It Works

1. The user types a message into the input box and presses the "Send" button.
2. The message is sent to the FastAPI backend via a `POST` request to the `/chat/` endpoint.
3. The backend processes the input, generates a bot response, and stores the conversation in the MySQL database.
4. The bot's response is returned and displayed on the frontend.
5. The conversation is displayed on the screen with formatted messages.

## Customization

- Modify the `generate_bot_response` function in `main.py` to integrate with a real chatbot model or API.
- The MySQL database schema can be extended to store additional information, such as user details or chat metadata.






