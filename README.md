# A Chatbot using GPT and a Database with a Front-End

<picture>
 <img alt="a close up of a person holding a cell phone" src=".readme/pradamas-gifarry-889Qh5HJj4I-unsplash.jpg">
</picture>

### Application & Deployment
- Use the notebook **chatbot_client.ipynb** to create chatbot types and instances.
- Follow the instructions at the bottom to create and deploy a chatbot (on pythonanywhere)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zhaw-iwi/singlestateconversation/blob/main/google_colab.ipynb)

### A Chatbot using GPT and a Database
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
- start(): Returns an initial message to the user (Resulting from instance_starter prompt)
- respond(user_says): Returns an assistance response to user_says
- info_retrieve(): Returns the chatbot name, type role and instance context
- reset(): Resets the conversation so far

### Create & Deploy a Chatbot (pythonanywhere)
Follow the 9 steps below to create and deploy a chatbot on pythonanywhere.

`<pythonanywhere>`
1. Create account
    User name will be part of your URL: PYTHONANYWHERE_USERNAME.pythonanywhere.com
2. Create web application
    - Python Web Framework: Flask, choose the latest version.
    - Path: Optionally change ".../my_site/..." to meaningful PYTHONANYWHERE_WEBAPPNAME
3. Create the following folders in the root folder of your web application
    - chatbot/
    - database/
    - static/
    - templates/
`</pythonanywhere>`

`<local>`
4. Edit file flask_app.py and set the following values
    - PYTHONANYWHERE_USERNAME
    - PYTHONANYWHERE_WEBAPPNAME
5. Create file chatbot/apikey.py with the following content
    OPENAI_KEY = "your OpenAI API key"
6. Use notebook chatbot_client.jpynb
    Create a new chatbot (type, instance, starter)
    This will create/update file chatbot.db in your local folder database/
`</local>`

`<pythonanywhere>`
7. Upload the following files (from local to pythonanywhere)
    - chatbot/chatbot.py, chatbot/persistence.py, chatbot/apikey.py to folder chatbot/
    - database/chatbot.db to folder database/
    - static/* to folder static/
    - templates/index.html to folder templates/
    - /flask_app.py to / (the root folder of your web appliation)
8. Bash Console: pip install openai
`</pythonanywhere>`

`<local>`
9. Access your chatbot by entering the URL into your browser
    - Example of format: https://[your pythonanywhere user name].pythonanywhere.com/[type id]/[user_id]/chat
`</local>`

If something doesn't work as expected
- Reload web application
    Navigate to your web application and press the green button to reload it (required for all changes except for content in folder static/)
- Have a look at the Error Log
    Study the latest error at the bottom of this file
