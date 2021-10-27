"""
Module containing the FTPWrapper class
"""

from ftplib import FTP
import os


class FTPWrapper(FTP):
    """Wrapper to Handle commands to an FTP server"""

    def __init__(
        self, host: str, user: str = "anonymous", passwd: str = "", port: int = 21
    ):
        super().__init__(host)

        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port

    def login(self) -> str:
        """Login. Uses `self.user` and `self.passwd` as credentials."""
        return super().login(self.user, self.passwd)

    @staticmethod
    def change_local_working_dir(path: str = "") -> None | str:
        """Changes the local working directory to `path`"""
        if path == ".":
            return os.getcwd()
        os.chdir(path)

    def get(self, path_to_file: str, local_path_to_file: str):
        """Downloads a online file at `path_to_file` as a local file at `local_path-to_file`."""
        
        with open(local_path_to_file, 'wb') as f:
            self.retrbinary(f'RETR {path_to_file}', f.write)

    def put(self, local_path_to_file: str, path_to_file: str):
        """Uploads a local file at `local_path_to_file` to the server at `path_to_file`"""

        with open(local_path_to_file, 'rb') as f:
            self.storbinary(f'STOR {path_to_file}', f.read)

    def make_directory(self, pathname: str):
        self.mkd(pathname)
    

        
