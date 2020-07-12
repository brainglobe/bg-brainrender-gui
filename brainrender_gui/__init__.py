from qtpy.QtWidgets import QApplication
import sys
from brainrender_gui.app import App
import click


def launch(*args, **kwargs):
    """
        Launches the application
    """
    app = QApplication(sys.argv)
    ex = App(*args, **kwargs)
    app.aboutToQuit.connect(ex.onClose)
    ex.show()
    sys.exit(app.exec_())


@click.command()
@click.option("-x", "--axes", is_flag=True, default=False)
@click.option("-a", "--atlas", default=None)
def clilaunch(atlas=None, axes=False):
    app = QApplication(sys.argv)
    ex = App(atlas=atlas, axes=axes)
    app.aboutToQuit.connect(ex.onClose)
    ex.show()
    sys.exit(app.exec_())
