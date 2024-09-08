# Telegram Job Application Tracker Bot

This is a Telegram bot for tracking job applications. The bot allows users to add, view, edit, and delete job applications, as well as search for specific applications by keyword. It also integrates with a database for storing and retrieving application data.

## Features

- Add a new job application
- View all job applications
- Update the status of an application
- Delete a single application or all applications
- Search for an application by keyword
- Supports error handling and button controls

## Prerequisites

To run this project locally, you will need:

- Python 3.7+
- A SQLite database or other supported database (configured in `db_fun.py`)
- A Telegram bot token (You can obtain one by talking to [BotFather](https://t.me/BotFather) on Telegram)

## Setup

### 1. Clone the repository

```bash
https://github.com/bsmat/tg_bot.git
cd tg_bot
```


### 2. Install dependencies
It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Environment Configuration
```bash
BOT_API_TOKEN=your-telegram-bot-token
```

### 4. Run the bot
To start the bot, run:
```bash
python bot.py
```
