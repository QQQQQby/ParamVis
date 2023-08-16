from typing import Union

from PySide2.QtCore import QPoint, QPointF
from PySide2.QtGui import QPaintEvent, QPainter, QPen, QColor, QPainterPath, QMouseEvent, QTransform, QWheelEvent, \
    QFontMetrics, QFont
from PySide2.QtWidgets import QWidget


class ParamEqDisplayWidget(QWidget):
    scale_range = (0.1, 500)
    scale_step = 1.1
    scales_to_intervals = [
        [100, 1], [50, 2], [20, 5],
        [10, 10], [5, 20], [2, 50],
        [1, 100], [0.5, 200], [0.2, 500], [0, 1000]
    ]
    tick_length = 10
    x_tick_margin = 5
    y_tick_margin = 10

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setMinimumSize(400, 400)
        self.resize(1000, 600)
        self.setMouseTracking(True)

        self.param_eq = None
        self.points = None

        self.transform_scale = QTransform()
        self.transform_move = QTransform()
        self.transform_move.translate(500, 300)
        self.transform_move.scale(1, -1)
        self.prev_moved = None

        self.interval = 100

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

    def calc_real_coord(self, p: Union[QPoint, QPointF]) -> Union[QPoint, QPointF]:
        return self.transform_move.map(self.transform_scale.map(p))

    def wheelEvent(self, event: QWheelEvent) -> None:

        angle = event.angleDelta() / 8
        angleY = angle.y()
        if angleY > 0:  # Zoom in
            self.transform_scale.scale(self.scale_step, self.scale_step)
            scale = self.transform_scale.m11()
            if scale > self.scale_range[1]:
                t = self.scale_range[1] / scale
                self.transform_scale.scale(t, t)

        else:  # Zoom out
            self.transform_scale.scale(1 / self.scale_step, 1 / self.scale_step)
            scale = self.transform_scale.m11()
            if scale < self.scale_range[0]:
                t = self.scale_range[0] / scale
                self.transform_scale.scale(t, t)

        scale = self.transform_scale.m11()
        i = 0
        while i < len(self.scales_to_intervals) and self.scales_to_intervals[i][0] > scale:
            i += 1
        self.interval = self.scales_to_intervals[i][1]

        self.repaint()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.prev_moved = QPoint(event.x(), event.y())
        self.repaint()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.prev_moved:
            curr_moved = QPoint(event.pos())
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
        center = self.calc_real_coord(QPoint(0, 0))
        painter.drawLine(center.x(), 0, center.x(), self.height() - 1)
        painter.drawLine(0, center.y(), self.width() - 1, center.y())

        # Draw ticks
        label_font = QFont('Times New Romans', 16, QFont.Bold)
        painter.setFont(label_font)
        label_font_metrics = QFontMetrics(label_font)

        i = self.interval
        while True:
            p0 = self.calc_real_coord(QPoint(i, 0))
            if p0.x() >= self.width():
                break
            p1 = QPoint(p0)
            p1.setY(p0.y() - self.tick_length)
            painter.drawLine(p0, p1)

            label_str = str(i)
            label_rect = label_font_metrics.boundingRect(label_str)
            label_rect.moveCenter(p0)
            label_rect.moveTop(p0.y() + self.x_tick_margin)
            painter.drawText(label_rect.bottomLeft(), label_str)

            i += self.interval

        i = -self.interval
        while True:
            p0 = self.calc_real_coord(QPoint(i, 0))
            if p0.x() < 0:
                break
            p1 = QPoint(p0)
            p1.setY(p0.y() - self.tick_length)
            painter.drawLine(p0, p1)

            label_str = str(i)
            label_rect = label_font_metrics.boundingRect(label_str)
            label_rect.moveCenter(p0)
            label_rect.moveTop(p0.y() + self.x_tick_margin)
            painter.drawText(label_rect.bottomLeft(), label_str)

            i -= self.interval

        i = self.interval
        while True:
            p0 = self.calc_real_coord(QPoint(0, i))
            if p0.y() < 0:
                break
            p1 = QPoint(p0)
            p1.setX(p0.x() + self.tick_length)
            painter.drawLine(p0, p1)

            label_str = str(i)
            label_rect = label_font_metrics.boundingRect(label_str)
            label_rect.moveCenter(p0)
            label_rect.moveRight(p0.x() - self.y_tick_margin)
            painter.drawText(label_rect.bottomLeft(), label_str)

            i += self.interval

        i = -self.interval
        while True:
            p0 = self.calc_real_coord(QPoint(0, i))
            if p0.y() >= self.height():
                break
            p1 = QPoint(p0)
            p1.setX(p0.x() + self.tick_length)
            painter.drawLine(p0, p1)

            label_str = str(i)
            label_rect = label_font_metrics.boundingRect(label_str)
            label_rect.moveCenter(p0)
            label_rect.moveRight(p0.x() - self.y_tick_margin)
            painter.drawText(label_rect.bottomLeft(), label_str)

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
