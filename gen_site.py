from dataclasses import dataclass, field
from typing import ClassVar

import jinja2

with open("template/index.html") as template_file:
    template = jinja2.Template(template_file.read())


@dataclass()
class Item:
    type: ClassVar[str]


@dataclass()
class Header(Item):
    type = "Header"

    header: str
    anchor: str = field(default=None)

    def __post_init__(self):
        if self.anchor is None:
            self.anchor = self.header


@dataclass()
class Image(Item):
    type = "Image"

    image: str
    alt: str
    caption: str


@dataclass()
class Text(Item):
    type = "Text"

    text: str


def main(items):
    file = template.render(items=items)
    with open("index.html", "w") as index:
        index.write(file)
        print("written")


main([
    Header("Overview"),
    Text("Aize is a programming language designed by a programmer, for programmers. "
         "It's design philsohpy can be summed up in 2 words: fast, simple."),
    Text("""Link <a href="template/index.html">Link</a>"""),
])
