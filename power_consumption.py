import os
from typing import TYPE_CHECKING
from uuid import UUID

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDoubleSpinBox, QLayout

import dialog
import main_form
from formatter import ConsumptionFormatter
from shop import Shop
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
            lambda index: self._presenter.on_shop_changed(self.comboBox_shop.currentData())
        )
        self.pushbtn_add_shop.clicked.connect(self._presenter.on_add_shop_clicked)
        self.pushbtn_del_shop.clicked.connect(self._presenter.on_delete_shop_clicked)
        self.pushbtn_confirm_data.clicked.connect(self._presenter.on_data_update_clicked)
        self.pushbtn_open_total.clicked.connect(self._presenter.on_open_total_clicked)
        self.action_load_file.triggered.connect(self._presenter.on_file_load_triggered)
        self.action_save_file.triggered.connect(self._presenter.on_file_save_triggered)

    @property
    def _month_boxes(self) -> list[QDoubleSpinBox]:
        return [self.dblSpinBox_january, self.dblSpinBox_february, self.dblSpinBox_march, self.dblSpinBox_april,
                self.dblSpinBox_may, self.dblSpinBox_june, self.dblSpinBox_july, self.dblSpinBox_august,
                self.dblSpinBox_september, self.dblSpinBox_october, self.dblSpinBox_november, self.dblSpinBox_december]

    def get_months_new_values(self) -> list[float]:
        return [box.value() for box in self._month_boxes]

    def set_enabled_data_fields(self, is_enabled: bool):
        self._set_enabled_fields(self.grid_value, is_enabled)
        for grid_month in self.grid_months.children():
            self._set_enabled_fields(grid_month, is_enabled)
        self._set_enabled_fields(self.vlayout_data_buttons, is_enabled)

    def refresh_shop(self, shop: Shop):
        for month_idx, month_box in enumerate(self._month_boxes):
            month_value = shop.months_values[month_idx]
            month_box.setValue(month_value)
        self.refresh_calculated_shop_fields(shop)

    def refresh_calculated_shop_fields(self, shop: Shop):
        month_name = self._get_max_consumption_month_name(shop.max_consumption_month_index)
        self._set_shop_max_consumption(month_name)

        self._set_shop_total(ConsumptionFormatter.format_value(shop.total_per_year))

    def add_shop(self, shop: Shop):
        self.comboBox_shop.addItem(shop.name, shop.id)

    def remove_shop(self, shop_id: UUID):
        index_to_remove = self.comboBox_shop.findData(shop_id)
        if index_to_remove != -1:
            self.comboBox_shop.removeItem(index_to_remove)

    def clear_data_fields(self):
        self.comboBox_shop.clear()
        self._set_shop_max_consumption(UIStrings.NOT_FOUND)
        self._set_shop_total(ConsumptionFormatter.format_value(0.0))

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

    def _set_shop_max_consumption(self, max_consumption: str):
        self.lbl_max_power_usage_value.setText(max_consumption)

    def _set_shop_total(self, total: str):
        self.lbl_total_value.setText(total)

    # noinspection PyMethodMayBeStatic
    def _get_max_consumption_month_name(self, month_index: int | None) -> str:
        if month_index is None:
            return UIStrings.NOT_FOUND
        return UIStrings.MONTHS[month_index]

    # noinspection PyMethodMayBeStatic
    def _set_enabled_fields(self, layout: QLayout, is_enabled: bool):
        for item in range(layout.count()):
            layout_item = layout.itemAt(item)
            if layout_item is None:
                continue

            widget = layout_item.widget()
            if widget and isinstance(widget, (QtWidgets.QLabel, QtWidgets.QDoubleSpinBox, QtWidgets.QPushButton)):
                widget.setEnabled(is_enabled)
