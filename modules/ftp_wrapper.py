"""
Module containing the FTPWrapper class
"""

import atexit
import ftplib
import os
from ftplib import FTP


class FTPWrapper(FTP):
    """Wrapper to Handle commands to an FTP server"""

    def __init__(self, host: str, port: int = 21):
        super().__init__(host)

        self.host = host
        self.port = port

        # Add Aliases
        self.ren = self.rename
        self.mkdir = self.mkd

        atexit.register(
            self._at_exit, self
        )  # register `self._at_exit` to be called at exit

    @staticmethod
    def lcd(path: str) -> str:
        """Changes the local working directory to `path`"""
        if path == ".":
            return os.getcwd()
        os.chdir(path)
        return f"Changed to {path}"

    def cd(self, path: str) -> str:
        if path == ".":
            return self.pwd()
        return self.cwd(path)

    def get(self, path_to_file: str) -> str:
        """Downloads a remote file at `path_to_file` as a local file."""

        with open(path_to_file, "wb") as f:
            return self.retrbinary(f"RETR {path_to_file}", f.write)

    def put(self, path_to_file: str) -> str:
        """Uploads a local file at `local_path_to_file`"""

        with open(path_to_file, "rb") as f:
            return self.storbinary(f"STOR {path_to_file}", f.read)

    def is_file(self, path: str) -> bool:
        try:
            self.size(path)
            return True
        except ftplib.error_perm:
            return False

    def rm(self, path: str) -> str:
        """Removes the file or folder at `path`"""
        if self.is_file(path):
            return self.delete(path)
        return self.rmd(path)

    @staticmethod
    def _at_exit(self):
        """At exit, gracefully and politely QUIT the connection. If this fails close the connection unilaterally."""
        try:
            self.quit()
        except ftplib.all_errors:
            self.close()
