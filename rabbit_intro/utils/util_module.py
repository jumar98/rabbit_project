from datetime import datetime
import smtplib
from .credentials import EMAIL, SEND_TO, PASSWORD

MESSAGE_TYPE = (
    "debug",
    "info",
    "warning",
    "error",
)

class MessageTypeError(Exception):
    pass

class Logger:

    @staticmethod
    def logs_in_file(logs_type, message):
        with open(f'{logs_type}.txt', 'a+') as f:
            f.write(f'{datetime.now()} : {message}\n')

    @staticmethod
    def send_email(message):
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, SEND_TO, message)

    @staticmethod
    def filter_message(receive_type, body_dict):
        if receive_type == 'debug':
            print(f"Receive <{body_dict['type']}> :  {body_dict['message']}")
            Logger.logs_in_file(receive_type, body_dict['message'])
            Logger.send_email(body_dict['message'])
        elif receive_type == 'info' and body_dict['type'] in ['info', 'warning', 'error']:
            print(f"Receive <{body_dict['type']}> :  {body_dict['message']}")
            Logger.logs_in_file(receive_type, body_dict['message'])
            Logger.send_email(body_dict['message'])
        elif receive_type == 'warning' and body_dict['type'] in ['warning', 'error']:
            print(f"Receive <{body_dict['type']}> :  {body_dict['message']}")
            Logger.logs_in_file(receive_type, body_dict['message'])
            Logger.send_email(body_dict['message'])
        elif receive_type == 'error' and body_dict['type'] == 'error':
            print(f"Receive <{body_dict['type']}> :  {body_dict['message']}")
            Logger.logs_in_file(receive_type, body_dict['message'])
            Logger.send_email(body_dict['message'])
