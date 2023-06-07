# Chatbot with Database and Front-End

<picture>
 <img alt="a close up of a person holding a cell phone" src=".readme/pradamas-gifarry-889Qh5HJj4I-unsplash.jpg">
</picture>

### Application & Deployment
To create your own bot and to deploy it on pythonanywhere follow the instructions in pythonanywhere.txt. Have a look at the code in the Notebook chatbot_client.ipynb to see how types and instances are created and used.

### Object-Oriented Chatbot using GPT and a Database
This allows multiple chatbot types (e.g. a health coach and a learning assistant) to be created. Multiple chatbot instances can be created per chatbot type (e.g. for User X and User Y). Both, type and instance are stored and referenced with an ID (e.g. with a UUID) in the database.

This can support the deployment of chatbots in a web backend (state-less). For example, the UUIDs of the type and instance can be read as URL parameters from a URL that users have received from you.

A chatbot is created with the following arguments.
- database_file: File of SQLite (in Folder data/)
- type_id: Reference to chatbot type
- instance_id: Reference to chatbot instance (typically one per user - however, may also be shared by multiple users)
- type_role: Role of chatbot type (will be turned into a first prompt with role:system)
- instance_context: Context of chatbot instance (will be turned into a second prompt with role:system)
- instance_starter: Will be used to generate an initial message to the user (will be turned into a final prompt with role:system)

The following functions are meant to be used from an application (e.g. from controllers of a REST API).
- conversation_retrieve(with_system=False): Retrieve the previous conversation history (default: without prompts with role:system)
- starter(): Returns an initial message to the user (Resulting from instance_starter prompt)
- response_for(user_says): Returns an assistance response to user_says
