from qtpy.QtWidgets import QApplication
import sys
from brainrender_gui.app import App


def launch():
    """
        Launches the application
    """
    app = QApplication(sys.argv)
    ex = App()
    app.aboutToQuit.connect(ex.onClose)
    ex.show()
    sys.exit(app.exec_())


# button.clicked.connect(say_hello)
