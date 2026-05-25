from PyQt5 import QtWidgets

import sum_month


class DialogTotal(QtWidgets.QDialog, sum_month.Ui_Dialog):
    def __init__(self, total):
        super().__init__()
        self.setupUi(self)
        self.set_data(total)

    def set_data(self, total):
        self.lbl_data_january.setText(total[1])
        self.lbl_data_february.setText(total[2])
        self.lbl_data_march.setText(total[3])
        self.lbl_data_april.setText(total[4])
        self.lbl_data_may.setText(total[5])
        self.lbl_data_june.setText(total[6])
        self.lbl_data_july.setText(total[7])
        self.lbl_data_august.setText(total[8])
        self.lbl_data_september.setText(total[9])
        self.lbl_data_october.setText(total[10])
        self.lbl_data_november.setText(total[11])
        self.lbl_data_december.setText(total[12])
        self.lcdNumber.display(total[13])
