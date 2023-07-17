import logging
from colorama import init, Fore, Style
import json

def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False

def format_log(*args, **kwargs):
    log_message = f"{Fore.GREEN}<---- START ---->\n"

    # Collect positional arguments
    if args:
        log_message += "Positional arguments:\n"
        for index, arg in enumerate(args, start=1):
            log_message += f"  Arg {index}: [{Style.RESET_ALL}{arg}{Fore.GREEN}]\n"

    # Collect keyword arguments
    if kwargs:
        log_message += "Keyword arguments:\n"
        for key, value in kwargs.items():
            if is_json_serializable(value):
                value = json.dumps(value, indent=4)
            log_message += f"  [{key}]: [{Style.RESET_ALL}{value}{Fore.GREEN}]\n"

    log_message += f"<---- END ---->\n{Style.RESET_ALL}"
    return log_message

def log_info(*args, **kwargs):
    # Log the message
    logging.info(format_log(*args, **kwargs))

def log_debug(*args, **kwargs):
    # Log the message
    logging.debug(format_log(*args, **kwargs))