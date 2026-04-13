import os
from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import QApplication, QMenu, QWidget

# 自定义图标路径，没有就显示字母 P
CUSTOM_ICON_PATH = None


class FloatingPill(QWidget):
    def __init__(self, mainWin):
        super().__init__()
        self.mainWin = mainWin
        self.dragAnchor = None
        self.startPress = None
        self.iconPix = QPixmap()

        if CUSTOM_ICON_PATH and os.path.isfile(CUSTOM_ICON_PATH):
            tmp = QPixmap(CUSTOM_ICON_PATH)
            if not tmp.isNull():
                self.iconPix = tmp

        self.setFixedSize(52, 52)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

    def place_default(self):
        r = QApplication.primaryScreen().availableGeometry()
        m = 16
        self.move(r.right() - self.width() - m, r.bottom() - self.height() - m)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(4, 4, self.width() - 8, self.height() - 8, 14, 14)
        painter.fillPath(path, QColor(30, 30, 36, 235))
        painter.strokePath(path, QPen(QColor(120, 120, 140, 200), 1))
        inner = QRect(6, 6, self.width() - 12, self.height() - 12)
        if not self.iconPix.isNull():
            painter.setClipPath(path)
            scaled = self.iconPix.scaled(
                inner.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            x = inner.x() + (inner.width() - scaled.width()) // 2
            y = inner.y() + (inner.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.setPen(QColor(240, 240, 245))
            font = QFont()
            font.setPointSize(11)
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "P")

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.dragAnchor = e.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.startPress = e.globalPosition().toPoint()
        elif e.button() == Qt.MouseButton.RightButton:
            menu = QMenu(self)
            a1 = menu.addAction("Restore window")
            a2 = menu.addAction("Quit")
            pick = menu.exec(e.globalPosition().toPoint())
            if pick == a1:
                self.mainWin.restore_from_floating()
            elif pick == a2:
                QApplication.quit()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.dragAnchor is not None and e.buttons() & Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self.dragAnchor)
        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            if self.startPress is not None:
                d = e.globalPosition().toPoint() - self.startPress
                if d.manhattanLength() <= 4:
                    self.mainWin.restore_from_floating()
            self.dragAnchor = None
            self.startPress = None
        super().mouseReleaseEvent(e)
