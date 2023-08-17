# coding: utf-8

import sys

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMainWindow, QWidget, QMenuBar, QStatusBar, QApplication, QVBoxLayout, QHBoxLayout, \
    QComboBox, QLabel

from display_widgets import ParamEqDisplayWidget
from option_widgets import OptionWidget
from param_eqs import LineParamEq, CircleParamEq, HyperbolaParamEq, LemniscateParamEq, HypotrochoidParamEq, \
    RoseCurveParamEq, LissajousParamEq, Extra1ParamEq, EpitrochoidParamEq

import images


class MainWindow(QMainWindow):
    options = [
        ('Line', LineParamEq, [
            ['x0', 'x0:', -500, 500, 1, 0],
            ['y0', 'y0:', -500, 500, 1, 0],
            ['k', 'k:', -1, 1, 0.05, 0.25]
        ]),
        ('Circle', CircleParamEq, [
            ['x0', 'x0:', -500, 500, 1, 0],
            ['y0', 'y0:', -500, 500, 1, 0],
            ['r', 'r:', 0.5, 500, 0.5, 1]
        ]),
        ('Hyperbola', HyperbolaParamEq, [
            ['x0', 'x0:', -500, 500, 1, 0],
            ['y0', 'y0:', -500, 500, 1, 0],
            ['a', 'a:', 0.1, 10, 0.1, 1],
            ['b', 'b:', 0.1, 10, 0.1, 1]
        ]),
        ('Lemniscate', LemniscateParamEq, [
            ['a', 'a:', 0.5, 500, 0.5, 1]
        ]),
        ('Hypotrochoid', HypotrochoidParamEq, [
            ['R', 'R:', 0.5, 500, 1, 2],
            ['r', 'r:', 0.5, 500, 1, 1],
            ['l', 'l:', 0, 2, 0.05, 0]
        ]),
        ('Epitrochoid', EpitrochoidParamEq, [
            ['R', 'R:', 0.5, 500, 1, 2],
            ['r', 'r:', 0.5, 500, 1, 1],
            ['l', 'l:', 0, 2, 0.05, 0]
        ]),
        ('Rose Curve', RoseCurveParamEq, [
            ['n', 'n:', 1, 50, 0.05, 1],
            ['a', 'a:', 0.5, 500, 1, 1]
        ]),
        ('Lissajous', LissajousParamEq, [
            ['a', 'a:', 0.5, 500, 1, 1],
            ['b', 'b:', 0.5, 500, 1, 1],
            ['p', 'p:', 0.5, 100, 1, 1],
            ['q', 'q:', 0.1, 100, 1, 1],
            ['phi', 'phi:', 0, 1.57, 0.05, 1]
        ]),
        ('Extra 1', Extra1ParamEq, [
            ['a', 'a:', 1, 50, 0.05, 1]
        ])
    ]
    label_eq_image_height = 200

    def __init__(self):
        super().__init__()

        self.resize(1024, 1024)

        # Menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Status bar
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # choices
        self.combo_box_choices = QComboBox(self)
        self.combo_box_choices.addItems(item[0] for item in MainWindow.options)
        self.combo_box_choices.currentIndexChanged.connect(self.on_choice_changed)
        choice_layout = QHBoxLayout()
        choice_layout.addStretch(1)
        choice_layout.addWidget(self.combo_box_choices)
        choice_layout.addStretch(1)

        # declaration of parametric equation
        self.label_eq_image = QLabel(self)
        self.label_eq_image.setMinimumHeight(self.label_eq_image_height)
        self.label_eq_image.setPixmap(QPixmap(':/images/' + MainWindow.options[0][0] + '.png')
                                      .scaledToHeight(self.label_eq_image_height))
        eq_image_layout = QHBoxLayout()
        eq_image_layout.addStretch(1)
        eq_image_layout.addWidget(self.label_eq_image)
        eq_image_layout.addStretch(1)

        # options and display
        self.param_eq_display_widget = ParamEqDisplayWidget(self)
        self.option_widget = OptionWidget(self, self.param_eq_display_widget)
        self.option_widget.set_param_eq_option(MainWindow.options[0])

        # all
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        layout.addLayout(choice_layout, 1)
        layout.addLayout(eq_image_layout, 1)
        layout.addWidget(self.option_widget, 1)
        layout.addWidget(self.param_eq_display_widget, 4)
        self.central_widget.setLayout(layout)

    def on_choice_changed(self, idx):
        self.label_eq_image.setPixmap(QPixmap(':/images/' + MainWindow.options[idx][0] + '.png')
                                      .scaledToHeight(self.label_eq_image_height))
        self.option_widget.set_param_eq_option(MainWindow.options[idx])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
