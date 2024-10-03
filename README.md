# A.L.V.E.X. (Adaptive Learning Virtual EXecutive)

A.L.V.E.X. is a personal assistant AI system inspired by J.A.R.V.I.S. It utilizes natural language processing (NLP) powered by OpenAI's GPT, voice recognition, and PC control capabilities to create a seamless interaction with your computer. The assistant is designed to execute commands in Dutch and respond intelligently to queries and requests.

## Features

- **Natural Language Processing (Dutch)**: Understands commands and queries in Dutch using OpenAI's GPT-4.
- **PC Control**: A.L.V.E.X. can open applications, shut down, restart the system, and provide system information like CPU and memory usage.
- **Voice Recognition and Speech Synthesis**: Recognizes your voice commands and speaks the responses (optional).
- **Modular and Extensible**: Easily customizable for future smart device control or other advanced features.

## How It Works

A.L.V.E.X. operates as a Flask-based web server that listens for requests from users and executes commands based on the input. Commands can be either text-based or voice-based (if speech recognition is enabled). 

The system integrates:
- **OpenAI GPT-4** for natural language understanding and responses.
- **Speech Recognition** for handling voice commands (optional).
- **System Control Functions** to interact with the operating system directly (open apps, check system info, shutdown, etc.).

## Prerequisites

- Python 3.6 or higher
- OpenAI API key (for GPT-4)
- Flask (Python web framework)
- Git (for version control and pushing updates to GitHub)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/alvex-assistant.git
