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
}}
QWidget#RightNavbar {{
    background-color: {palette['background']};
}}
QWidget#MainWidget {{
    background-color: {palette['background']};
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
    margin: 12px 24;
}}


QListWidget#actors_list {{
    background-color: {palette['foreground']};
    color: {palette['text']};
    border-radius: 8px;
    padding: 6px;
    font-size: 14pt;
    margin: 4px 34px;
}}

"""
