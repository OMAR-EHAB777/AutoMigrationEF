#region imports

import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
#endregion
#region Initialize logging
logging.basicConfig(filename='migration_automation.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
# Define a StreamHandler to log to the console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# Add the StreamHandler to the root logger
logging.getLogger().addHandler(console_handler)
#endregion

#region Define project settings for .NET backend
script_directory = Path(__file__).parent if __file__ else Path.cwd()
backend_project_path = Path("D:/OnlineOrdering/Back/Infrastructure")
backend_repo_path = Path("D:/OnlineOrdering/Back")
#endregion

#region Function to run shell commands
def run_command(command, working_directory=None):
    """
    Run a shell command.

    Args:
        command (str): The command to run.
        working_directory (str): The working directory for the command (default: None).

    Returns:
        str: The stdout output of the command.
    
    Raises:
        subprocess.CalledProcessError: If the command returns a non-zero exit status.
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_directory, text=True, shell=True)
    stdout, stderr = process.communicate()
    stdout_str = stdout.decode('utf-8') if isinstance(stdout, bytes) else stdout
    stderr_str = stderr.decode('utf-8') if isinstance(stderr, bytes) else stderr
    if process.returncode != 0:
        logging.error(f"Command '{command}' failed with error: {stderr_str}")
        raise subprocess.CalledProcessError(process.returncode, command, output=stdout_str, stderr=stderr_str)
    logging.info(f"Command output:\n{stdout_str}")
    return stdout.strip()
#endregion

#region Function to pull latest changes
def pull_latest_changes(repo_path):
    """
    Pull the latest changes from the Git repository.

    Args:
        repo_path (str): The path to the Git repository.

    Raises:
        subprocess.CalledProcessError: If the Git commands fail.
    """
    try:
        os.chdir(repo_path)
        run_command('git checkout AutoMigrationtest')
        logging.info("Checked out AutoMigrationtest.")
        run_command('git pull origin AutoMigrationtest')
        logging.info("Pulled last changes.")
    except Exception as e:
        logging.error(f"Failed to pull latest changes: {e}")
        sys.exit(1)
#endregion

#region Function to create a unique migration name
def create_migration_name():
    """
    Create a unique migration name based on the current timestamp.

    Returns:
        str: The unique migration name.
    """
    # Using a timestamp for uniqueness
    return "Migration" + datetime.now().strftime("%Y%m%d%H%M%S")
#endregion

#region Function to add migration

def add_migration(backend_project_path, migration_name):
    """
    Adds a migration to the specified .NET backend project using Entity Framework Core.

    Parameters:
        backend_project_path (str or Path): The path to the .NET backend project where the migration will be added.
        migration_name (str): The name of the migration to be added.

    Raises:
        subprocess.CalledProcessError: If the subprocess command fails.
        Exception: If an unexpected error occurs during the migration addition process.

    Notes:
        This function changes the current working directory to the specified backend project path
        before running the migration command.

    Example:
        add_migration("D:/OnlineOrdering/Back/Infrastructure", "InitialMigration")
    """
    try:
        os.chdir(backend_project_path)
        run_command(f"dotnet ef migrations add {migration_name} --project {backend_project_path}")
        logging.info(f"Migration {migration_name} added.")
    except Exception as e:
        logging.error(f"An error occurred while adding migration {migration_name}: {e}")
        sys.exit(1)
#endregion

#region Function to push changes
def push_changes(repo_path, migration_name):
    """
    Pushes changes to the Git repository after adding a migration.

    Parameters:
        repo_path (str or Path): The path to the Git repository.
        migration_name (str): The name of the migration that was added.

    Raises:
        subprocess.CalledProcessError: If the subprocess command fails.
        Exception: If an unexpected error occurs during the push process.

    Notes:
        This function changes the current working directory to the specified repository path
        before executing Git commands to add, commit, and push changes.

    Example:
        push_changes("D:/OnlineOrdering/Back", "InitialMigration")
    """
    try:
        os.chdir(repo_path)
        run_command('git add .')
        run_command(f'git commit -m "Added migration {migration_name}"')
        run_command('git push origin AutoMigrationtest')
        logging.info("Changes pushed to repository.")
    except Exception as e:
        logging.error(f"An error occurred while pushing changes: {e}")
        sys.exit(1)
#endregion

#region Execute the workflow
migration_name = create_migration_name()
pull_latest_changes(backend_repo_path)
add_migration(backend_project_path, migration_name)
push_changes(backend_repo_path, migration_name)
#endregion