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
