# Auto Migration Script for .NET Projects

This repository contains a Python script (`Auto_Migration.py`) designed to automate the process of generating and managing Entity Framework Core migrations for a .NET backend application.

## Overview

The `Auto_Migration.py` script is used to streamline the development process by handling migrations in a consistent and automated manner. It integrates with the Entity Framework Core tools to:

- Pull the latest changes from the repository
- Add new migrations with meaningful names reflecting the changes
- Remove migrations if necessary
- Commit and push changes to a specified branch in the repository

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Python 3.x
- .NET Core SDK
- Entity Framework Core CLI tools
- Git

## Usage

To use the script, follow these steps:

1. Clone the repository and navigate to the script's directory.
2. Open a terminal or command prompt.
3. Execute the script with the following command:

```bash
python Auto_Migration.py
