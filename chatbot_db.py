import openai
openai.api_key = "Your https://platform.openai.com/ API key here"

from chatbot_db_helper import ChatbotDBHelper

class Chatbot:
    
    default_type_name = "Coach"
    default_type_role = "Du bist ein achtsamer Coach. Du führst Gespräche mit einem Benutzer. Ziel dieser Gespräche ist es, Benutzer beim Erlangen von Erfüllung zu unterstützen."
    default_instance_context = "Du führst jetzt solch ein Gespräch mit einem Benutzer. Du sprichst mit dem Benutzer in Du-Form. Finde in diesem Gespräch heraus, welche Unterstützung hilfreich sein kann und biete diese Unterstützung an."
    default_instance_starter = "Erzeuge eine kurze Begrüssung, um das Gespräch mit dem Benutzer zu eröffnen."

    def __init__(self, database_file, type_id, user_id, type_name=None, type_role=None, instance_context=None, instance_starter=None):
        
        if database_file is None:
            raise RuntimeError("a database file path must be provided")
        if type_id is None:
            raise RuntimeError("a type_id must be provided - either refer to an existing type or for a new type to be created")
        if user_id is None:
            raise RuntimeError("a user_id must be provided - either refer to an existing user or for a instance to be created")
        
        if (type_name is not None or type_role is not None or instance_context is not None or instance_starter is not None) and (type_name is None or type_role is None or instance_context is None or instance_starter is None):
            raise RuntimeError("if any of type/instance configuration is provided then all of type/instance configurations must be provided")
        
        self._db_helper = ChatbotDBHelper(
            database=database_file,
            type_id=type_id,
            user_id=user_id,
            type_name=type_name,
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
        )
        response = chat.choices[0].message.content
        return response

    def info_retrieve(self):
        return self._db_helper.info_retrieve()
    
    def conversation_retrieve(self, with_system=False):
        return self._db_helper.messages_retrieve(with_system)

    def starter(self):
        self._db_helper.starter_save()
        response = self._openai()
        self._append_assistant(response)
        return response

    def response_for(self, user_says):
        if user_says is None:
            raise RuntimeError("user_says must not be None")
        self._append_user(user_says)
        assistant_says = self._openai()
        self._append_assistant(assistant_says)
        return assistant_says
    
    def reset(self):
        self._db_helper.reset()