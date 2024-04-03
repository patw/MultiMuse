# Basic flask stuff for building http APIs and rendering html templates
from flask import Flask, render_template, request

# Bootstrap integration with flask so we can make pretty pages
from flask_bootstrap import Bootstrap

# Flask forms integrations which save insane amounts of time
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Parallel calls to Mistral.ai
from concurrent.futures import ThreadPoolExecutor

# Basic python stuff
import os
import json

# Some nice formatting for code
import misaka

# Import the mistral stuff
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Nice way to load environment variables for deployments
from dotenv import load_dotenv
load_dotenv()

# Get the LLM
mistral_client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])
model_name = os.environ["MODEL_NAME"]

# Get app name
app_name = os.environ["APP_NAME"]

# Load the advisors
with open("advisors.json", 'r',  encoding='utf-8') as file:
    advisors = json.load(file)

# Get the advisor list
advisor_list = []
for advisor in advisors:
    advisor_list.append(advisor["name"])

# Create the Flask app object
app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

# Make it pretty because I can't :(
Bootstrap(app)

# A form for asking your external brain questions
class QuestionForm(FlaskForm):
    question = StringField('Question 💬', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Call mistral model
def llm_mistral(prompt, system_message, temperature):
    messages = [ChatMessage(role="system", content=system_message), ChatMessage(role="user", content=prompt)]
    response = mistral_client.chat(model=model_name, temperature=temperature, messages=messages)
    return response.choices[0].message.content

# The default question view
@app.route('/', methods=['GET', 'POST'])
def index():

    # Question form for the external brain
    form = QuestionForm()
    results = []

    # If user is prompting send it
    if form.validate_on_submit():

         # Get the form variables
        form_result = request.form.to_dict(flat=True)
        q = form_result["question"]

         # Create a ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Use executor.map to parallelize the llm_mistral function calls
            for advisor, raw_result in zip(advisors, executor.map(llm_mistral, [q]*len(advisors), [advisor["role"] for advisor in advisors], [0.7]*len(advisors))):
                name = advisor["name"]
                formatted_result = misaka.html(raw_result)
                results.append({"name": name, "advice": formatted_result})
    
    # Spit out the template
    return render_template('index.html', results=results, app_name=app_name, advisor_list=advisor_list, form=form)