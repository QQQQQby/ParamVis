from typing import Union

from PySide2.QtCore import QPointF
from PySide2.QtGui import QPaintEvent, QPainter, QPen, QColor, QPainterPath, QMouseEvent, QTransform, QWheelEvent
from PySide2.QtWidgets import QWidget


class ParamEqDisplayWidget(QWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setMinimumSize(400, 400)
        self.setMouseTracking(True)

        self.param_eq = None
        self.points = None

        self.transform_scale = QTransform()
        self.transform_move = QTransform()
        self.transform_move.translate(200, 200)
        self.transform_move.scale(1, -1)
        self.prev_moved = None

        self.interval = 10

    def set_param_eq(self, param_eq_type, *args, do_repaint=True):
        self.param_eq = param_eq_type(*args)
        self.points = self.param_eq.get_points()
        if do_repaint:
            self.repaint()

    def set_param_eq_args(self, key: str, value: Union[int, float], do_repaint=True):
        if self.param_eq is None:
            raise RuntimeError('Parametric equation is None!')
        setattr(self.param_eq, key, value)
        self.points = self.param_eq.get_points()
        if do_repaint:
            self.repaint()

    def calc_real_coord(self, p: QPointF) -> QPointF:
        return self.transform_move.map(self.transform_scale.map(p))

    def wheelEvent(self, event: QWheelEvent) -> None:
        scale_range = (0.25, 10)
        step = 1.1

        angle = event.angleDelta() / 8
        angleY = angle.y()
        if angleY > 0:  # Zoom in
            self.transform_scale.scale(step, step)
            scale = self.transform_scale.m11()
            if scale > scale_range[1]:
                t = scale_range[1] / scale
                self.transform_scale.scale(t, t)

        else:  # Zoom out
            self.transform_scale.scale(1 / step, 1 / step)
            scale = self.transform_scale.m11()
            if scale < scale_range[0]:
                t = scale_range[0] / scale
                self.transform_scale.scale(t, t)

        self.repaint()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.prev_moved = QPointF(event.x(), event.y())
        self.repaint()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.prev_moved:
            curr_moved = QPointF(event.pos())
            offset = curr_moved - self.prev_moved
            self.transform_move.translate(offset.x(), -offset.y())
            self.prev_moved = curr_moved

            self.repaint()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.prev_moved = None

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter()
        painter.begin(self)

        # Draw axis
        painter.setPen(QPen(QColor(128, 128, 128), 3))
        center = self.calc_real_coord(QPointF(0, 0))
        painter.drawLine(center.x(), 0, center.x(), self.height() - 1)
        painter.drawLine(0, center.y(), self.width() - 1, center.y())

        # Draw ticks
        tick_length = 5

        i = self.interval
        while True:
            p0 = self.calc_real_coord(QPointF(i, 0))
            if p0.x() >= self.width():
                break
            p1 = QPointF(p0)
            p1.setY(p0.y() - tick_length)
            painter.drawLine(p0, p1)
            i += self.interval

        i = -self.interval
        while True:
            p0 = self.calc_real_coord(QPointF(i, 0))
            if p0.x() < 0:
                break
            p1 = QPointF(p0)
            p1.setY(p0.y() - tick_length)
            painter.drawLine(p0, p1)
            i -= self.interval

        i = self.interval
        while True:
            p0 = self.calc_real_coord(QPointF(0, i))
            if p0.y() < 0:
                break
            p1 = QPointF(p0)
            p1.setX(p0.x() + tick_length)
            painter.drawLine(p0, p1)
            i += self.interval

        i = -self.interval
        while True:
            p0 = self.calc_real_coord(QPointF(0, i))
            if p0.y() >= self.height():
                break
            p1 = QPointF(p0)
            p1.setX(p0.x() + tick_length)
            painter.drawLine(p0, p1)
            i -= self.interval

        # Draw Param Eq
        painter.setPen(QPen(QColor(255, 0, 0), 3))

        if self.points is not None:
            path = QPainterPath()
            path.moveTo(self.calc_real_coord(QPointF(*self.points[0])))
            for i in range(1, len(self.points)):
                path.lineTo(self.calc_real_coord(QPointF(*self.points[i])))

            painter.drawPath(path)

        # Draw border
        border_width = 5
        border_color = QColor(0, 0, 0)
        painter.fillRect(0, 0, self.width(), border_width, border_color)
        painter.fillRect(0, 0, border_width, self.height(), border_color)
        painter.fillRect(0, self.height() - border_width, self.width(), border_width, border_color)
        painter.fillRect(self.width() - border_width, 0, border_width, self.height(), border_color)

        painter.end()
