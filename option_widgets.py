from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout

from custom_widgets import DoubleSlider
from display_widgets import ParamEqDisplayWidget
from qt_utils import clear_layout


class OptionWidget(QWidget):
    def __init__(self, parent, param_eq_display_widget: ParamEqDisplayWidget, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        self.param_eq_display_widget = param_eq_display_widget

    def set_param_eq_option(self, option):
        clear_layout(self.main_layout)
        self.param_eq_display_widget.set_param_eq(option[1], *(arg[5] for arg in option[2]))

        for i, arg in enumerate(option[2]):
            item_layout = QHBoxLayout(self)
            item_layout.addStretch(1)

            label = QLabel(self)
            label.setText(arg[1])
            item_layout.addWidget(label)

            slider = DoubleSlider(self)
            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setMinimum(arg[2])
            slider.setMaximum(arg[3])
            slider.setInterval(arg[4])
            slider.setValue(arg[5])
            slider.doubleValueChanged.connect(self._make_slider_callback(arg[0]))
            item_layout.addWidget(slider)

            item_layout.addStretch(1)

            self.main_layout.addLayout(item_layout, i // 4, i % 4)

    def _make_slider_callback(self, key):
        return lambda value: self.param_eq_display_widget.set_param_eq_args(key, value, True)
