import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Initialize logging
logging.basicConfig(filename='migration_automation.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Define project settings for .NET backend
script_directory = Path(__file__).parent if __file__ else Path.cwd()
backend_project_path = script_directory.parent / "Back" / "Infrastructure"
backend_repo_path = script_directory.parent / "Back"

# Function to run shell commands
def run_command(command, working_directory=None):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, text=True, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        logging.error(f"Command '{command}' failed with error: {stderr}")
        raise subprocess.CalledProcessError(process.returncode, command, output=stdout, stderr=stderr)
    return stdout.strip()

# Function to pull latest changes
def pull_latest_changes(repo_path):
    try:
        os.chdir(repo_path)
        run_command('git checkout AutoMigrationtest')
        logging.info("Checked out AutoMigrationtest.")
        run_command('git pull origin AutoMigrationtest')
        logging.info("Pulled last changes.")
    except Exception as e:
        logging.error(f"Failed to pull latest changes: {e}")
        sys.exit(1)

# Function to create a unique migration name
def create_migration_name():
    # Using a timestamp for uniqueness
    return "Migration" + datetime.now().strftime("%Y%m%d%H%M%S")

# Function to add migration
def add_migration(backend_project_path, migration_name):
    try:
        os.chdir(backend_project_path)
        run_command(f"dotnet ef migrations add {migration_name} --project {backend_project_path}")
        logging.info(f"Migration {migration_name} added.")
    except Exception as e:
        logging.error(f"An error occurred while adding migration {migration_name}: {e}")
        sys.exit(1)

# Function to push changes
def push_changes(repo_path, migration_name):
    try:
        os.chdir(repo_path)
        run_command('git add .')
        run_command(f'git commit -m "Added migration {migration_name}"')
        run_command('git push origin AutoMigrationtest')
        logging.info("Changes pushed to repository.")
    except Exception as e:
        logging.error(f"An error occurred while pushing changes: {e}")
        sys.exit(1)

# Execute the workflow
migration_name = create_migration_name()
pull_latest_changes(backend_repo_path)
add_migration(backend_project_path, migration_name)
push_changes(backend_repo_path, migration_name)
