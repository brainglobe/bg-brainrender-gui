from PyQt5.Qt import Qt
import brainrender

from brainrender_gui.widgets.add_regions import AddRegionsWindow
from brainrender_gui.widgets.actors_list import remove_from_list
from brainrender_gui.utils import (
    get_region_actors,
    get_color_from_string,
    get_alpha_from_string,
)


class RegionsControl:
    def __init__(self):
        """
            Collections of functions to control the 
            addition of regions meshes to the brainrender
            Scene for the GUI
        """
        return

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
        if get_region_actors(self.scene.actors, region) is None:
            # Add region
            self.scene.add_brain_regions(region,)
        else:
            # remove regiona and update list
            act = get_region_actors(self.scene.actors, region)
            del act
            del self.actors[region]
            remove_from_list(self.actors_list, region)

        # Update hierarchy's item font
        item.toggle_active()

        # Update brainrender scene
        self._update()
