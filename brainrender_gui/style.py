palette = {  # from napari.utils.theme
    "folder": "dark",
    "background": "rgb(38, 41, 48)",
    "foreground": "rgb(65, 72, 81)",
    "primary": "rgb(90, 98, 108)",
    "secondary": "rgb(134, 142, 147)",
    "highlight": "rgb(106, 115, 128)",
    "text": "rgb(240, 241, 242)",
    "icon": "rgb(209, 210, 212)",
    "warning": "rgb(153, 18, 31)",
    "current": "rgb(0, 122, 204)",
    "syntax_style": "native",
    "console": "rgb(0, 0, 0)",
    "canvas": "black",
}

style = f"""
QWidget#LeftNavbar {{
    background-color: {palette['background']};
    border: 2px solid {palette['text']};
    border-radius: 24px;
    margin: 12px 12px;
    padding: 24px 12px;
}}
QWidget#RightNavbar {{
    background-color: {palette['background']};
    border: 2px solid {palette['text']};
    border-radius: 24px;
    margin: 12px 12px;
    padding: 24px 12px;
}}
QWidget#MainWidget {{
    background-color: {palette['background']};
    padding: 48px;
}}



QPushButton {{ 
    background-color: {palette['foreground']};
    color: {palette['text']};
    border-radius: 8px;
    padding: 6px;
    font-size: 14pt;
    margin: 4px 34px;

}}
QPushButton:hover {{
    border: 1px solid {palette['text']};
}}



QLabel {{
    color: {palette['text']};
    font-size: 16pt;
    font-weight: 700;
    margin: 12px 24px;
}}
QLabel#PopupLabel {{
    color: {palette['text']};
    font-size: 12pt;
    font-weight: 400;
    margin: 12px 24px;
}}


QListWidget#actors_list {{
    background-color: {palette['foreground']};
    color: {palette['text']};
    border-radius: 8px;
    padding: 6px;
    font-size: 14pt;
    margin: 4px 34px;
}}

QLineEdit {{
    background-color: {palette['foreground']};
    color: {palette['text']};
    border-radius: 8px;
    padding: 6px;
    font-size: 12pt;
    height: 48px;
    min-width: 600px;
    margin: 4px 34px;
    width: 80%
}}
QDialog {{
    background-color: {palette['background']};
}}
QPushButton#RegionsButton {{
    width: 80%;
}}

"""
