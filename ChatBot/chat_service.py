import datetime
from database import DatabaseManager
from llm_service import LLMService

class ChatService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.llm_service = LLMService(api_service="Groq")  # Switch to "Together" if needed
        self.conversation_history = []
        self.chat_id = None

    def start_new_session(self, user_input):
        start_time = datetime.datetime.now()
        is_stream = 1  # Start of conversation
        self.db_manager.insert_chat_history(start_time, is_stream)
        self.chat_id = self.db_manager.get_latest_chat_id()
        bot_response = self.llm_service.generate_response(self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": bot_response})
        self.db_manager.insert_chat_data(self.chat_id, user_input, bot_response)
        return bot_response

    def continue_session(self, user_input):
        current_time = datetime.datetime.now()
        bot_response = self.llm_service.generate_response(self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": bot_response})
        self.db_manager.insert_chat_history(current_time, is_stream=0)  # Ongoing session
        self.db_manager.insert_chat_data(self.chat_id, user_input, bot_response)
        return bot_response

    def stop_session(self, user_input):
        current_time = datetime.datetime.now()
        self.db_manager.insert_chat_history(current_time, is_stream=2)  # End of conversation
        self.db_manager.insert_chat_data(self.chat_id, user_input, "Chat session ended!")
        return "Chat session ended!"

    def handle_chat(self, user_input):
        if user_input == "/stop":
            return self.stop_session(user_input)
        self.conversation_history.append({"role": "user", "content": user_input})
        if self.chat_id is None:
            return self.start_new_session(user_input)
        else:
            return self.continue_session(user_input)
