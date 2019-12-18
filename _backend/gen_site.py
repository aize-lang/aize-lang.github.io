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

    def __post_init__(self):
        if self.anchor is None:
            self.anchor = self.header

    def render(self) -> str:
        return f"""<a id="{self.anchor}"></a>
                <p class="header">{self.header}</p>"""


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


def main(items):
    file = template.render(items=items)
    curr_dir = pathlib.Path(__file__).absolute()
    with (curr_dir.parent.parent / "index.html").open("w") as index:
        index.write(file)
        print("written")


main([
    Header("Overview"),
    Text("Aize is a programming language designed by a programmer, for programmers. "
         "It's design philosophy can be summed up in 2 words:"),
    UnorderedList("", [
        Text("Fast  -  Aize must be a fast language."),
        Text("Simple  -  Aize must be a simple language to learn for experienced programmers, and relatively easy for beginners."),
    ]),
    Header("Getting Started"),
    OrderedList("", [
        Text("Goto the Github Repository"),
    ])
])
