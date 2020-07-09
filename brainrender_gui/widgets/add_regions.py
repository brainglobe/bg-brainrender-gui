from qtpy.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout
from brainrender_gui.style import style


class Window2(QDialog):
    left = 250
    top = 250
    width = 800
    height = 300

    label_msg = (
        "Write the acronyms of brainregions  "
        + "you wish to add.\n[as 'space' separated strings (e.g.: STN TH)]"
    )

    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("Add brain regions")
        self.ui()
        self.main_window = main_window
        self.setStyleSheet(style)

    def ui(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()

        label = QLabel(self)
        label.setObjectName("PopupLabel")
        label.setText(self.label_msg)

        # Create textbox
        self.textbox = QLineEdit(self)

        # Create a button in the window
        self.button = QPushButton("Add regions", self)
        self.button.clicked.connect(self.on_click)
        self.button.setObjectName("RegionsButton")

        layout.addWidget(label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.show()

    def on_click(self):
        regions = self.textbox.text().split(" ")
        self.main_window.add_regions(regions)

        self.close()
