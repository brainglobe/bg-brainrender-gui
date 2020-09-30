from qtpy.QtWidgets import QApplication
import sys
from brainrender_gui.app import App
import click

import pyinspect
pyinspect.install_traceback()

def launch(*args, output=None, **kwargs):
    """
        Launches the application
    """
    if output is None:
        screenshot_kwargs = {}
    else:
        screenshot_kwargs = dict(folder=output)

    app = QApplication(sys.argv)
    app.setApplicationName("Brainrender GUIs")
    ex = App(*args, screenshot_kwargs=screenshot_kwargs, **kwargs)
    app.aboutToQuit.connect(ex.onClose)
    ex.show()
    sys.exit(app.exec_())


@click.command()
@click.option("-x", "--axes", is_flag=True, default=False)
@click.option("-a", "--atlas", default=None)
@click.option("-o", "--output", default=None)
def clilaunch(atlas=None, axes=False, output=None):
    if output is None:
        screenshot_kwargs = {}
    else:
        screenshot_kwargs = dict(folder=output)

    app = QApplication(sys.argv)
    app.setApplicationName("Brainrender GUIs")
    ex = App(atlas=atlas, axes=axes, screenshot_kwargs=screenshot_kwargs)
    app.aboutToQuit.connect(ex.onClose)
    ex.show()
    sys.exit(app.exec_())
