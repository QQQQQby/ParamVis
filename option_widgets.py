from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QSlider, QLabel, QHBoxLayout, QGridLayout

from display_widgets import ParamEqDisplayWidget


# TODO: fix bugs

class OptionWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

    def set_param_eq_widget(self, param_eq_widget: ParamEqDisplayWidget, options: List[List]):
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.layout():
                child.layout().deleteLater()

        def make_slider_callback(widget, key):
            return lambda value: widget.set_param(key, value)
        for i, option in enumerate(options):
            item_layout = QHBoxLayout(self)
            item_layout.addStretch(1)

            label = QLabel(self)
            label.setText(option[1])
            item_layout.addWidget(label)

            slider = QSlider(self)
            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setRange(option[2], option[3])
            slider.setValue(option[4])
            slider.valueChanged.connect(make_slider_callback(param_eq_widget, option[0]))
            item_layout.addWidget(slider)

            param_eq_widget.set_param(option[0], option[4])

            item_layout.addStretch(1)
            self.main_layout.addLayout(item_layout, i // 4, i % 4)

