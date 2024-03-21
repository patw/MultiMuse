# MultiMuse

One of the significant benefits of Large Language Models (LLMs) is their ability to serve as a sounding board for ideas and assist in problem-solving. MultiMuse is a unique tool that allows you to configure multiple distinct personalities, each providing a fresh viewpoint on a given question. 

While its primary purpose may lean more towards entertainment than practicality, it offers an engaging experience. 

This tool is powered by Mistral.ai.

![UI Screenshot](images/ui.png)

## Basic Installation

```
pip install -r requirements.txt
```

## Configuration

* Get an API key from Mistral.ai.
* Copy the sample.env file to .env and edit this file. 
* Use your mistral API key in the API_KEY field.
* Edit the advisors.json if you want different advisors

## Running

### MacOS / Linux

```
python3 -m flask run
```

### Windows

```
flask run
```