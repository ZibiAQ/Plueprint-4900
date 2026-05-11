from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)
from PySide6.QtCore import Qt


class DatasetSwitchDialog(QDialog):
    def __init__(self, dataset_names: list[str], current_name: str | None = None):
        super().__init__()
        self.setWindowTitle("Switch Dataset")
        self.resize(420, 360)

        self._selected_name: str | None = None

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Search:"))
        self.search = QLineEdit()
        self.search.setPlaceholderText("Type to filter datasets...")
        self.search.textChanged.connect(self._apply_filter)
        layout.addWidget(self.search)

        self.list = QListWidget()
        for name in dataset_names:
            self.list.addItem(QListWidgetItem(name))
        self.list.itemDoubleClicked.connect(lambda _: self._accept_selected())
        layout.addWidget(self.list)

        btns = QHBoxLayout()
        self.btnOk = QPushButton("Switch")
        self.btnCancel = QPushButton("Cancel")
        self.btnOk.clicked.connect(self._accept_selected)
        self.btnCancel.clicked.connect(self.reject)
        btns.addWidget(self.btnOk)
        btns.addWidget(self.btnCancel)
        layout.addLayout(btns)

        self.setLayout(layout)

        if current_name:
            matches = self.list.findItems(current_name, Qt.MatchExactly)
            if matches:
                self.list.setCurrentItem(matches[0])

    def _apply_filter(self):
        text = self.search.text().lower()
        for i in range(self.list.count()):
            item = self.list.item(i)
            item.setHidden(text not in item.text().lower())

    def _accept_selected(self):
        item = self.list.currentItem()
        if not item:
            return
        self._selected_name = item.text()
        self.accept()

    def selected_name(self) -> str | None:
        return self._selected_name

