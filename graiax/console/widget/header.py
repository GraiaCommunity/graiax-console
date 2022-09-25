from rich.console import RenderableType
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text
from textual.reactive import Reactive
from textual.widgets import Header


class HeadBar(Header):
    """
    Custom Header for showing status
    """

    status: Reactive[str] = Reactive("Input")

    def __init__(self):
        super().__init__(tall=False, style=Style(color="#2277ff", bgcolor="#3b4252"))

    def render(self) -> RenderableType:
        header_table: Table = Table.grid(padding=(1, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=20)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="center", width=10)
        header_table.add_row(
            f"  {self.status}",
            Text("Graia Console", style=Style(bold=True, color="#3fa03f")),
            self.get_clock() if self.clock else "",
        )

        return Panel(header_table, style=self.style) if self.tall else header_table
