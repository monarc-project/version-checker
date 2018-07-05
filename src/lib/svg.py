
from bootstrap import application
import svgwrite

STYLE = {
                "up-to-date": {
                                "rect_size": (95, 20),
                                "rect_fill": "green",
                                "paragraph_fill": "white",
                                "text_fill": "white",
                            },
                "update available": {
                                "rect_size": (140, 20),
                                "rect_fill": "orange",
                                "paragraph_fill": "white",
                                "text_fill": "white",
                            },
                "security update available": {
                                "rect_size": (210, 20),
                                "rect_fill": "red",
                                "paragraph_fill": "white",
                                "text_fill": "white",
                            },
            }


def simple_text(name, text, style):
    """Draw a text in a rectangle."""
    dwg = svgwrite.Drawing(name, style["rect_size"])

    rect = dwg.rect(insert=(0, 0), size=style["rect_size"], fill=style["rect_fill"])
    dwg.add(rect)

    paragraph = dwg.add(dwg.g(font_size=14, font_family="DejaVu Sans", fill=style["paragraph_fill"]))

    text = dwg.text(text, insert=(5, 15), font_weight='bold', fill=style["text_fill"])

    paragraph.add(text)

    #return dwg
    file_name = "{}.svg".format(name.replace(' ', '-'))
    file_path = application.config['UPLOAD_FOLDER'] + file_name

    dwg.saveas(file_path)
    return file_name



if __name__ == '__main__':
    for state in ["up-to-date", "update available",
                  "security update available"]:
        simple_text("{}.svg".format(state.replace(' ', '-')), state,
                    STYLE[state])
