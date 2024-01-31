# A Chatbot using GPT and a Database with a Front-End

<picture>
 <img alt="a close up of a person holding a cell phone" src=".readme/pradamas-gifarry-889Qh5HJj4I-unsplash.jpg">
</picture>

## Create and deploy a chatbot

Follow the 9 steps below to create a chatbot and deploy it on pythonanywhere.

`<github codespaces>`

1. Use the notebook **chatbot_setup.ipynb** to create a chatbot.\
[![Open Notebook in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/zhaw-iwi/singlestateconversation)
2. Download the database file **database/chatbot.db**.

`</github codespaces>`

`<pythonanywhere>`

3. Create an account at pythonanywhere\
    [https://www.pythonanywhere.com/registration/register/beginner](https://www.pythonanywhere.com/registration/register/beginner)\
    Note: The user name chosen will be part of your URL (PYTHONANYWHERE_USERNAME.pythonanywhere.com)
4. Create a web application (in the Web tab)
    - Python Web Framework: Flask, choose the latest version.
    - Path: Optionally change ".../my_site/..." to meaningful PYTHONANYWHERE_WEBAPPNAME
5. Start a Bash console (in the Consoles tab) and enter the following commands:
    - `pip install openai`
    - `cd mysite` &rarr; if you have a different PYTHONANYWHERE_WEBAPPNAME, replace ***mysite*** with yours.
    - `rm -r *`
    - `git clone https://github.com/zhaw-iwi/singlestateconversation .`\
    Note: The dot at the end is necessary.
6. Edit file **flask_app.py** (in the Files tab) and set the following values.\
    PYTHONANYWHERE_USERNAME\
    PYTHONANYWHERE_WEBAPPNAME
7. Edit the file **chatbot/openai_template.py** and save it as **chatbot/openai.py**. Set the following keys.\
    OPENAI_KEY = "Your OpenAI API Key in quotes"\
    OPENAI_MODEL = "Model name in quotes, e.g. gpt-3.5-turbo-16k"
8. Upload the database file **database/chatbot.db** you downloaded from GitHub Codespaces (Step 2) into the folder **database/**.

`</pythonanywhere>`

9. Access your chatbot by entering the URL into your browser.\
https://[PYTHONANYWHERE_USERNAME].pythonanywhere.com/[type_id]/[user_id]/chat

#### If something doesn't work as expected
- Reload your Web Application:\
Navigate to your web application (in the Web tab) and press the green button to reload it (required for all changes except for content in folder database/ and static/)
- Have a look at the Error Log:\
Navigate to your web application (in the Web tab) and scroll down to the Log files. Study the latest error at the bottom of the Error log.

## A Chatbot using GPT and a Database
This allows multiple chatbot types (e.g. a health coach and a learning assistant) to be created. Multiple chatbot instances can be created per chatbot type (e.g. a health coach for user X and user Y, and a learning assistant for user P and user Q). Both, types and instances are stored with and referenced by an ID (e.g. a UUID) in the database.

This can support the deployment of chatbots in a web backend (state-less). For example, the IDs of the type and instance can be read from parameters of a URL that users have received from you.

A chatbot is created with the following arguments.
- database_file: File of SQLite (in Folder data/)
- type_id: Reference to a chatbot type (existing or new one)
- instance_id: Reference to chatbot instance (existing or new one)
- type_role: Role prompt of chatbot type (will be turned into a first prompt with role:system)
- instance_context: Context prompt of chatbot instance (will be turned into a second prompt with role:system)
- instance_starter: Prompt that will be used to generate an initial message to the user (will be turned into a third prompt with role:system)

The following functions are meant to be used from an application (e.g. from controllers of a REST API).
- conversation_retrieve(with_system=False): Retrieve the previous conversation history (default: without prompts with role:system)
- start(): Returns an initial message to the user (Resulting from instance_starter prompt)
- respond(user_says): Returns an assistance response to user_says
- info_retrieve(): Returns the chatbot name, type role and instance context
- reset(): Resets the conversation so far