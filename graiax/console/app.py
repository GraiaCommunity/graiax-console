from textual import events
from textual.app import App

from .widget.header import HeadBar
from .widget.input import Input
from .widget.log_view import LogView


class ConsoleView(App):
    async def on_load(self) -> None:
        await self.bind("enter", "send_msg")
        await self.bind("up", "scroll_up")
        await self.bind("down", "scroll_down")

    async def action_scroll_up(self) -> None:
        await self.logger.scroll.key_up()

    async def action_scroll_down(self) -> None:
        await self.logger.scroll.key_down()

    async def on_mount(self) -> None:
        self.head_bar: HeadBar = HeadBar()
        self.input: Input = Input()
        self.logger: LogView = LogView()
        self.grid = await self.view.dock_grid()
        self.grid.add_column("col")
        self.grid.add_row(fraction=1, name="upper")
        self.grid.add_row(fraction=8, name="mid")
        self.grid.add_row(fraction=2, name="lower")
        self.grid.place(self.head_bar, self.logger.scroll, self.input)

    async def on_key(self, event: events.Key) -> None:
        self.input.insert(event.key)
        if event.key == "escape":
            self.input.is_input = False
            self.head_bar.status = "No input"
        if event.key == "q":
            if not self.input.is_input:
                await self.action_quit()
        elif event.key == "i":
            self.input.is_input = True
            self.head_bar.status = "Input"
        elif event.key == "enter" and self.input.value:
            self.logger.append(self.input.clear())

    async def run_async(self) -> None:
        await self.process_messages()
