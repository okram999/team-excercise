# AnyState IT Desktop Support Application (Python)

A Python desktop application that provides state employees with direct access to IT support through a chat interface, backed by Amazon Connect and AI-assisted responses.

## Features

- AI-assisted IT support available 24/7
- Live agent chat support during business hours (Monday to Friday, 9 AM to 5 PM)
- Phone callback request option
- Windows user identification
- Integration with Amazon Connect for backend support

## Technical Overview

This application is built using:
- Python 3 with Tkinter for the UI
- boto3 for AWS Connect integration
- Threading for simulating async operations

## Requirements

- Python 3.6+
- boto3 library
- Windows 10 or later (for production use)
- Access to AnyState's Amazon Connect instance

## Installation

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python anystate_it_support.py
   ```

## Deployment

For production deployment, the application can be packaged into an executable using PyInstaller:

```
pip install pyinstaller
pyinstaller --onefile --windowed anystate_it_support.py
```

The resulting executable can be deployed via Group Policy to all domain-joined computers in the AnyState government network.

## Security

In production, the application should be configured to:
- Use Windows domain authentication
- Connect securely to AWS services
- Store no sensitive information locally