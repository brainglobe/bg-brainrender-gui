import brainrender
from brainrender.scene import Scene
from brainrender.Utils.camera import set_camera
from vedo import Plotter, addons
from collections import namedtuple
import datetime

from brainrender_gui.ui import UI
from brainrender_gui.apputils.camera_control import CameraControl
from brainrender_gui.apputils.add_from_file_control import AddFromFile
from brainrender_gui.apputils.regions_control import RegionsControl
from brainrender_gui.apputils.actors_control import ActorsControl

from brainrender_gui.widgets.actors_list import update_actors_list
from brainrender_gui.widgets.screenshot_modal import ScreenshotModal


class App(
    Scene, UI, CameraControl, AddFromFile, RegionsControl, ActorsControl
):
    actors = {}  # stores actors and status
    camera_orientation = None  # used to manually set camera orientation

    def __init__(self, *args, atlas=None, axes=None, **kwargs):
        """
            Initialise the pyqt5 app and the brainrender scene. 

            Arguments:
            ----------

            atlas: str/None. Name of the brainglobe atlas to use
            axes: bool. If true axes are shown in the brainrender render
        """
        # Initialize parent classes
        self.scene = Scene(*args, atlas=atlas, **kwargs)
        UI.__init__(self, *args, **kwargs)
        CameraControl.__init__(self)
        AddFromFile.__init__(self)
        RegionsControl.__init__(self)
        ActorsControl.__init__(self)

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

        buttons_funcs = dict(
            add_brain_regions=self.open_regions_dialog,
            add_from_file=self.add_from_file_object,
            add_cells=self.add_from_file_cells,
            add_sharptrack=self.add_from_file_sharptrack,
            show_structures_tree=self.toggle_treeview,
            take_screenshot=self.take_screenshot,
            reset=self.reset_camera,
            top=self.move_camera_top,
            side1=self.move_camera_side1,
            side2=self.move_camera_side2,
            front=self.move_camera_front,
        )

        for btn, fun in buttons_funcs.items():
            self.buttons[btn].clicked.connect(fun)

        self.treeView.clicked.connect(self.add_region_from_tree)

        self.alpha_textbox.textChanged.connect(self.update_actor_properties)
        self.color_textbox.textChanged.connect(self.update_actor_properties)

    def take_screenshot(self):
        actors = self._update()
        self.scene.plotter.render()

        # Get savename
        self.scene.screenshots_folder.mkdir(exist_ok=True)

        savename = str(
            self.scene.screenshots_folder / self.scene.screenshots_name
        )
        savename += (
            f'_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}' + ".png"
        )
        print(f"\nSaving screenshot at {savename}\n")
        self.scene.plotter.screenshot(savename)

        # show success message
        dialog = ScreenshotModal(self, self.palette)
        dialog.exec()

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

        for actor in self.scene.actors:
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
        self.scene.apply_render_style()

        if self.camera_orientation is not None:
            set_camera(self.scene, self.camera_orientation)
            self.camera_orientation = None

        # Get actors to render
        self._update_actors()
        to_render = [act for act in self.actors.values() if act.is_visible]

        # Set actors look
        meshes = [act.mesh.c(act.color).alpha(act.alpha) for act in to_render]

        # Add axes
        if self.axes is not None:
            meshes.append(self.axes)

        # update actors rendered
        self.scene.plotter.show(
            *meshes, interactorStyle=0, bg=brainrender.BACKGROUND_COLOR,
        )

        # Fake a button press to force canvas update
        self.scene.plotter.interactor.MiddleButtonPressEvent()
        self.scene.plotter.interactor.MiddleButtonReleaseEvent()

        # Update list widget
        update_actors_list(self.actors_list, self.actors)

        return meshes

    # ----------------------------------- Close ---------------------------------- #
    def onClose(self):
        """
            Disable the interactor before closing to prevent it from trying to act on a already deleted items
        """
        self.vtkWidget.close()
