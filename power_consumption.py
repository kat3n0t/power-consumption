import csv
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDoubleSpinBox, QLayout

import dialog
import main_form
import shop_data
from strings import UIStrings, ErrorStrings


class App(QtWidgets.QMainWindow, main_form.Ui_MainWindow):
    _DELIMITER = ";"

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._shop_data = shop_data.ShopData()

        self._set_enabled_data_fields(False)

        self.comboBox_shop.currentIndexChanged.connect(self._change_shop)
        self.pushbtn_add_shop.clicked.connect(self._add_shop_click)
        self.pushbtn_del_shop.clicked.connect(self._del_shop_click)
        self.pushbtn_confirm_data.clicked.connect(self._update_data_click)
        self.pushbtn_open_total.clicked.connect(self._open_total_click)
        self.action_load_file.triggered.connect(self._load_file_click)
        self.action_save_file.triggered.connect(self._save_file_click)

    @property
    def _month_boxes(self) -> list[QDoubleSpinBox]:
        return [self.dblSpinBox_january, self.dblSpinBox_february, self.dblSpinBox_march, self.dblSpinBox_april,
                self.dblSpinBox_may, self.dblSpinBox_june, self.dblSpinBox_july, self.dblSpinBox_august,
                self.dblSpinBox_september, self.dblSpinBox_october, self.dblSpinBox_november, self.dblSpinBox_december]

    def _set_enabled_data_fields(self, is_enabled: bool):
        self._set_enabled_fields(self.grid_value, is_enabled)
        for grid_month in self.grid_months.children():
            self._set_enabled_fields(grid_month, is_enabled)
        self._set_enabled_fields(self.vlayout_data_buttons, is_enabled)

    # noinspection PyMethodMayBeStatic
    def _set_enabled_fields(self, layout: QLayout, is_enabled: bool):
        for item in range(len(layout)):
            layout_item = layout.itemAt(item)
            if layout_item is None:
                continue

            widget = layout_item.widget()
            if widget and isinstance(widget, (QtWidgets.QLabel, QtWidgets.QDoubleSpinBox, QtWidgets.QPushButton)):
                widget.setEnabled(is_enabled)

    def _change_shop(self):
        index = self.comboBox_shop.currentIndex()
        if index != -1:
            self._set_enabled_data_fields(True)
            self._refresh_shops(index)
            if not (self.pushbtn_confirm_data.isEnabled()):
                self.pushbtn_confirm_data.setEnabled(True)
        else:
            self._clear_app()
            self._set_enabled_data_fields(False)
            if self.pushbtn_confirm_data.isEnabled():
                self.pushbtn_confirm_data.setEnabled(False)

    def _refresh_shops(self, shop_number: int):
        for month_idx, month_box in enumerate(self._month_boxes):
            month_number = month_idx + 1
            value = self._shop_data.get_value_for_month(shop_number, month_number)
            month_box.setValue(value)
        self._refresh_shop_values(self._shop_data.get_shop_by_number(shop_number))

    def _refresh_shop_values(self, shop):
        if shop[13] != "":
            self.lbl_total_value.setText(shop[13])
        else:
            self.lbl_total_value.setText("0")
        if shop[14] != "":
            self.lbl_max_power_usage_value.setText(shop[14])
        else:
            self.lbl_max_power_usage_value.setText(UIStrings.NOT_FOUND)

    def _add_shop_click(self):
        name_shop, ok = QtWidgets.QInputDialog.getText(self, UIStrings.SHOP_NAME, UIStrings.ENTER_NEW_SHOP_NAME)
        if ok and name_shop != "":
            self._shop_data.add_shop(name_shop)
            self.comboBox_shop.addItem(name_shop)

    def _del_shop_click(self):
        index = self.comboBox_shop.currentIndex()
        if index != -1:
            self._shop_data.del_shop(index)
            self.comboBox_shop.removeItem(index)

    def _update_data_click(self):
        """
        Обрабатывает и сохраняет данные в памяти
        """

        shop_list = self._shop_data.get_shop_list()
        index = self.comboBox_shop.currentIndex()
        sum_months = [0.0]
        max_usage_month = [UIStrings.NOT_FOUND]
        self._set_data_months(sum_months, max_usage_month)
        sum_months[0] = format(sum_months[0], ".2f")  # во избежание перегрузок
        shop_list[index] = [self._shop_data.get_shop_name(index)]
        for box in self._month_boxes:
            shop_list[index].append(str(box.value()).replace(".", ","))
        shop_list[index].append(str(sum_months[0]).replace(".", ","))
        shop_list[index].append(max_usage_month[0])

        self._refresh_shops(index)

    def _set_data_months(self, sum_months, max_usage_month):
        """
        Изменяет значения принимаемых годовой суммы и месяца с максимальным потреблением,
        которые передаются как нулевой элемент списков
        """

        max_usage = 0.0
        for grid in self.grid_months.children():
            for i in range(len(grid)):
                if type(grid.itemAt(i).widget()) is QtWidgets.QDoubleSpinBox:
                    sum_months[0] += grid.itemAt(i).widget().value()
                    if grid.itemAt(i).widget().value() > max_usage:
                        max_usage = grid.itemAt(i).widget().value()
                        max_usage_month[0] = grid.itemAt(i).widget().statusTip()

    def _open_total_click(self):
        """
        Добавляет окно с итоговыми суммами
        """

        dialog_total = dialog.DialogTotal(self._shop_data.get_total_line())
        dialog_total.exec_()

    def _load_file_click(self):
        """
        Загружает данные из табличного файла
        """

        csv_path = QtWidgets.QFileDialog.getOpenFileName(self, UIStrings.CHOOSE_FILE, os.getenv("Home"), "CSV (*.csv)")
        if csv_path[0] != "":
            with open(csv_path[0], "r") as file:
                csv_reader = csv.reader(file, delimiter=self._DELIMITER)
                self._clear_app()
                try:
                    self._shop_data.load_shop_list(csv_reader)
                    shop_list = self._shop_data.get_shop_list()
                    for row in shop_list:
                        self.comboBox_shop.addItem(row[0])
                except:
                    QtWidgets.QMessageBox.about(self, ErrorStrings.DEFAULT, ErrorStrings.FILE_PARSE_FAILED)

    def _clear_app(self):
        """
        Очищает все поля с данными
        """

        self.comboBox_shop.clear()
        self._shop_data.clear_shops()
        self.lbl_max_power_usage_value.setText(UIStrings.NOT_FOUND)
        self.lbl_total_value.setText("0,00")
        for grid in self.grid_months.children():
            for i in range(len(grid)):
                if type(grid.itemAt(i).widget()) is QtWidgets.QDoubleSpinBox:
                    grid.itemAt(i).widget().setValue(0)

    def _save_file_click(self):
        """
        Сохраняет данные в табличный файл
        """

        shop_list = [self._shop_data.first_line]
        shop_list.extend(self._shop_data.get_shop_list())
        shop_list.append(self._shop_data.get_total_line())
        if len(shop_list) > 2:
            csv_path = QtWidgets.QFileDialog.getSaveFileName(self, UIStrings.SAVE_FILE, "",
                                                             "CSV (*.csv);;Excel (*.xlsx)")
            if csv_path[0] != "":
                try:
                    if ".csv" in csv_path[0]:
                        with open(csv_path[0], "w") as file:
                            csv_writer = csv.writer(file, delimiter=self._DELIMITER, lineterminator="\n")
                            for line in shop_list:
                                csv_writer.writerow(line)
                    elif ".xlsx" in csv_path[0]:
                        self._shop_data.save_data_as_xlsx(shop_list, csv_path[0])
                except:
                    QtWidgets.QMessageBox.about(self, ErrorStrings.DEFAULT, ErrorStrings.FILE_SAVE_FAILED)
        else:
            QtWidgets.QMessageBox.about(self, ErrorStrings.DEFAULT, ErrorStrings.SHOPS_NOT_FOUND)
