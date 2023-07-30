from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout

from custom_widgets import DoubleSlider
from display_widgets import ParamEqDisplayWidget
from qt_utils import clear_layout


class OptionWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

    def set_param_eq_widget(self, param_eq_widget: ParamEqDisplayWidget, options: List[List]):
        clear_layout(self.main_layout)

        def make_slider_callback(key):
            return lambda value: param_eq_widget.set_param(key, value)

        for i, option in enumerate(options):
            item_layout = QHBoxLayout(self)
            item_layout.addStretch(1)

            label = QLabel(self)
            label.setText(option[1])
            item_layout.addWidget(label)

            slider = DoubleSlider(self)
            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setMinimum(option[2])
            slider.setMaximum(option[3])
            slider.setInterval(option[4])
            slider.setValue(option[5])
            slider.doubleValueChanged.connect(make_slider_callback(option[0]))
            item_layout.addWidget(slider)
            param_eq_widget.set_param(option[0], option[5])

            item_layout.addStretch(1)
            self.main_layout.addLayout(item_layout, i // 4, i % 4)
