# import datetime
from database import DatabaseManager
from llm_service import LLMService
from datetime import datetime as dt

class ChatService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.llm_service = LLMService(api_service="Groq")  # Alternate "Together"
        self.conversation_history = []
        self.session_id = None
        self.u_id = None

    def start_new_session(self, user_input):
        bot_response = self.llm_service.generate_response(self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": bot_response})
        time_stamp = dt.now()
        stream_id = 1  # Start of conversation
        # session_id : u_id$$time_stamp
        self.session_id = str(self.u_id)+"$$"+time_stamp.strftime("%Y-%m-%d@%H:%M:%S") 
        self.db_manager.set_active_user(self.u_id)
        self.db_manager.insert_session_data(self.u_id,self.session_id,time_stamp, stream_id)
        self.db_manager.insert_chat_data(self.u_id,self.session_id,user_input,bot_response)
        return bot_response

    def continue_session(self, user_input):
        bot_response = self.llm_service.generate_response(self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": bot_response})
        time_stamp = dt.now()
        # u_id = self.db_manager.get_active_user()
        # session_id = self.db_manager.get_latest_session_id()
        stream_id = 0 # Ongoing session
        self.db_manager.insert_session_data(self.u_id,self.session_id,time_stamp, stream_id)  
        self.db_manager.insert_chat_data(self.u_id,self.session_id,user_input,bot_response)
        return bot_response

    def stop_session(self, user_input):
        bot_response = "Chat session ended!"
        self.conversation_history.append({"role": "assistant", "content": bot_response})
        time_stamp = dt.now()
        # u_id = self.db_manager.get_active_user()
        # session_id = self.db_manager.get_latest_session_id()
        stream_id = 2   # End of conversation
        self.db_manager.insert_session_data(self.u_id,self.session_id,time_stamp, stream_id) 
        self.db_manager.insert_chat_data(self.u_id,self.session_id,user_input,bot_response)
        self.db_manager.reset_active_user(self.u_id)
        return "Chat session ended!"

    def handle_chat(self, user_input,u_id):
        self.u_id = u_id
        self.conversation_history.append({"role": "user", "content": user_input})
        if user_input == "/stop":
            return self.stop_session(user_input)
        
        # Keep context length under 1024
        if len(self.conversation_history) >= 1024:
            self.conversation_history = self.conversation_history[-3:]
        if self.session_id is None:
            return self.start_new_session(user_input)
        else:
            return self.continue_session(user_input)
