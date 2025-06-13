# AnyState IT Desktop Support Application

A Windows desktop application that provides state employees with direct access to IT support through a chat interface, backed by Amazon Connect and AI-assisted responses.

## Features

- AI-assisted IT support available 24/7
- Live agent chat support during business hours (Monday to Friday, 9 AM to 5 PM)
- Phone callback request option
- Windows domain authentication for seamless user identification
- Integration with Amazon Connect for backend support

## Technical Overview

This application is built using:
- .NET 6.0 with WPF for the UI
- Amazon Connect for chat and callback functionality
- Windows domain authentication for user identification

## Requirements

- Windows 10 or later
- .NET 6.0 Runtime
- Domain-joined Windows computer
- Access to AnyState's Amazon Connect instance

## Deployment

The application is deployed via Group Policy to all domain-joined computers in the AnyState government network.

## Support

For issues with the application, please contact the IT Support team at support@anystate.gov.

## Security

The application leverages existing security measures, including domain-joined computer authentication and integration with the state's current Amazon Connect instance.