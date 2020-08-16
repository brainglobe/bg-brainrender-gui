import numpy as np
from brainrender_gui.utils import (
    get_color_from_string,
    get_alpha_from_string,
)
from brainrender_gui.style import palette
from qtpy.QtGui import QColor, QIcon
from pkg_resources import resource_filename


class ActorsControl:
    def __init__(self):
        """
            Collection of functions to control actors properties 
            and related widget in the GUI
        """
        return

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
            icon = QIcon(resource_filename("brainrender_gui", "icons/eye.svg"))
        else:
            txt = palette["primary"]
            icon = QIcon(
                resource_filename("brainrender_gui", "icons/eye-slash.svg")
            )
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
