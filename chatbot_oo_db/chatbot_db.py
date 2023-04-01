import openai
openai.api_key = "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"
openai.organization = "org-URhHRj9qqmQqR8yZZNJcRClX"

from chatbot_db_helper import ChatbotDBHelper

class Chatbot:
    
    default_type_role = "You are a kind, respectful, and symapthetic coach."
    default_instance_context = "You are now having a coaching session with the user."
    default_instance_starter = "Create a short prompt to greet the user."

    def __init__(self, database_file, type_id, user_id, type_role=None, instance_context=None, instance_starter=None):
        
        if database_file is None:
            raise RuntimeError("a database file path must be provided")
        if type_id is None:
            raise RuntimeError("a type_id must be provided - either refer to an existing type or for a new type to be created")
        if user_id is None:
            raise RuntimeError("a user_id must be provided - either refer to an existing user or for a instance to be created")
        
        if (type_role is not None or instance_context is not None or instance_starter is not None) and (type_role is None or instance_context is None or instance_starter is None):
            raise RuntimeError("if any of type/instance configuration is provided then all of type/instance configurations must be provided")
        
        self._db_helper = ChatbotDBHelper(
            database=database_file,
            type_id=type_id,
            user_id=user_id,
            type_role=type_role,
            instance_context=instance_context,
            instance_starter=instance_starter
        )

    def _append_assistant(self, content):
        self._db_helper.message_save(ChatbotDBHelper._assistant_label, content)

    def _append_user(self, content):
        self._db_helper.message_save(ChatbotDBHelper._user_label, content)

    def _openai(self):
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self._db_helper.messages_retrieve(with_system=True),
            max_tokens=256
        )
        response = chat.choices[0].message.content
        return response

    def conversation_retrieve(self, with_system=False):
        return self._db_helper.messages_retrieve(with_system)

    def starter(self):
        self._db_helper.starter_save()
        response = self._openai()
        self._append_assistant(response)
        return response

    def response_for(self, request):
        if request:
            self._append_user(request)
            response = self._openai()
            self._append_assistant(response)
            return response