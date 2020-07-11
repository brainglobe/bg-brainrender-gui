from qtpy.QtWidgets import (
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QLineEdit,
    QTreeView,
)
from PyQt5.Qt import QStandardItemModel

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from napari.utils.theme import palettes
import os
from pathlib import Path
from brainrender_gui.style import style, tree_css, update_css
from brainrender_gui.widgets.tree import StandardItem

class UI(QMainWindow):
    buttons = {}

    left_navbar_button_names = [
        "add brain regions",
        "add cells",
        "add from file",
        "add sharptrack",
    ]

    def __init__(self, theme="dark"):
        super().__init__()

        self.palette = palettes[theme]
        self.theme = theme

        # set the title of main window
        self.setWindowTitle("BRAINGLOBE - brainrender GUI")

        # set the size of window
        self.Width = 3000
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # Create UI
        self.get_icons()
        self.initUI()
        self.setStyleSheet(update_css(style, self.palette))

    def get_icons(self):

        fld = Path(os.path.dirname(os.path.realpath(__file__)))
        self.palette["branch_closed_img"] = str(
            fld / "icons" / f"right_{self.theme}.svg"
        ).replace("\\", "/")

        self.palette["branch_opened_img"] = str(
            fld / "icons" / f"down_{self.theme}.svg"
        ).replace("\\", "/")

        self.palette["checked_img"] = str(
            fld / "icons" / f"checkedbox_{self.theme}.svg"
        ).replace("\\", "/")

        self.palette["unchecked_img"] = str(
            fld / "icons" / f"box_{self.theme}.svg"
        ).replace("\\", "/")

    def make_left_navbar(self):
        """
            Creates the structures tree hierarchy widget and populates 
            it with structures names from the brainglobe-api's Atlas.hierarchy
            tree view.
        """
        # Create QTree widget
        treeView = QTreeView()
        treeView.setExpandsOnDoubleClick(False)
        treeView.setHeaderHidden(True)
        treeView.setStyleSheet(update_css(tree_css, self.palette))
        treeView.setWordWrap(False)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        # Add element's hierarchy
        tree = self.scene.atlas.hierarchy
        items = {}
        for n, node in enumerate(tree.expand_tree()):
            # Get Node info
            node = tree.get_node(node)
            if node.tag in ["VS", "fiber tracts"]:
                continue

            # Get brainregion name
            name = self.scene.atlas._get_from_structure(node.tag, "name")

            # Create Item
            item = StandardItem(
                name,
                node.tag,
                tree.depth(node.identifier),
                self.palette["text"],
            )

            # Get/assign parents
            parent = tree.parent(node.identifier)
            if parent is not None:
                if parent.identifier not in items.keys():
                    continue
                else:
                    items[parent.identifier].appendRow(item)

            # Keep track of added nodes
            items[node.identifier] = item
            if n == 0:
                root = item

        # Finish up
        rootNode.appendRow(root)
        treeView.setModel(treeModel)
        treeView.expandToDepth(2)
        self.treeView = treeView

        return treeView

    def make_right_navbar(self):
        # make layout
        layout = QVBoxLayout()

        # Add label
        layout.addWidget(QLabel("Add actors"))

        # Add buttons
        for bname in self.left_navbar_button_names:
            btn = QPushButton(bname.capitalize(), self)
            btn.setObjectName(bname.replace(" ", "_"))
            self.buttons[bname.replace(" ", "_")] = btn
            layout.addWidget(btn)

        # Add label
        lbl = QLabel("Actors")
        lbl.setObjectName('LabelWithBorder')
        layout.addWidget(lbl)

        # add list widget
        self.actors_list = QListWidget()
        self.actors_list.setObjectName("actors_list")
        layout.addWidget(self.actors_list)

        # Add label
        lbl = QLabel("Actor properties")
        lbl.setObjectName('LabelWithBorder')
        layout.addWidget(lbl)

        # Actor Alpha
        alphalabel = QLabel("Alpha")
        alphalabel.setObjectName("PropertyName")
        self.alpha_textbox = QLineEdit(self)
        self.alpha_textbox.setObjectName("Property")
        layout.addWidget(alphalabel)
        layout.addWidget(self.alpha_textbox)

        # Actor Color
        colorlabel = QLabel("Color")
        colorlabel.setObjectName("PropertyName")
        self.color_textbox = QLineEdit(self)
        self.color_textbox.setObjectName("Property")
        layout.addWidget(colorlabel)
        layout.addWidget(self.color_textbox)

        # set spacing
        layout.addStretch(5)
        layout.setSpacing(20)

        # make widget
        widget = QWidget()
        widget.setObjectName("RightNavbar")
        widget.setLayout(layout)

        return widget

    def make_brwidget(self):
        self.vtkWidget = QVTKRenderWindowInteractor(self)

    def initUI(self):
        # Create navbars
        self.treeView = self.make_left_navbar()
        right_navbar = self.make_right_navbar()

        # Create brainrender widget
        self.make_brwidget()

        # Make overall layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.treeView)
        main_layout.addWidget(self.vtkWidget)
        main_layout.addWidget(right_navbar)

        # Make the brwidget wider
        main_layout.setStretch(0, 70)
        main_layout.setStretch(1, 200)
        main_layout.setStretch(2, 70)

        # Create main window widget
        main_widget = QWidget()
        main_widget.setObjectName("MainWidget")
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
