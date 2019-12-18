from dataclasses import dataclass, field
from typing import ClassVar

import jinja2

template = jinja2.Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aize-lang</title>
      <link rel="stylesheet" href="style.css">
    <link rel="icon" type="images/png" href="images/logo50x50.png">
</head>
<body>
    <div class="side-bar">
        <img src="images/logo.svg" alt="aize logo">
        <div class="side-bar-title">
            Navigation
        </div>
        <div class="side-bar-links">
            <a href="#title" class="side-bar-link"><p>Aize</p></a>
            {% for item in items %}
                {% if item.type == "Header" %}
                    <a href="#{{ item.anchor }}" class="side-bar-link"><p>{{ item.header }}</p></a>
                {% endif %}
            {% endfor %}
        </div>
    </div>
    <div class="top-bar">
        <p class="top-bar-title">The Aize Programming Language</p>
    </div>
    <div class="title-bar">
        <a id="title"></a>
        <div class="title-container">
            <div class="title">
                Aize
            </div>
            <div class="title-blurb">
                The Future of Programming
            </div>
        </div>
    </div>
    <div class="content">
        {% for item in items %}
            {% if item.type == "Text" %}
                <p class="text">{{ item.text }}</p>
            {% elif item.type == "Image" %}
                <div class="img-box">
                    <img src="{{ item.image }}" alt="{{ item.alt }}">
                    <p>{{ item.caption }}</p>
                </div>
            {% elif item.type == "Header" %}
                <a id="{{ item.anchor }}"></a>
                <p class="header">{{ item.header }}</p>
            {% endif %}
        {% endfor %}
    </div>
</body>
</html>
""")


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


main([
    Header("Overview"),
    Image("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
          "Google Logo", "The Google Logo"),
    Text("Aize a programming language that aims to be fast and simple."),
    Image("https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
          "Google Logo", "The Google Logo"),
])
