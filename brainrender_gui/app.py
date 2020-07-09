import brainrender
from brainrender.scene import Scene
from brainrender.Utils.camera import set_camera
from vedo import Plotter, addons
from collections import namedtuple
from qtpy.QtWidgets import QFileDialog
from qtpy.QtGui import QColor
from PyQt5.Qt import Qt


from brainrender_gui.ui import UI
from brainrender_gui.widgets.actors_list import (
    update_actors_list,
    remove_from_list,
)
from brainrender_gui.widgets.add_regions import Window2
from brainrender_gui.style import palette

"""
    # ! known issues
        when toggling actors, if all are toggled OFF that doesn't work
            at least one actor needs to show at all times
"""


class App(Scene, UI):
    actors = {}  # stores actors and status

    def __init__(
        self, *args, atlas=None, axes=None, random_colors=False, **kwargs
    ):
        self.scene = Scene(*args, atlas=atlas, **kwargs)
        UI.__init__(self, *args, **kwargs)

        # Setup brainrender plotter
        self.axes = axes
        self.atuple = namedtuple("actor", "mesh, is_visible")

        self.setup_plotter()
        self._update()
        self.scene._get_inset()

        # Setup widgets functionality
        self.actors_list.clicked.connect(self.actor_list_clicked)
        self.buttons["add_brain_regions"].clicked.connect(
            self.open_regions_dialog
        )
        self.buttons["add_from_file"].clicked.connect(
            self.add_from_file_object
        )
        self.buttons["add_cells"].clicked.connect(self.add_from_file_cells)
        self.buttons["add_sharptrack"].clicked.connect(
            self.add_from_file_sharptrack
        )

        # Add callback
        self.treeView.clicked.connect(self.add_region_from_tree)

    # ---------------------------- Add/Update regions ---------------------------- #
    def open_regions_dialog(self):
        self.regions_dialog = Window2(self)

    def add_regions(self, regions):
        self.scene.add_brain_regions(regions)
        self._update()

    def add_region_from_tree(self, val):
        """
            When an item on the hierarchy tree is double clicked, the
            corresponding mesh is added/removed from the brainrender scene
        """
        # Get item
        idxs = self.treeView.selectedIndexes()
        if idxs:
            item = idxs[0]
        else:
            return
        item = item.model().itemFromIndex(val)

        # Get region name
        region = item.tag

        # Toggle checkbox
        if not item._checked:
            item.setCheckState(Qt.Checked)
            item._checked = True
        else:
            item.setCheckState(Qt.Unchecked)
            item._checked = False

        # Add/remove mesh
        if region not in self.scene.actors["regions"].keys():
            # Add region
            self.scene.add_brain_regions(region,)
        else:
            # remove regiona and update list
            del self.scene.actors["regions"][region]
            del self.actors[region]
            remove_from_list(self.actors_list, region)

        # Update hierarchy's item font
        item.toggle_active()

        # Update brainrender scene
        self._update()

    # ------------------------------- Add from file ------------------------------ #

    def open_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        fname, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*)",
            options=options,
        )
        return fname

    def add_from_file(self, fun):
        fname = self.open_file()
        if not fname:
            return
        else:
            fun(fname)
            self._update()

    def add_from_file_object(self):
        self.add_from_file(self.scene.add_from_file)

    def add_from_file_sharptrack(self):
        self.add_from_file(self.scene.add_probe_from_sharptrack)

    def add_from_file_cells(self):
        self.add_from_file(self.scene.add_cells_from_file)

    # -------------------------------- Actors list ------------------------------- #
    def actor_list_clicked(self, index):
        """
            When an item in the actors list is clicked
            it toggles the corresponding actor's visibility
        """
        # Get actor
        aname = self.actors_list.currentItem().text()
        if aname not in self.actors.keys():
            raise ValueError(f"Actor {aname} not in the actors record")
        else:
            actor = self.actors[aname]

        # Toggle visibility
        self.actors[aname] = self.atuple(actor.mesh, not actor.is_visible)

        # Toggle list item UI
        if self.actors[aname].is_visible:
            txt = palette["text"]
        else:
            txt = palette["primary"]
        rgb = txt.replace(")", "").replace(" ", "").split("(")[-1].split(",")
        self.actors_list.item(index.row()).setForeground(
            QColor(*[int(r) for r in rgb])
        )

        # uPDATE
        self._update()

    # ------------------------------- Initial setup ------------------------------ #
    def setup_plotter(self):
        """
            Changes the scene's default plotter
            with one attached to the qtWidget in the 
            pyqt application. 
        """
        # Get embedded plotter
        new_plotter = Plotter(qtWidget=self.vtkWidget)
        self.scene.plotter = new_plotter

        # Get axes
        if self.axes:
            ax = addons.buildAxes(
                self.scene.root,
                xtitle="x [um]",
                xLabelOffset=0.07,
                xTitleOffset=0.1,
                xTitleJustify="bottom-left",
                ytitle="y [um]",
                yLabelOffset=0.025,
                yTitleOffset=0.1,
                yTitleJustify="bottom-left",
                ztitle="z [um]",
                zLabelOffset=0.025,
                zTitleOffset=0.1,
                zTitleJustify="bottom-left",
            )
            for a in ax.unpack():
                if "xtitle" in a.name or "xNumericLabel" in a.name:
                    a.RotateZ(180)

            self.scene.add_actor(ax)

        # Fix camera
        set_camera(self.scene, self.scene.camera)

    # ---------------------------------- Update ---------------------------------- #
    def _update_actors(self):
        """
            All actors that are part of the scene are stored
            in a dictionary with key as the actor name and 
            value as a 2-tuple with (Mesh, is_visible). 
            `is_visible` is a bool that determines if the 
            actor should be rendered
        """

        for actor in self.scene.get_actors():
            if actor is None:
                continue
            if actor.name not in self.actors.keys():
                self.actors[actor.name] = self.atuple(actor, True)

    def _update(self):
        """
            Updates the scene's Plotter to add/remove
            meshes
        """
        # Get actors to render
        self._update_actors()
        to_render = [at.mesh for at in self.actors.values() if at.is_visible]

        # Make sure root toggles correctly
        if "root" not in [a.name for a in to_render]:
            self.scene.root = None
        elif self.scene.root is None:
            self.scene.add_root()

        # update actors rendered
        self.scene.apply_render_style()
        self.scene.plotter.show(
            *to_render, interactorStyle=0, bg=brainrender.BACKGROUND_COLOR,
        )

        # Fake a button press to force canvas update
        self.scene.plotter.interactor.MiddleButtonPressEvent()
        self.scene.plotter.interactor.MiddleButtonReleaseEvent()

        # Update list widget
        update_actors_list(self.actors_list, self.actors)

    # ----------------------------------- Close ---------------------------------- #
    def onClose(self):
        """
            Disable the interactor before closing to prevent it from trying to act on a already deleted items
        """
        self.vtkWidget.close()
