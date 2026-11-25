# Chatbot Assistant System using Python

A Django web application providing automated technical support and setup guidance. Users can register an account, log in, chat with the technical assistant, click returned links to open step-by-step setup and troubleshooting pages, browse the guide directory, and edit their personal details.

## Modules & Features

- **Register (`/register/`)**: Create an account with username, full name, email, phone, occupation, address, and password.
- **Login (`/login/`)**: Authenticate using valid credentials.
- **Chat Window (`/chat/`)**: Real-time chat interface powered by `POST /api/chat/`. Persists chat history per user and returns clickable internal guide links and official external reference links.
- **Technical Guides (`/guides/` and `/guides/<slug>/`)**: Searchable, categorized troubleshooting and setup guides (Python, Django, XAMPP/MySQL, Git/GitHub, VS Code, Wi-Fi, PC performance, BSOD, audio, Bluetooth, printers, OS updates, browser SSL/cache, database migrations, IMAP/SMTP email, and security).
- **Edit User Details (`/profile/edit/`)**: Update personal info, bio, and password.

## Tech Stack

- **Backend**: Python 3, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite by default (with commented MySQL / XAMPP configuration in `chatbot_project/settings.py`)

## Quick Start

1. Activate the virtual environment (or create one and install dependencies from `requirements.txt`):

```bash
source .venv/bin/activate
```

2. Run migrations and seed the technical knowledge base:

```bash
python manage.py migrate
python manage.py seed_kb
```

3. (Optional) Create an admin user for `/admin/`:

```bash
python manage.py createsuperuser
```

4. Start the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Running Tests

```bash
python manage.py test -v 2
```

## Optional XAMPP / MySQL Setup

1. Start Apache and MySQL in the XAMPP Control Panel and create a database named `chatbot_assistant_db` in phpMyAdmin.
2. Install a MySQL driver such as `mysqlclient` (`pip install mysqlclient`).
3. Uncomment the MySQL `DATABASES` block in `chatbot_project/settings.py` and run `python manage.py migrate && python manage.py seed_kb`.
