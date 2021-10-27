from ftplib import all_errors
from modules.ftp_wrapper import FTPWrapper
from ftplib import all_errors as FTP_all_errors
import sys
import atexit

if __name__ == "__main__":
    ftp = FTPWrapper("192.168.1.1", user="admin", passwd="admin")

    @atexit.register
    def at_exit():
        """At exit, gracefully and politely QUIT the connection. If this fails close the connection unilaterally."""
        try:
            ftp.quit()
        except FTP_all_errors:
            ftp.close()

    print(ftp.getwelcome())
    print(ftp.login())
