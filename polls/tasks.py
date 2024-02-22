# tasks.py

from celery import shared_task

@shared_task
def print_message(message):  # Accept the message as an argument
    print(f"Scheduled task: {message}")
