from qtpy.QtGui import QIcon

def get_in_alist(qlist):
    items = []
    for index in range(qlist.count()):
        items.append(qlist.item(index).text())
    return items


def update_actors_list(qlist, actorsdict):
    listed = get_in_alist(qlist)

    # Add items to list
    for actor in actorsdict.keys():
        if actor not in listed:
            qlist.insertItem(qlist.count() + 1, actor)

            item = qlist.item(qlist.count() - 1)
            item.setIcon(QIcon('brainrender_gui/icons/eye.svg'))



def remove_from_list(qlist, aname):
    if aname not in get_in_alist(qlist):
        raise ValueError(
            f"Attempting to remove {aname} from list, but {aname} not in list."
        )
    else:
        idx = [n for n, a in enumerate(get_in_alist(qlist)) if a == aname][0]
        qlist.takeItem(idx)
