from typing import Self, override

from ludic.attrs import Attrs
from ludic.catalog.buttons import ButtonDanger, ButtonSuccess
from ludic.catalog.headers import H1, H2
from ludic.catalog.layouts import Box, Cluster
from ludic.catalog.lists import Item, List
from ludic.catalog.messages import MessageWarning, Title
from ludic.catalog.typography import Code, CodeBlock, Link, Paragraph
from ludic.html import b
from ludic.web import Endpoint, Request

from web.components import LogoBig
from web.pages import Page


def index(request: Request) -> Page:
    return Page(
        LogoBig(logo_url=request.url_for("static", path="ludic.png")),
        H1("Introduction"),
        Paragraph(
            "Ludic is a lightweight framework for building HTML pages with a component "
            f"approach similar to {Link("React", to="https://react.dev/")}. It is "
            f"built to be used together with {Link(
                "htmx.org", to="https://htmx.org/")} so that developers don't need "
            "to write almost any JavaScript to create dynamic web services. Its "
            "potential can be leveraged together with its web framework which is a "
            f"wrapper around the powerful {Link(
                "Starlette", to="https://www.starlette.io/")} framework. It is built "
            "with the latest Python 3.12 features heavily incorporating typing."
        ),
        MessageWarning(
            Title("Experimental"),
            "The framework is in a very early development/experimental stage. There "
            "are a lot of half-functioning features at the moment. Contributions are "
            "welcome to help out with the progress!",
        ),
        H2("Features"),
        List(
            Item(
                f"Seamless {b("</> htmx")} integration for rapid web development "
                f"in {b("pure Python")}"
            ),
            Item(f"{b("Type-Guided components")} utilizing Python's typing system"),
            Item(
                f"Uses the power of {b("Starlette")} and {b("Async")} for "
                "high-performance web development"
            ),
            Item(f"Build HTML with the ease and power of Python {b('f-strings')}"),
            Item(f"Add CSS styling to your components with {b("Themes")}"),
            Item(
                "Create simple, responsive layouts adopted from the "
                f"{b("Every Layout Book")}"
            ),
        ),
        H2("Quick Example"),
        Paragraph(
            "Here is a simple re-implementation of an example from "
            f"{Link("Reflex", to=(
                "https://reflex.dev/docs/getting-started/introduction/"
                "#an-example:-make-it-count")
            )}:"
        ),
        Box(Counter(value=0)),
        Paragraph("The counter can be included on any page like here:"),
        CodeBlock(
            """
            from typing import override

            from ludic.html import b, div
            from ludic.web import Endpoint, LudicApp, Request
            from ludic.catalog.buttons import ButtonDanger, ButtonSuccess
            from ludic.catalog.layouts import Box

            app = LudicApp()

            @app.get("/")
            def index(request: Request) -> Box:
                return Box(Counter("0"))
            """,
            language="python",
        ),
        Paragraph(
            f"Note that the {Code("Box")} is just a component wrapping the buttons "
            f"and the number to make it nicely framed. You can read more about the "
            f"{Code("Box")} in the {b(Link("Layouts", to=(
                request.url_for("catalog:layouts").path))
            )} section later. Anyway, the {Code("Counter")} component is the part "
            "that is more interesting: "
        ),
        CodeBlock(
            """
            @app.get("/counter/{value}")
            def Counter(value: str) -> div:
                return div(
                    ButtonDanger(
                        "Decrement",
                        hx_get=app.url_path_for("Counter", value=int(value) - 1),
                        hx_target="#counter",
                    ),
                    b(value, style={"font-size": "2em"}),
                    ButtonSuccess(
                        "Increment",
                        hx_get=app.url_path_for("Counter", value=int(value) + 1),
                        hx_target="#counter",
                    ),
                    id="counter",
                )
            """,
            language="python",
        ),
        H2("Requirements"),
        Paragraph("Python 3.12+"),
        H2("Installation"),
        CodeBlock('pip install "ludic[full]"'),
        Paragraph(
            "As similar for Starlette, you'll also want to install an "
            f"{Link("ASGI", to="https://asgi.readthedocs.io/en/latest/")} server:"
        ),
        CodeBlock("pip install uvicorn"),
        H2("Contributing"),
        Paragraph(
            "Any contributions to the framework are warmly welcome! Your help will "
            "make it a better resource for the community. If you're ready to "
            "contribute, read the ",
            Link(
                "contribution guide on GitHub",
                to="https://github.com/paveldedik/ludic/blob/main/CONTRIBUTING.md",
            ),
            ".",
        ),
        request=request,
        active_item="docs:index",
    )


class CounterAttrs(Attrs):
    value: int


class Counter(Endpoint[CounterAttrs]):
    @classmethod
    def get(cls, value: str) -> Self:
        return cls(value=int(value))

    @override
    def render(self) -> Cluster:
        return Cluster(
            ButtonDanger(
                "Decrement",
                hx_get=self.url_for("docs:Counter", value=self.attrs["value"] - 1),
                hx_target="#counter",
            ),
            b(
                self.attrs["value"],
                style={"font-size": self.theme.fonts.size * 2},
            ),
            ButtonSuccess(
                "Increment",
                hx_get=self.url_for("docs:Counter", value=self.attrs["value"] + 1),
                hx_target="#counter",
            ),
            id="counter",
            classes=["centered"],
        )