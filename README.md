# LinkedIn Auto Poster (Windows)

This repository now contains a Windows-focused app that can schedule and publish a LinkedIn post from your own laptop.

## What it does

- Lets you write a post.
- Lets you schedule date/time.
- Uses your local Chrome profile (so it can reuse your LinkedIn login session).
- Opens browser automation and posts at the scheduled time.

## Important notes

- I cannot access your laptop remotely from here.
- You must run this app on your own Windows machine.
- LinkedIn UI can change; selectors in automation might need updates.
- Use responsibly and respect LinkedIn policies.

## 1) Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2) Find your Chrome profile path

Usually:

```text
C:\Users\<YOUR_USER>\AppData\Local\Google\Chrome\User Data
```

Profile directory is often `Default` or `Profile 1`.

## 3) Run

```powershell
python app.py
```

## 4) Use the app

1. Paste your post text.
2. Choose schedule date/time (`YYYY-MM-DD HH:MM`) in local time.
3. Enter your Chrome user data directory.
4. Enter profile directory name.
5. Click **Schedule Post**.

The app keeps running until it publishes.

## Troubleshooting

- If Chrome is already open and profile is locked, close Chrome and try again.
- If LinkedIn layout changed, update selectors in `linkedin_poster.py`.
- If login is required, start Chrome manually with that profile and log in once, then retry.
