from qtpy.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QListWidget,
    QHBoxLayout,
)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from brainrender_gui.style import style


class UI(QMainWindow):
    buttons = {}

    left_navbar_button_names = [
        "add brain regions",
        "add cells",
        "add from file",
        "add sharptrack",
    ]

    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle("BRAINGLOBE - brainrender GUI")

        # set the size of window
        self.Width = 3000
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        self.initUI()

        self.setStyleSheet(style)

    def make_left_navbar(self):
        # make layout
        layout = QVBoxLayout()

        # Add label
        layout.addWidget(QLabel("Add actors"))

        # Add buttons
        for bname in self.left_navbar_button_names:
            btn = QPushButton(bname.capitalize(), self)
            btn.setObjectName(bname.replace(" ", "_"))
            self.buttons[bname.replace(" ", "_")] = btn
            layout.addWidget(btn)

        # set spacing
        layout.addStretch(5)
        layout.setSpacing(20)

        # make widget
        widget = QWidget()
        widget.setObjectName("LeftNavbar")
        widget.setLayout(layout)

        return widget

    def make_right_navbar(self):
        # make layout
        layout = QVBoxLayout()

        # Add label
        layout.addWidget(QLabel("Actors"))

        # add list widget
        self.actors_list = QListWidget()
        self.actors_list.setObjectName("actors_list")
        layout.addWidget(self.actors_list)

        # set spacing
        layout.addStretch(5)
        layout.setSpacing(20)

        # make widget
        widget = QWidget()
        widget.setObjectName("RightNavbar")
        widget.setLayout(layout)

        return widget

    def make_brwidget(self):
        self.vtkWidget = QVTKRenderWindowInteractor(self)

    def initUI(self):
        # Create navbars
        left_navbar = self.make_left_navbar()
        right_navbar = self.make_right_navbar()

        # Create brainrender widget
        self.make_brwidget()

        # Make overall layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_navbar)
        main_layout.addWidget(self.vtkWidget)
        main_layout.addWidget(right_navbar)

        # Make the brwidget wider
        main_layout.setStretch(0, 70)
        main_layout.setStretch(1, 200)
        main_layout.setStretch(2, 70)

        # Create main window widget
        main_widget = QWidget()
        main_widget.setObjectName("MainWidget")
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
