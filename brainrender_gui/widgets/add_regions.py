from qtpy.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel


class Window2(QDialog):
    left = 250
    top = 250
    width = 800
    height = 300

    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Add brain regions")
        self.ui()
        self.main_window = main_window

    def ui(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label = QLabel(
            "Write the acronyms of brainregions"
            + "you wish to add as comma separated string (e.g.: STN, TH)"
        )

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.button = QPushButton("Add regions", self)
        self.button.move(20, 80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        regions = self.textbox.text().split(", ")
        self.main_window.add_regions(regions)

        self.close()
