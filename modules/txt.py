import os
from datetime import datetime

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    VSplit,
    Window,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import MenuContainer, MenuItem, TextArea
from pygments.lexers import find_lexer_class_for_filename
from pygments.util import ClassNotFound


class ApplicationState:
    """Application state"""

    show_status_bar = True
    ask_for_filename = False


def run(filename):
    def get_text_from_file(filename):
        text = ""
        if filename is not None and os.path.exists(filename):
            with open(filename) as f:
                text = f.read()
        return text

    text = get_text_from_file(filename)
    lexer = None

    if filename is not None:
        try:
            lexer = find_lexer_class_for_filename(filename)
        except ClassNotFound:
            lexer = None

        lexer = PygmentsLexer(lexer)
    else:
        lexer = lexer

    # Editing area
    text_field = TextArea(
        text=text,
        lexer=lexer,
        scrollbar=True,
        line_numbers=True,
    )

    # Status bar area
    def get_datetime():
        """Get opening datetime"""
        return "Opened at " + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    status_bar_field = VSplit([Window(FormattedTextControl(get_datetime()))], height=1)

    def _no_filename_save(event):
        global filename
        filename = event.text
        with open(event.text, "wt") as f:
            f.write(text_field.text)
        ApplicationState.show_status_bar = True
        ApplicationState.ask_for_filename = False
        get_app().layout.focus(text_field)

        return True

    filename_prompt_field_text = TextArea(
        scrollbar=False,
        line_numbers=False,
        multiline=False,
        accept_handler=_no_filename_save,
    )

    filename_prompt_field = VSplit(
        [
            Window(FormattedTextControl("Path To Save File: ")),
            filename_prompt_field_text,
        ],
        height=1,
    )

    # UI main body
    body = HSplit(
        [
            text_field,
            ConditionalContainer(
                content=status_bar_field,
                filter=Condition(lambda: ApplicationState.show_status_bar),
            ),
            ConditionalContainer(
                content=filename_prompt_field,
                filter=Condition(lambda: ApplicationState.ask_for_filename),
            ),
        ]
    )

    # Keybindings
    bindings = KeyBindings()

    @bindings.add("c-d")
    def _exit(event):
        """Exit the text editor"""
        event.app.exit()

    @bindings.add("c-s")
    def _save_file(event) -> None:
        if filename is not None:
            with open(filename, "w") as f:
                f.write(text_field.text)
        else:
            ApplicationState.show_status_bar = False
            ApplicationState.ask_for_filename = True
            get_app().layout.focus(filename_prompt_field_text)

    @bindings.add("c-c")
    def _focus(event):
        """Focus on the menu"""
        event.app.layout.focus(root_container.window)

    # Menu items
    def status_bar_handler():
        ApplicationState.show_status_bar = not ApplicationState.show_status_bar

    root_container = MenuContainer(
        body=body,
        menu_items=[
            MenuItem(
                "File",
                children=[
                    MenuItem("New"),
                    MenuItem("Save"),
                    MenuItem("Exit", handler=lambda: get_app().exit()),
                ],
            ),
            MenuItem(
                "View", children=[MenuItem("Status Bar", handler=status_bar_handler)]
            ),
            MenuItem("Info", children=[MenuItem("About")]),
        ],
        key_bindings=bindings,
    )

    layout = Layout(root_container, focused_element=text_field)

    # Global style
    style = Style.from_dict({})  # empty for now

    application = Application(
        layout=layout,
        style=style,
        full_screen=True,
    )

    application.run()
