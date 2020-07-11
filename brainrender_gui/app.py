import brainrender
from brainrender.scene import Scene
from brainrender.Utils.camera import set_camera
from vedo import Plotter, addons
from collections import namedtuple
from qtpy.QtWidgets import QFileDialog
from qtpy.QtGui import QColor
from PyQt5.Qt import Qt
import numpy as np

from brainrender_gui.ui import UI
from brainrender_gui.widgets.actors_list import (
    update_actors_list,
    remove_from_list,
)
from brainrender_gui.widgets.add_regions import AddRegionsWindow
from brainrender_gui.style import palette


class App(Scene, UI):
    actors = {}  # stores actors and status

    def __init__(
        self, *args, atlas=None, axes=None, random_colors=False, **kwargs
    ):
        self.scene = Scene(*args, atlas=atlas, **kwargs)
        UI.__init__(self, *args, **kwargs)

        # Setup brainrender plotter
        self.axes = axes
        self.atuple = namedtuple("actor", "mesh, is_visible, color, alpha")

        self.setup_plotter()
        self._update()
        self.scene._get_inset()

        # Setup widgets functionality
        self.actors_list.itemDoubleClicked.connect(self.actor_list_double_clicked)
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

        
        self.treeView.clicked.connect(self.add_region_from_tree)

        self.alpha_textbox.textChanged.connect(self.update_actor_properties)
        self.color_textbox.textChanged.connect(self.update_actor_properties)

    # ---------------------------- Update actor props ---------------------------- #
    def update_actor_properties(self):
        # Get currently selected actor
        aname = self.actors_list.currentItem().text()
        if aname not in self.actors.keys():
            raise ValueError(f"Actor {aname} not in the actors record")
        else:
            actor = self.actors[aname]

        # Get color
        if not self.color_textbox.text(): return
        try:
            rgb = self.color_textbox.text()
            rgb = rgb.replace('[', '').replace(']', '')
            color = np.array([float(c) for c in rgb.split(' ')])
        except:
            color = self.color_textbox.text()

        # Get alpha
        try:
            alpha = float(self.alpha_textbox.text())
        except ValueError:
            return

        # Update actor

        try:
            self.actors[aname] = self.atuple(
                                    actor.mesh,
                                    actor.is_visible,
                                    color,
                                    alpha
                                    )
            self._update()
        except IndexError:  # likely something went wrong with getting of color
            self.actors[aname] = actor
            return

    # ---------------------------- Add/Update regions ---------------------------- #
    def open_regions_dialog(self):
        self.regions_dialog = AddRegionsWindow(self, self.palette)

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
    def actor_list_double_clicked(self, listitem):
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
        self.actors[aname] = self.atuple(actor.mesh, not actor.is_visible, actor.color, actor.alpha)

        # Toggle list item UI
        if self.actors[aname].is_visible:
            txt = palette["text"]
        else:
            txt = palette["primary"]
        rgb = txt.replace(")", "").replace(" ", "").split("(")[-1].split(",")

        listitem.setForeground(
            QColor(*[int(r) for r in rgb])
        )

        # update
        self._update()

    def actor_list_clicked(self, index):
        # Get actor
        aname = self.actors_list.currentItem().text()
        if aname not in self.actors.keys():
            raise ValueError(f"Actor {aname} not in the actors record")
        else:
            actor = self.actors[aname]

        self.alpha_textbox.setText(str(actor.alpha))
        self.color_textbox.setText(str(actor.color))


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
                self.actors[actor.name] = self.atuple(actor, True, actor.color(), actor.alpha())

    def _update(self):
        """
            Updates the scene's Plotter to add/remove
            meshes
        """
        # Get actors to render
        self._update_actors()
        to_render = [act for act in self.actors.values() if act.is_visible]

        # Set actors look
        meshes = [act.mesh.c(act.color).alpha(act.alpha) for act in to_render]
        

        # update actors rendered
        self.scene.apply_render_style() 
        self.scene.plotter.show(
            *meshes, 
            interactorStyle=0, bg=brainrender.BACKGROUND_COLOR,
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
