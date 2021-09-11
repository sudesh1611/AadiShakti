import os
import subprocess
import requests
import tempfile
import inspect
import secrets
import string
from datetime import datetime


# Variables
DEBUG_MODE = False


# Functions to print logs in somewhat better format
def InfoPrint(log):
    if DEBUG_MODE == True:
        print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} | INFO    | {inspect.stack()[1].function.ljust(15)} :: {log}')

def WarningPrint(log):
    if DEBUG_MODE == True:
        print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} | WARNING | {inspect.stack()[1].function.ljust(15)} :: {log}')

def ErrorPrint(log):
    if DEBUG_MODE == True:
        print(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} | ERROR   | {inspect.stack()[1].function.ljust(15)} :: {log}')



# Class that can be used to Download binaries/files from url
class Downloader:
    def DownloadHere(self, url, url_params = {}, out_path_dir = os.getcwd(), out_file_Name = ""):
        try:
            InfoPrint(f'Called with parameters --> {url}, {url_params}, {out_path_dir}, {out_file_Name}')
            result = requests.get(url=url,params=url_params)
            InfoPrint(f'Return status of {url} --> {result.status_code}')
            if result.ok == True:
                if out_file_Name == "":
                    out_file_Name = url.split("/")[-1].strip()
                with open(os.path.join(out_path_dir,out_file_Name), "wb") as fl:
                    fl.write(result.content)
                InfoPrint(f'Downloaded content to --> {os.path.join(out_path_dir,out_file_Name)}')
                return os.path.join(out_path_dir,out_file_Name)
            else:
                WarningPrint(f'Status was not OK, hence returning False')
                return False
        except Exception as ex:
            ErrorPrint(f'Exception occured, hence returning False. Exception --> {ex.with_traceback()}')
            return False
    
    def DownloadInTemp(self, url, url_params = {}, out_file_Name = ""):
        try:
            InfoPrint(f'Called with parameters --> {url}, {url_params}, {out_file_Name}')
            temp_dir_path = tempfile.gettempdir()
            _rand_char_length = 6
            new_dir_name = "".join(secrets.choice(string.ascii_letters) for i in range(_rand_char_length)) + "-" + "".join(secrets.choice(string.digits + string.ascii_uppercase) for i in range(_rand_char_length)) + "-" + "".join(secrets.choice(string.ascii_letters) for i in range(_rand_char_length))
            os.makedirs(os.path.join(temp_dir_path,new_dir_name))
            if os.path.exists(os.path.join(temp_dir_path,new_dir_name)):
                InfoPrint(f'Created directory successfully --> {os.path.join(temp_dir_path,new_dir_name)}')
                return self.DownloadHere(url=url, url_params=url_params, out_path_dir=os.path.join(temp_dir_path,new_dir_name), out_file_Name=out_file_Name)
            else:
                WarningPrint(f'Unable to create directory. Returning False')
                return False
        except Exception as ex:
            ErrorPrint(f'Exception occured, hence returning False. Exception --> {ex.with_traceback()}')
            return False