import shlex

import pwinput
from rich.console import Console
from rich.panel import Panel

from modules.ftp_wrapper import FTPWrapper


def get_formatted_message(msg: str) -> str:
    try: # Account for empty response
        code, msg = msg.split(" ", 1)
    except ValueError:
        code = msg
        msg = ''

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


if __name__ == "__main__":
    console = Console()
    console.rule("[bold red]PyFTP")

    console.print(Panel("[green]Connect to Server"))

    host = console.input("Enter Host Address 🌐: ")

    ftp = FTPWrapper(host)
    console.print(get_formatted_message(ftp.getwelcome()))

    user = console.input("Enter username 👤: ")
    password = pwinput.pwinput(prompt="Enter password 🔐: ")

    console.print(get_formatted_message(ftp.login(user, password)))

    while True:
        #try:
        try:  # Handle empty input
            cmd, *body = console.input("> ").split(" ", 1)
        except ValueError:
            continue
        cmd = cmd.lower()
        body = ' '.join(body).strip()

        match cmd:
            case 'welcome':
                console.print(get_formatted_message(ftp.getwelcome()))

            case '#':  # Execute one line python code
                try:
                    exec(body)
                except Exception as e:
                    console.print(e)

            case 'lcd':
                console.print(ftp.lcd(body))

            case 'cd':
                console.print(get_formatted_message(ftp.cd(body)))

            case 'rm':
                console.print(get_formatted_message(ftp.rm(body)))

            case 'put':
                console.print(ftp.put(body))

            case 'get':
                console.print(ftp.get(body))

            case 'ren':
                console.print(get_formatted_message(ftp.ren(*shlex.split(body))))

            case 'mkdir':
                console.print(get_formatted_message(ftp.mkdir(body)))

            case 'isfile':
                console.print(ftp.is_file(body))
        #except Exception as e:
        #    console.print(e)