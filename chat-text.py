import os
import mysql.connector
import datetime
from dotenv import load_dotenv
from together import Together
from groq import Groq

load_dotenv()

# Database configuration
db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME')
}

def create_tables():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChatDB.Chat_history (
        chat_id INT AUTO_INCREMENT PRIMARY KEY,
        start_time DATETIME,
        is_stream INT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChatDB.Chat_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        chat_id INT,
        user TEXT,
        assistant TEXT,
        FOREIGN KEY (chat_id) REFERENCES ChatDB.Chat_history(chat_id)
    )
    ''')

    # Drop trigger if it exists and then create a new trigger
    cursor.execute('''
    DROP TRIGGER IF EXISTS update_is_stream;
    ''')

    # Create trigger to update Chat_data.is_stream when Chat_history.is_stream is updated
    cursor.execute('''
    CREATE TRIGGER update_is_stream
    AFTER UPDATE ON ChatDB.Chat_history
    FOR EACH ROW
    BEGIN
        UPDATE ChatDB.Chat_data
        SET is_stream = NEW.is_stream
        WHERE chat_id = NEW.chat_id;
    END;
    ''')

    conn.commit()
    cursor.close()
    conn.close()
    print("Chat_history & Chat_data table and trigger created successfully")


def insert_chat_history(start_time,is_stream):
	conn = mysql.connector.connect(**db_config)
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO ChatDB.Chat_history (start_time,is_stream)
		VALUES(%s,%s)''',(start_time,is_stream))
	conn.commit()
	cursor.close()
	conn.close()

def get_chat_history():
	conn = mysql.connector.connect(**db_config)
	cursor = conn.cursor()
	cursor.execute('''
		SELECT chat_id FROM ChatDB.Chat_history WHERE 
		chat_id=(SELECT MAX(chat_id) FROM ChatDB.Chat_history)
		''')
	chat_id_pk = cursor.fetchone()[0]
	conn.commit()
	cursor.close()
	conn.close()
	if chat_id_pk:
	    return chat_id_pk
	else:
	    return None


def insert_chat_data(chat_id_pk,user,assistant):
	conn = mysql.connector.connect(**db_config)
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO ChatDB.Chat_data (chat_id,user,assistant)
		VALUES(%s,%s,%s)''',(chat_id_pk,user,assistant))
	conn.commit()
	cursor.close()
	conn.close()



create_tables()



def generate_llm_response(conversation_history):
	if api_service=="Together":
		client = Together(api_key=os.environ.get('TOGETHER_API_KEY'))
		response = client.chat.completions.create(
				        model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
				        messages=conversation_history,
				        max_tokens=512,
				        temperature=0.3,
				        top_p=0.7,
				        top_k=50,
				        repetition_penalty=1,
				        stop=["<|eot_id|>", "<|eom_id|>"],
				        stream=False  # Set to False to get the full response at once
					)
		bot_response = response.choices[0].message.content
	else:
		client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
		response = client.chat.completions.create(
				        model="llama3-8b-8192",
				        messages=conversation_history,
				        max_tokens=1024,
				        temperature=0.3,
				        top_p=0.7,
				        # top_k=25,
				        # repetition_penalty=1,
				        stop=["<|eot_id|>", "<|eom_id|>"],
				        stream=False  # Set to False to get the full response at once
					)
		bot_response = response.choices[0].message.content

	print("\nBot: ",bot_response)
	return bot_response




print("Welcome to the chatbot! Type '/stop' to end the conversation.")

# Initialize the conversation history
conversation_history = []

# Start the chat session
start_time = datetime.datetime.now()
chat_id_pk = None
conversation_history = []
api_service="Groq" # Together

while True:
	user_input = input("\nYou: ")
	# Add the user's message to the conversation history
	conversation_history.append({"role": "user", "content": user_input})
	if chat_id_pk==None: # first time starting conversation
		if user_input=="/stop":
			break
		bot_response = generate_llm_response(conversation_history)
		conversation_history.append({"role": "assistant", "content": bot_response})
		# store in DB
		is_stream = 1 # start of new conversation
		insert_chat_history(start_time,is_stream)
		chat_id_pk = get_chat_history()
		insert_chat_data(chat_id_pk,user_input,bot_response)
	else:
		current_time = datetime.datetime.now()
		if user_input=="/stop":
			is_stream = 2 # end of conversation
			insert_chat_history(current_time,is_stream)
			insert_chat_data(chat_id_pk,user_input,bot_response)
			break
		else:
			bot_response = generate_llm_response(conversation_history)
			conversation_history.append({"role": "assistant", "content": bot_response})	
			is_stream = 0 # continuation of conversation
			insert_chat_history(current_time,is_stream)
			chat_id_pk = get_chat_history()
			insert_chat_data(chat_id_pk,user_input,bot_response)
			# reset time
			# start_time = current_time
		# no need to send entire context - since it's costly
		if len(conversation_history)>1000: 
			conversation_history = conversation_history[-3:]


