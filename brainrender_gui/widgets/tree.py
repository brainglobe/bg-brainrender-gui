from PyQt5.Qt import QStandardItem, Qt
from PyQt5.QtGui import QFont, QColor


class StandardItem(QStandardItem):
    def __init__(self, txt="", tag=None, depth=0, color=None):
        """
            Items in the tree list with some
            extended functionality to specify/update
            their look. 
        """
        super().__init__()
        self.depth = depth  # depth in the hierarchy structure
        self.tag = tag

        # Set font color/size
        self.bold = False
        self.toggle_active()

        # Set text
        self.setEditable(False)
        rgb = color.replace(")", "").replace(" ", "").split("(")[-1].split(",")
        self.setForeground(QColor(*[int(r) for r in rgb]))
        self.setText(txt)

        # Set checkbox
        self.setFlags(
            self.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable
        )
        self.setCheckState(Qt.Unchecked)
        self._checked = False

    def toggle_active(self):
        """
            When a mesh corresponding to the item's region
            get's rendered, change the font to bold
            to highlight the fact. 
        """
        fnt = QFont("Roboto", 14)
        fnt.setBold(self.bold)
        self.setFont(fnt)
