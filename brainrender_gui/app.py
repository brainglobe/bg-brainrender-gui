import brainrender
from brainrender.scene import Scene
from brainrender.Utils.camera import set_camera
from vedo import Plotter, addons
from collections import namedtuple
from qtpy.QtWidgets import QFileDialog
from qtpy.QtGui import QColor, QIcon
from PyQt5.Qt import Qt
import numpy as np

from brainrender_gui.ui import UI
from brainrender_gui.widgets.actors_list import (
    update_actors_list,
    remove_from_list,
)
from brainrender_gui.widgets.add_regions import AddRegionsWindow
from brainrender_gui.style import palette
from brainrender_gui.utils import get_color_from_string, get_alpha_from_string


class App(Scene, UI):
    actors = {}  # stores actors and status

    def __init__(self, *args, atlas=None, axes=None, **kwargs):
        """
            Initialise the pyqt5 app and the brainrender scene. 

            Arguments:
            ----------

            atlas: str/None. Name of the brainglobe atlas to use
            axes: bool. If true axes are shown in the brainrender render
        """
        self.scene = Scene(*args, atlas=atlas, **kwargs)
        UI.__init__(self, *args, **kwargs)

        # Setup brainrender plotter
        self.axes = axes
        self.atuple = namedtuple("actor", "mesh, is_visible, color, alpha")

        self.setup_plotter()
        self._update()
        self.scene._get_inset()

        # Setup widgets functionality
        self.actors_list.itemDoubleClicked.connect(
            self.actor_list_double_clicked
        )
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
        self.buttons["show_structures_tree"].clicked.connect(
            self.toggle_treeview
        )

        self.treeView.clicked.connect(self.add_region_from_tree)

        self.alpha_textbox.textChanged.connect(self.update_actor_properties)
        self.color_textbox.textChanged.connect(self.update_actor_properties)

    # ------------------------------ Toggle treeview ----------------------------- #
    def toggle_treeview(self):
        """
            Method for the show structures tree button.
            It toggles the visibility of treeView widget
            and adjusts the button's text accordingly.
        """
        if not self.treeView.isHidden():
            self.buttons["show_structures_tree"].setText(
                "Show structures tree"
            )
        else:
            self.buttons["show_structures_tree"].setText(
                "Hide structures tree"
            )

        self.treeView.setHidden(not self.treeView.isHidden())

    # ---------------------------- Update actor props ---------------------------- #
    def update_actor_properties(self):
        """
            Called when the text boxes for showing/editing
            the selected actor's alpha/color are edited.
            This function checks that the values makes sense
            and update the atuple of the selected actor.
        """
        # Get currently selected actor
        aname = self.actors_list.currentItem().text()
        if aname not in self.actors.keys():
            raise ValueError(f"Actor {aname} not in the actors record")
        else:
            actor = self.actors[aname]

        # Get color
        if not self.color_textbox.text():
            return
        color = get_color_from_string(self.color_textbox.text())

        # Get alpha
        alpha = get_alpha_from_string(self.alpha_textbox.text())
        if alpha is None:
            return

        # Update actor
        try:
            self.actors[aname] = self.atuple(
                actor.mesh, actor.is_visible, color, alpha
            )
            self._update()
        except IndexError:  # likely something went wrong with getting of color
            self.actors[aname] = actor
            return

    # ---------------------------- Add/Update regions ---------------------------- #
    def open_regions_dialog(self):
        """
            Opens a QDialog window for inputting 
            regions to add to the scene
        """
        self.regions_dialog = AddRegionsWindow(self, self.palette)

    def add_regions(self, regions, alpha, color):
        """
            Called by AddRegionsWindow when it closes.
            It adds brain regions to the scene

            Arguments:
            ----------
            regions: list of strings with regions acronyms
            alpha: str, meshes transparency
            color: str, meshes color. If 'atlas' the default colors are used
        """
        # Get params
        alpha = get_alpha_from_string(alpha)
        if alpha is None:
            alpha = brainrender.DEFAULT_MESH_ALPHA

        color = get_color_from_string(color)
        if color == "atlas":
            use_original = True
            colors = None
        else:
            use_original = False
            colors = color

        # Add brain regions
        self.scene.add_brain_regions(
            regions,
            alpha=alpha,
            use_original_color=use_original,
            colors=colors,
        )

        # Toggle treview entries
        # TODO update treeview item corresponding to regions

        # update
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

    def add_from_file(self, fun):
        """
            General function for selecting, loading
            and adding to scene a file.

            Arguments:
            -----------

            fun: function. One of Scene's methods used to add the file's
                    content to the scene.
        """
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog

        fname, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            "All Files (*)",
            options=options,
        )

        if not fname:
            return
        else:
            fun(fname)
            self._update()

    def add_from_file_object(self):
        """
            Add to scene from .stl, .obj and .vtk files.
            Method of the corresponding button
        """
        self.add_from_file(self.scene.add_from_file)

    def add_from_file_sharptrack(self):
        """
            Add to scene from .m file with SHARPTRACK output
            Method of the corresponding button
        """
        self.add_from_file(self.scene.add_probe_from_sharptrack)

    def add_from_file_cells(self):
        """
            Add to scene from .h5 and .csv files with cell coordinates data.
            Method of the corresponding button
        """
        self.add_from_file(self.scene.add_cells_from_file)

    # -------------------------------- Actors list ------------------------------- #
    def actor_list_double_clicked(self, listitem):
        """
            When an item in the actors list is doube clicked
            it toggles the corresponding actor's visibility
            and updates the list widget UI
        """
        # Get actor
        aname = self.actors_list.currentItem().text()
        if aname not in self.actors.keys():
            raise ValueError(f"Actor {aname} not in the actors record")
        else:
            actor = self.actors[aname]

        # Toggle visibility
        self.actors[aname] = self.atuple(
            actor.mesh, not actor.is_visible, actor.color, actor.alpha
        )

        # Toggle list item UI
        if self.actors[aname].is_visible:
            txt = palette["text"]
            icon = QIcon("brainrender_gui/icons/eye.svg")
        else:
            txt = palette["primary"]
            icon = QIcon("brainrender_gui/icons/eye-slash.svg")
        rgb = txt.replace(")", "").replace(" ", "").split("(")[-1].split(",")

        listitem.setForeground(QColor(*[int(r) for r in rgb]))
        listitem.setIcon(icon)

        # update
        self._update()

    def actor_list_clicked(self, index):
        """
            When an item of the actors list is clicked
            this function loads it's parameters and updates
            the text in the alpha/color textboxes. 
        """
        # Get actor
        aname = self.actors_list.currentItem().text()
        if aname not in self.actors.keys():
            raise ValueError(f"Actor {aname} not in the actors record")
        else:
            actor = self.actors[aname]

        self.alpha_textbox.setText(str(actor.alpha))

        if isinstance(actor.color, np.ndarray):
            color = "".join([str(c) + " " for c in actor.color]).rstrip()
        else:
            color = actor.color

        self.color_textbox.setText(color)

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

            self.axes = ax
            self.scene.add_actor(ax)
        else:
            self.axes = None

        # Fix camera
        set_camera(self.scene, self.scene.camera)

    # ---------------------------------- Update ---------------------------------- #
    def _update_actors(self):
        """
            All actors that are part of the scene are stored
            in a dictionary with key as the actor name and 
            value as a 4-tuple with (Mesh, is_visible, color, alpha). 
            `is_visible` is a bool that determines if the 
            actor should be rendered
        """

        for actor in self.scene.get_actors():
            if actor is None:
                continue

            try:
                if actor.name not in self.actors.keys():
                    self.actors[actor.name] = self.atuple(
                        actor, True, actor.color(), actor.alpha()
                    )
            except AttributeError:
                # the Assembly object representing the axes should be ignore
                pass

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

        # Add axes
        if self.axes is not None:
            meshes.append(self.axes)

        # update actors rendered
        self.scene.apply_render_style()
        self.scene.plotter.show(
            *meshes, interactorStyle=0, bg=brainrender.BACKGROUND_COLOR,
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
