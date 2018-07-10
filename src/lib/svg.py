
from bootstrap import application
import svgwrite

STYLE = {
    "up-to-date": {
                    "text": "up-to-date",
                    "rect_size": (95, 20),
                    "rect_fill": "green",
                    "paragraph_fill": "white",
                    "text_fill": "white",
                },
    "update-available": {
                    "text": "update available",
                    "rect_size": (140, 20),
                    "rect_fill": "orange",
                    "paragraph_fill": "white",
                    "text_fill": "white",
                },
    "security-update-available": {
                    "text": "security update available",
                    "rect_size": (360, 20),
                    "rect_fill": "red",
                    "paragraph_fill": "white",
                    "text_fill": "white",
                },
    "unknown": {
                    "text": "unknown",
                    "rect_size": (95, 20),
                    "rect_fill": "grey",
                    "paragraph_fill": "white",
                    "text_fill": "white",
                },
}


def simple_text(name, style, text=None):
    """Draw a text in a rectangle."""
    dwg = svgwrite.Drawing(name, style["rect_size"])

    rect = dwg.rect(insert=(0, 0), size=style["rect_size"],
                    fill=style["rect_fill"])
    dwg.add(rect)

    paragraph = dwg.add(dwg.g(font_size=14, font_family="DejaVu Sans",
                        fill=style["paragraph_fill"]))
    if not text:
        text = style["text"]
    text_elem = dwg.text(text, insert=(5, 15), font_weight='bold',
                        fill=style["text_fill"])
    paragraph.add(text_elem)

    file_name = "{}.svg".format(name.replace(' ', '-'))
    file_path = application.config['GENERATED_SVG_FOLDER'] + file_name

    dwg.saveas(file_path)
    return file_name


if __name__ == '__main__':
    for state in ["up-to-date", "update available",
                  "security update available"]:
        simple_text("{}.svg".format(state.replace(' ', '-')), state,
                    STYLE[state])
