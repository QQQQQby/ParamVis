from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QGridLayout, QDoubleSpinBox

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
            spinbox = QDoubleSpinBox(self)

            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setMinimum(arg[2])
            slider.setMaximum(arg[3])
            slider.setInterval(arg[4])
            slider.setValue(arg[5])
            item_layout.addWidget(slider)

            spinbox.setMinimum(arg[2])
            spinbox.setMaximum(arg[3])
            spinbox.setSingleStep(arg[4])
            spinbox.setValue(arg[5])
            item_layout.addWidget(spinbox)

            item_layout.addStretch(1)

            self.main_layout.addLayout(item_layout, i // 4, i % 4)

            slider.doubleValueChanged.connect(self._make_slider_callback(arg[0], spinbox))
            spinbox.valueChanged.connect(self._make_spinbox_callback(arg[0], slider))

    def _make_slider_callback(self, key, spinbox: QDoubleSpinBox):
        def func(value):
            return self.on_slider_value_changed(key, value, spinbox)

        return func

    def _make_spinbox_callback(self, key, slider: DoubleSlider):
        def func(value):
            return self.on_spinbox_value_changed(key, value, slider)

        return func

    def on_slider_value_changed(self, key, value, spinbox: QDoubleSpinBox):
        value = round(value, 2)
        spinbox.blockSignals(True)
        spinbox.setValue(value)
        spinbox.blockSignals(False)
        return self.param_eq_display_widget.set_param_eq_args(key, value)

    def on_spinbox_value_changed(self, key, value, slider: DoubleSlider):
        value = float(value)
        slider.blockSignals(True)
        slider.setValue(value)
        slider.blockSignals(False)
        return self.param_eq_display_widget.set_param_eq_args(key, value)
