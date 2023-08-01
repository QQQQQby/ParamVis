from typing import Union

from PySide2.QtCore import QPoint
from PySide2.QtGui import QPaintEvent, QPainter, QPen, QColor, QPainterPath
from PySide2.QtWidgets import QWidget


class ParamEqDisplayWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setMinimumSize(400, 400)

        self.param_eq = None

    def set_param_eq(self, param_eq_type, *args, do_repaint=True):
        self.param_eq = param_eq_type(*args)
        if do_repaint:
            self.repaint()

    def set_param_eq_args(self, key: str, value: Union[int, float], do_repaint=True):
        if self.param_eq is None:
            raise RuntimeError('Parametric equation is None!')
        setattr(self.param_eq, key, value)
        if do_repaint:
            self.repaint()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)

        # Draw border
        painter.setPen(QPen(QColor(255, 0, 0), 3))
        painter.drawLine(0, 0, self.width() - 1, 0)
        painter.drawLine(0, 0, 0, self.height() - 1)
        painter.drawLine(self.width() - 1, 0, self.width(), self.height())
        painter.drawLine(0, self.height() - 1, self.width(), self.height())

        # Draw Param Eq
        if self.param_eq is not None:
            points = self.param_eq.get_points()
            center = QPoint(self.width() // 2, self.height() // 2)
            path = QPainterPath()

            path.moveTo(center + QPoint(*points[0]))
            for i in range(1, len(points)):
                path.lineTo(center + QPoint(*points[i]))

            painter.setPen(QPen(QColor(255, 0, 0), 3))
            painter.drawPath(path)

        painter.end()
