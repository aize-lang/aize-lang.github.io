import pathlib
from dataclasses import dataclass, field
from typing import ClassVar, List

import jinja2

with open("_templates/index_template.html") as template_file:
    template = jinja2.Template(template_file.read())


@dataclass()
class Item:
    type: ClassVar[str]

    def render(self) -> str:
        raise NotImplementedError()


@dataclass()
class Header(Item):
    type = "Header"

    header: str
    anchor: str = field(default=None)
    level: int = field(default=0)

    def __post_init__(self):
        if self.anchor is None:
            self.anchor = self.header

    def render(self) -> str:
        assert 0 <= self.level <= 1
        return f"""<a id="{self.anchor}" class="jump-target"></a>
                <p class="header{self.level}">{self.header}</p>"""


@dataclass()
class Image(Item):
    type = "Image"

    image: str
    alt: str
    caption: str

    def render(self) -> str:
        return f"""<div class="img-box">
                    <img src="{self.image}" alt="{self.alt}">
                    <p>{self.caption}</p>
                </div>"""


@dataclass()
class Text(Item):
    type = "Text"

    text: str

    def render(self) -> str:
        return f"""<p class="text">{self.text}</p>"""


@dataclass()
class UnorderedList(Item):
    type = "UnorderedList"

    text: str
    items: List[Item]

    def render(self) -> str:
        return f"""{self.text}<ul class="content-list">{''.join(
            '<li>'+item.render()+'</li>' for item in self.items)
        }</ul>"""


@dataclass()
class OrderedList(Item):
    type = "OrderedList"

    text: str
    items: List[Item]

    def render(self) -> str:
        return f"""{self.text}<ol class="content-list">{''.join(
            '<li>'+item.render()+'</li>' for item in self.items)
        }</ol>"""


@dataclass()
class Stacked(Item):
    type = "Stacked"

    items: List[Item]

    def render(self) -> str:
        return f"""{''.join(item.render() for item in self.items)}"""


@dataclass()
class CodeBlock(Item):
    type = "CodeBlock"

    code: str

    def render(self) -> str:
        # return f"""<div class="code-block">{''.join('<p><code>'+line+'</code></p>' for line in self.code.splitlines())}</div>"""
        return f"""<div class="code-block"><pre><code>{self.code}</code></pre></div>"""


def main(items):
    file = template.render(items=items)
    curr_dir = pathlib.Path(__file__).absolute()
    with (curr_dir.parent.parent / "index.html").open("w") as index:
        index.write(file)
        print("written")


main([
    CodeBlock("""\
def fibo(n: int) -> int {
    if (n < 2) {
        return n;
    } else {
        return fibo(n-1) + fibo(n-2);
    }
}
"""),
    Header("Overview"),
    Text("Aize is a programming language designed by a programmer, for programmers. "
         "It's design philosophy can be summed up in 2 words:"),
    UnorderedList("", [
        Text("Fast  -  Aize must be a fast language."),
        Text("Simple  -  Aize must be a simple language to learn for experienced programmers, and relatively easy for beginners."),
    ]),
    Header("Getting Started"),
    OrderedList("", [
        UnorderedList("Requirements", [
            Text("Python 3.7+"),
            UnorderedList("A C Compiler", [
                Text("MinGW on Windows. It must be on your path, in Program Files, or your user folder."),
                Text("GCC or Clang on Linux. At least one must be on your path.")
            ])
        ]),
        Text("Goto the Github Repository and download and unzip aize-lang onto your computer somewhere."),
        Text("Goto into the `/aizelang` folder."),
        Stacked([Text("Assuming the correct Python is on the path, type into the command prompt for Windows:"),
                 CodeBlock("python -m aizec test/fibo.aize --run")]),
        Text("You should see the first 20 fibonacci numbers printed."),
        Text("For Linux, do Step 4 within the terminal instead."),
    ]),

    Header("Links"),
    Header("Github", level=1),
    UnorderedList("", [
        Text("<a href='https://github.com/aize-lang/aize-lang'>aize-lang</a>: The compiler repository."),
        Text("<a href='https://github.com/aize-lang/aize-lang'>aize-lang.github.io</a>: This website's repository."),
    ]),
])
