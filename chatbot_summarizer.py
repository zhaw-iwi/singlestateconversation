from chatbot_db_helper import ChatbotDBHelper

class ChatbotSummarizer(ChatbotDBHelper):
    
    _chatbot_summary_table = "chatbot_summaries"
    _chatbot_summary_session_table = "chatbot_summaries_sessions"

    def __init__(self, database, type_id, user_id, type_name=None, type_role=None, instance_context=None, instance_starter=None):
        ChatbotDBHelper.__init__(self, database, type_id, user_id, type_name, type_role, instance_context, instance_starter)

        ChatbotDBHelper._connection
        if not self._ddl_exists_summarizer():
            self._ddl_save_summarizer()

    def _ddl_save_summarizer(self):
        cursor = self._connection
        cursor.execute("CREATE TABLE " + ChatbotSummarizer._chatbot_summary_table + " (id INTEGER PRIMARY KEY, summary TEXT NOT NULL, is_deleted BOOLEAN DEFAULT (0))")
        cursor.execute("CREATE TABLE " + ChatbotSummarizer._chatbot_summary_session_table + " (session INTEGER NOT NULL, summary INTEGER NOT NULL, t TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (session) REFERENCES " + ChatbotDBHelper._chatbot_session_table + "(id)), FOREIGN KEY (summary) REFERENCES " + ChatbotSummarizer._chatbot_summary_table + "(id)")
        self._connection.commit()

    def _ddl_exists_summarizer(self):
        cursor = self._connection
        result_summary = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"" + ChatbotSummarizer._chatbot_summary_table + "\"")
        result_summary = result_summary.fetchone()[0]
        result_summary_session = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"" + ChatbotSummarizer._chatbot_summary_session_table + "\"")
        result_summary_session = result_summary_session.fetchone()[0]
        self._connection.commit()
        return (result_summary and result_summary_session)
    
    def messages_retrieve(self, with_system=False):
        pass

    def summarize(self):
        pass