from PySide2.QtWidgets import QLayout


def clear_layout(layout: QLayout):
    if layout is None:
        return
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        else:
            clear_layout(item.layout())
