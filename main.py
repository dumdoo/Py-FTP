from ftplib import all_errors
from modules.ftp_wrapper import FTPWrapper
from ftplib import all_errors as FTP_all_errors
import sys

if __name__ == "__main__":
    ftp = FTPWrapper("192.168.1.1")
