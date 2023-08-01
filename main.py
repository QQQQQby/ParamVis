# coding: utf-8

import sys

from PySide2.QtCore import QRect
from PySide2.QtWidgets import QMainWindow, QWidget, QMenuBar, QStatusBar, QApplication, QVBoxLayout, QPushButton, \
    QHBoxLayout, QComboBox

from display_widgets import ParamEqDisplayWidget
from option_widgets import OptionWidget
from param_eqs import CircleParamEq, HypotrochoidParamEq


class MainWindow(QMainWindow):
    selector = [
        ('Circle', CircleParamEq, [
            ['radius', 'Radius:', 1, 1000, 1, 100]
        ]),
        ('Hypotrochoid', HypotrochoidParamEq, [
            ['R', 'R:', 50, 1000, 1, 100],
            ['k', 'k:', 0.001, 1, 0.01, 0.5],
            ['l', 'l:', 0.001, 2, 0.001, 1],
        ])
    ]

    def __init__(self):
        super().__init__()

        self.resize(640, 480)

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.menu_bar.setGeometry(QRect(0, 0, 640, 480))
        self.setMenuBar(self.menu_bar)

        # Status bar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # choices
        self.combo_box_choices = QComboBox(self)
        self.combo_box_choices.addItems(item[0] for item in MainWindow.selector)
        self.combo_box_choices.currentIndexChanged.connect(self.on_choice_changed)
        choice_layout = QHBoxLayout()
        choice_layout.addStretch(1)
        choice_layout.addWidget(self.combo_box_choices)
        choice_layout.addStretch(1)

        # options
        self.option_widget = OptionWidget(self)

        # display
        self.param_eq_display_widget = ParamEqDisplayWidget(self)
        self.param_eq_display_widget.set_param_eq(MainWindow.selector[0][1])
        self.option_widget.set_param_eq_widget(self.param_eq_display_widget, MainWindow.selector[0][2])
        self.param_eq_display_widget.show_image(True)

        # all
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.addLayout(choice_layout, 1)
        layout.addWidget(self.option_widget, 2)
        layout.addWidget(self.param_eq_display_widget, 4)
        self.central_widget.setLayout(layout)

    def on_choice_changed(self, idx):
        self.param_eq_display_widget.show_image(False)
        self.param_eq_display_widget.set_param_eq(MainWindow.selector[idx][1])
        self.option_widget.set_param_eq_widget(self.param_eq_display_widget, MainWindow.selector[idx][2])
        self.param_eq_display_widget.show_image(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
