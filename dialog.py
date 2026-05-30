from PyQt5 import QtWidgets

import sum_month


class DialogTotal(QtWidgets.QDialog, sum_month.Ui_Dialog):
    def __init__(self, parent: QtWidgets.QWidget | None, totals: list[str]):
        super().__init__(parent)
        self.setupUi(self)
        self._set_data(totals)

    @property
    def _month_labels(self) -> list[QtWidgets.QLabel]:
        return [self.lbl_data_january, self.lbl_data_february, self.lbl_data_march,
                self.lbl_data_april, self.lbl_data_may, self.lbl_data_june,
                self.lbl_data_july, self.lbl_data_august, self.lbl_data_september,
                self.lbl_data_october, self.lbl_data_november, self.lbl_data_december]

    def _set_data(self, totals: list[str]):
        for label, string_value in zip(self._month_labels, totals[:12]):
            label.setText(string_value)
        self.lcdNumber.display(totals[12])
