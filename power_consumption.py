import os
from typing import TYPE_CHECKING

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDoubleSpinBox, QLayout

import dialog
import main_form
from strings import UIStrings, ErrorStrings

if TYPE_CHECKING:
    from app_presenter import AppPresenter


class App(QtWidgets.QMainWindow, main_form.Ui_MainWindow):
    def __init__(self, presenter: "AppPresenter"):
        super().__init__()
        self.setupUi(self)

        self._presenter = presenter

        self.set_enabled_data_fields(False)

        self.comboBox_shop.currentIndexChanged.connect(
            lambda checked: self._presenter.on_shop_changed(self.comboBox_shop.currentIndex())
        )
        self.pushbtn_add_shop.clicked.connect(self._presenter.on_add_shop_clicked)
        self.pushbtn_del_shop.clicked.connect(
            lambda checked: self._presenter.on_delete_shop_clicked(self.comboBox_shop.currentIndex())
        )
        self.pushbtn_confirm_data.clicked.connect(
            lambda checked: self._presenter.on_data_update_clicked(self.comboBox_shop.currentIndex())
        )
        self.pushbtn_open_total.clicked.connect(self._presenter.on_open_total_clicked)
        self.action_load_file.triggered.connect(self._presenter.on_file_load_triggered)
        self.action_save_file.triggered.connect(self._presenter.on_file_save_triggered)

    @property
    def _month_boxes(self) -> list[QDoubleSpinBox]:
        return [self.dblSpinBox_january, self.dblSpinBox_february, self.dblSpinBox_march, self.dblSpinBox_april,
                self.dblSpinBox_may, self.dblSpinBox_june, self.dblSpinBox_july, self.dblSpinBox_august,
                self.dblSpinBox_september, self.dblSpinBox_october, self.dblSpinBox_november, self.dblSpinBox_december]

    def get_months_new_values_with_name(self) -> list[tuple[float, str]]:
        return [(box.value(), box.statusTip()) for box in self._month_boxes]

    def set_enabled_data_fields(self, is_enabled: bool):
        self._set_enabled_fields(self.grid_value, is_enabled)
        for grid_month in self.grid_months.children():
            self._set_enabled_fields(grid_month, is_enabled)
        self._set_enabled_fields(self.vlayout_data_buttons, is_enabled)

    def refresh_shop(self, shop: list[str], shop_months_values: list[float]):
        for month_idx, month_box in enumerate(self._month_boxes):
            month_value = shop_months_values[month_idx]
            month_box.setValue(month_value)
        self.set_shop_total(shop[13])
        self.set_shop_max_consumption(shop[14])

    def set_shop_total(self, total: str):
        if total:
            self.lbl_total_value.setText(total)
        else:
            self.lbl_total_value.setText("0")

    def set_shop_max_consumption(self, max_consumption: str):
        if max_consumption:
            self.lbl_max_power_usage_value.setText(max_consumption)
        else:
            self.lbl_max_power_usage_value.setText(UIStrings.NOT_FOUND)

    def add_shop(self, shop_name: str):
        self.comboBox_shop.addItem(shop_name)

    def remove_shop(self, shop_index: int):
        self.comboBox_shop.removeItem(shop_index)

    def clear_data_fields(self):
        self.comboBox_shop.clear()
        self.lbl_max_power_usage_value.setText(UIStrings.NOT_FOUND)
        self.lbl_total_value.setText("0,00")

        for month_box in self._month_boxes:
            month_box.setValue(0.0)

    def enable_confirm_button(self, is_enabled: bool):
        self.pushbtn_confirm_data.setEnabled(is_enabled)

    def show_total_dialog(self, totals: list[str]):
        dialog_total = dialog.DialogTotal(self, totals)
        dialog_total.exec_()

    def show_add_shop_dialog(self) -> tuple[str, bool | None]:
        return QtWidgets.QInputDialog.getText(self, UIStrings.SHOP_NAME, UIStrings.ENTER_NEW_SHOP_NAME)

    def show_open_file_name_dialog(self) -> str:
        return QtWidgets.QFileDialog.getOpenFileName(self, UIStrings.CHOOSE_FILE, os.getenv("Home"), "CSV (*.csv)")[0]

    def show_save_file_name_dialog(self) -> str:
        return QtWidgets.QFileDialog.getSaveFileName(self, UIStrings.SAVE_FILE, "", "CSV (*.csv);;Excel (*.xlsx)")[0]

    def show_error_message(self, error_message: ErrorStrings):
        QtWidgets.QMessageBox.about(self, UIStrings.ERROR_DEFAULT, error_message)

    # noinspection PyMethodMayBeStatic
    def _set_enabled_fields(self, layout: QLayout, is_enabled: bool):
        for item in range(len(layout)):
            layout_item = layout.itemAt(item)
            if layout_item is None:
                continue

            widget = layout_item.widget()
            if widget and isinstance(widget, (QtWidgets.QLabel, QtWidgets.QDoubleSpinBox, QtWidgets.QPushButton)):
                widget.setEnabled(is_enabled)
