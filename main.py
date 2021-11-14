import shlex
import subprocess

import pwinput
from rich.console import Console
from rich.panel import Panel

from modules.ftp_wrapper import FTPWrapper
from modules.txt import run as txt_run


def get_formatted_message(msg: str) -> str:
    try:  # Account for empty response
        code, msg = msg.split(" ", 1)
    except ValueError:
        code = msg
        msg = ""

    color = "white"
    extra = ""  # Extra symbol to add to the msg
    if code.startswith("1"):
        color = "#ADFF2F"
    elif code.startswith("2"):
        color = "green"
        extra = "✔"
    elif code.startswith("3"):
        color = "yellow"
    elif code.startswith("4"):
        color = "orange"
    elif code.startswith("5"):
        color = "red"
        extra = "❌"

    return f"[{color}]{extra + ' ' + msg} " + "{" + code + "}"


def prompt():
    try:
        host = console.input("Enter Host Address 🌐: ")
        ftp = FTPWrapper(host)
        console.print(get_formatted_message(ftp.getwelcome()))

        user = console.input("Enter username 👤: ")

        console.print(
            get_formatted_message(
                ftp.login(user, pwinput.pwinput(prompt="Enter password 🔐: "))
            )
        )

    except Exception as e:
        console.print(e)
    while True:
        try:
            try:  # Handle empty input
                cmd, *body = console.input("> ").split(" ", 1)
            except ValueError:
                continue
            cmd = cmd.lower()
            body = " ".join(body).strip()

            if cmd == "welcome":
                console.print(get_formatted_message(ftp.getwelcome()))

            elif cmd == "#":  # Execute one line python code
                try:
                    exec(body)
                except Exception as e:
                    console.print(e)

            elif cmd == "lcd":
                console.print(ftp.lcd(body))

            elif cmd == "cd":
                console.print(get_formatted_message(ftp.cd(body)))

            elif cmd == "rm":
                console.print(get_formatted_message(ftp.rm(body)))

            elif cmd == "put":
                console.print(ftp.put(body))

            elif cmd == "get":
                console.print(ftp.get(body))

            elif cmd == "ren":
                console.print(get_formatted_message(ftp.ren(*shlex.split(body))))

            elif cmd == "mkdir":
                console.print(get_formatted_message(ftp.mkdir(body)))

            elif cmd == "isfile":
                console.print(ftp.is_file(body))

            elif cmd == "open":
                console.print(Panel("[green]Connect to Server"))

                host = console.input("Enter Host Address 🌐: ")

                ftp = FTPWrapper(host)
                console.print(get_formatted_message(ftp.getwelcome()))

                user = console.input("Enter username 👤: ")

                console.print(
                    get_formatted_message(
                        ftp.login(user, pwinput.pwinput(prompt="Enter password 🔐: "))
                    )
                )
            

            elif cmd in ["bye", "quit", "exit"]:
                raise SystemExit

            elif cmd == "txt":
                txt_run(body)

            elif cmd == "!":
                subprocess.run(body, shell=True)

            elif cmd == "ls":
                console.print(ftp.ls(body))

            else:
                console.print(f'[red bold]Unknown Command "{cmd}"')

        except Exception as e:
            console.print(e)


if __name__ == "__main__":
    console = Console()
    console.rule("[bold red]Py-FTP")

    console.print(Panel("[green]Connect to Server"))

    try:
        prompt()
    except KeyboardInterrupt:
        raise SystemExit
