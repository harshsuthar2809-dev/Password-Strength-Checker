# Password Strength Checker

## Overview
A beginner-friendly Python cybersecurity project that estimates password strength using password length, character variety, and common-pattern checks.

## Features
- Five strength levels: Very Weak, Weak, Moderate, Strong, and Very Strong.
- Live password strength meter and checklist.
- Checks length, lowercase letters, uppercase letters, numbers, and special characters.
- Suggestions to improve password quality.
- Show/hide password option.
- Educational entropy estimate.
- No database or password-file storage is implemented.

## Requirements
- Python 3.9 or newer
- Flask

## Run the single Python file on Windows
1. Download `sutharharshb._passwordstrenghtchecker.py`.
2. Open Command Prompt in the folder containing the file. If it is in Downloads, run:

   ```cmd
   cd %USERPROFILE%\Downloads
   ```

3. Install Flask:

   ```cmd
   python -m pip install Flask
   ```

4. Start the application:

   ```cmd
   python sutharharshb._passwordstrenghtchecker.py
   ```

5. Open this address in your browser:

   `http://127.0.0.1:5000`

Keep the Command Prompt window open while using the application. Press `Ctrl+C` in that window to stop the server.

## Run the folder-based Flask version
If you are using the version with `app.py` and `templates/index.html`, run these commands from that project folder:

```cmd
python -m pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## Privacy and security note
Use a fictional sample password when demonstrating the project. Do not enter a password that you use for a real account. If the app is deployed publicly, HTTPS should be used.

## Limitations
This is an educational estimate, not a guarantee that a password is secure or a password-cracking simulation. The entropy estimate is approximate, and the app does not check breached-password databases. Use long, unique passwords, a password manager, and multi-factor authentication.
