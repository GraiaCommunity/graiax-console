from logging import StreamHandler
from typing import Union

from loguru import logger
from rich.tree import Tree
from textual.widget import Widget
from textual.widgets import ScrollView


class ConsoleHandler(StreamHandler):
    def __init__(self, messages: "LogView") -> None:
        super().__init__(None)
        self.messages: "LogView" = messages

    def emit(self, record) -> None:
        self.messages.append(self.format(record))


class LogView(Widget):
    def __init__(self, name: Union[str, None] = None) -> None:
        name = name or "logger"
        super().__init__(name)
        self.root: Tree = Tree("", highlight=True, hide_root=True, expanded=True)
        self.handler: ConsoleHandler = ConsoleHandler(self)
        self.scroll: ScrollView = ScrollView(self, gutter=1)
        logger.remove()
        logger.add(self.handler)

    def scroll_end(self, refresh: bool = True) -> None:
        self.scroll.target_y = (
            self.scroll.window.virtual_size.height - self.scroll.size.height
        )
        self.scroll.animate("y", self.scroll.target_y, duration=0)
        if refresh:
            self.scroll.window.refresh(layout=True)

    def append(self, msg: str) -> None:
        self.root.add(msg)
        self.refresh(layout=True)
        self.scroll_end()

    def render(self) -> Tree:
        return self.root
