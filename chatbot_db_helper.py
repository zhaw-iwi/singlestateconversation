import sqlite3
import re

class ChatbotDBHelper:

    _sytem_label = "system"
    _assistant_label = "assistant"
    _user_label = "user"

    _chatbot_type_table = "chatbot_types"
    _chatbot_instance_table = "chatbot_instances"
    _chatbot_session_table = "chatbot_sessions"

    def __init__(self, database, type_id, user_id, type_name=None, type_role=None, instance_context=None, instance_starter=None):

        if type_id is None:
            raise RuntimeError("a type_id must be provided - either refer to an existing one or for a new one to be created")
        if user_id is None:
            raise RuntimeError("a user_id must be provided - either refer to an existing one or for a new one to be created")

        self._connection = None
        try:
            self._connection = sqlite3.connect(database)
        except sqlite3.Error as e:
            raise RuntimeError(" ".join(e.args))
        
        if not self._ddl_exists():
            if type_name is None or type_role is None or instance_context is None or instance_starter is None:
                raise RuntimeError("since we are creating a new database instance you must provide a type_name, type_role, instance_context, and instance_starter")                  
            self._ddl_save()
        if not self._type_exists(type_id):
            if type_name is None or type_role is None:
                raise RuntimeError("since we are creating a new chatbot type you must provide a type_name and type_role")
            self._type_save(type_id, type_name, type_role)
        if not self._instance_exists(type_id, user_id):
            if instance_context is None or instance_starter is None:
                raise RuntimeError("since we are creating a new chatbot instance you must provide a instance_context and instance_starter")
            self._instance_save(type_id, user_id, instance_context, instance_starter)

        self._type_id = type_id
        self._user_id = user_id

    def _ddl_save(self):
        cursor = self._connection
        cursor.execute("CREATE TABLE " + ChatbotDBHelper._chatbot_type_table + " (id TEXT PRIMARY KEY, name TEXT NOT NULL, role TEXT NOT NULL)")
        cursor.execute("CREATE TABLE " + ChatbotDBHelper._chatbot_instance_table + " (type TEXT NOT NULL, user TEXT NOT NULL, context TEXT NOT NULL, starter TEXT NOT NULL, PRIMARY KEY(type, user), FOREIGN KEY (type) REFERENCES " + ChatbotDBHelper._chatbot_type_table + "(id))")
        cursor.execute("CREATE TABLE " + ChatbotDBHelper._chatbot_session_table + " (id INTEGER PRIMARY KEY, type TEXT NOT NULL, user TEXT NOT NULL, t TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, who_says TEXT NOT NULL, says_what TEXT NOT NULL, is_deleted BOOLEAN DEFAULT (0), FOREIGN KEY (type, user) REFERENCES " + ChatbotDBHelper._chatbot_instance_table + "(type, user))")
        self._connection.commit()
    
    def _ddl_exists(self):
        cursor = self._connection
        result_type = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"" + ChatbotDBHelper._chatbot_type_table + "\"")
        result_type = result_type.fetchone()[0]
        result_instance = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"" + ChatbotDBHelper._chatbot_instance_table + "\"")
        result_instance = result_instance.fetchone()[0]
        result_session = cursor.execute("SELECT count(name) FROM sqlite_master WHERE type=\"table\" AND name=\"" + ChatbotDBHelper._chatbot_session_table + "\"")
        result_session = result_session.fetchone()[0]
        self._connection.commit()
        return (result_type and result_instance and result_session)
    
    def _type_save(self, type_id, name, role):
        role_normalised = re.sub(r"\s+", " ", role).strip()
        cursor = self._connection
        cursor.execute("INSERT INTO " + ChatbotDBHelper._chatbot_type_table + " (id, name, role) VALUES (\"" + type_id + "\", \"" + name + "\", \"" + role_normalised + "\")")
        self._connection.commit()
    
    def _type_exists(self, type_id):
        cursor = self._connection
        result = cursor.execute("SELECT id FROM " + ChatbotDBHelper._chatbot_type_table + " WHERE id = \"" + type_id + "\"")
        if not result:
            return None
        result = result.fetchall()  # TODO fetchone
        self._connection.commit()
        return len(result) == 1  

    def _instance_save(self, type_id, user_id, context, starter):
        context_normalised = re.sub(r"\s+", " ", context).strip()
        starter_normalised = re.sub(r"\s+", " ", starter).strip()
        cursor = self._connection
        cursor.execute("INSERT INTO " + ChatbotDBHelper._chatbot_instance_table + " (type, user, context, starter) VALUES (\"" + type_id + "\", \"" + user_id + "\", \"" + context_normalised + "\", \"" + starter_normalised + "\")")
        self._connection.commit()

    def _instance_exists(self, type_id, user_id):
        cursor = self._connection
        result = cursor.execute("SELECT type, user FROM " + ChatbotDBHelper._chatbot_instance_table + " WHERE type = \"" + type_id + "\" AND user = \"" + user_id + "\"")
        if not result:
            return None
        result = result.fetchall()  # TODO fetchone
        self._connection.commit()
        return len(result) == 1

    def info_retrieve(self):
        cursor = self._connection
        result = cursor.execute("SELECT t.name, t.role, i.context FROM " + ChatbotDBHelper._chatbot_type_table + " t, " + ChatbotDBHelper._chatbot_instance_table + " i WHERE t.id = i.type AND type = \"" + self._type_id + "\" AND user = \"" + self._user_id + "\"")
        result = result.fetchone()
        self._connection.commit()
        return {"name": result[0], "role": result[1], "context": result[2]}

    def messages_retrieve(self, with_system=False):
        cursor = self._connection
        messages = []
        if (with_system):
            # retrieve type role
            result = cursor.execute("SELECT role FROM " + ChatbotDBHelper._chatbot_type_table + " WHERE id = \"" + self._type_id + "\"")
            result = result.fetchone()
            messages.append({"role": ChatbotDBHelper._sytem_label, "content": result[0]})
            # retrieve instance context and starter
            result = cursor.execute("SELECT context FROM " + ChatbotDBHelper._chatbot_instance_table + " WHERE type = \"" + self._type_id + "\" AND user = \"" + self._user_id + "\"")
            result = result.fetchone()
            messages.append({"role": ChatbotDBHelper._sytem_label, "content": result[0]})
        # retrieve session utterances
        result = cursor.execute("SELECT who_says, says_what FROM " + ChatbotDBHelper._chatbot_session_table + " WHERE type = \"" + self._type_id + "\" AND user = \"" + self._user_id + "\" AND is_deleted = 0 ORDER BY t, id ASC")
        result = result.fetchall()
        self._connection.commit()
        for row in result:
            if not with_system:
                if row[0] != ChatbotDBHelper._sytem_label:
                    messages.append({"role": row[0], "content": row[1]})
            else:
                messages.append({"role": row[0], "content": row[1]})
        return messages

    def starter_save(self):
        cursor = self._connection
        result = cursor.execute("SELECT starter FROM " + ChatbotDBHelper._chatbot_instance_table + " WHERE type = \"" + self._type_id + "\" AND user = \"" + self._user_id + "\"")
        result = result.fetchone()
        self._connection.commit()
        self.message_save(ChatbotDBHelper._sytem_label, result[0])

    def message_save(self, who_says, says_what):
        says_what_normalised = re.sub(r"\s+", " ", says_what).strip()
        statement = "INSERT INTO " + ChatbotDBHelper._chatbot_session_table + " (type, user, who_says, says_what) VALUES (?, ?, ?, ?)"
        cursor = self._connection
        result = cursor.execute(statement, (self._type_id, self._user_id, who_says, says_what_normalised))
        self._connection.commit()
        return result.lastrowid
    
    def reset(self):
        cursor = self._connection
        cursor.execute("UPDATE " + ChatbotDBHelper._chatbot_session_table + " SET is_deleted = 1 WHERE type = \"" + self._type_id + "\" AND user = \"" + self._user_id + "\" AND is_deleted = 0")
        self._connection.commit()