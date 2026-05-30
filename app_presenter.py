from power_consumption import App
from repository import FileRepository
from shop_model import ShopModel
from strings import UIStrings, ErrorStrings


class AppPresenter:
    _UNSELECTED_SHOP_INDEX = -1

    def __init__(self, model: ShopModel, file_repository: FileRepository):
        self._view: App | None = None
        self._model = model
        self._file_repository = file_repository

    @property
    def _first_line(self) -> list[str]:
        return [UIStrings.SHOPS_LIST,
                UIStrings.MONTH_JAN, UIStrings.MONTH_FEB, UIStrings.MONTH_MAR, UIStrings.MONTH_APR,
                UIStrings.MONTH_MAY, UIStrings.MONTH_JUN, UIStrings.MONTH_JUL, UIStrings.MONTH_AUG,
                UIStrings.MONTH_SEP, UIStrings.MONTH_OCT, UIStrings.MONTH_NOV, UIStrings.MONTH_DEC,
                UIStrings.TOTAL_PER_YEAR, UIStrings.MAX_CONSUMPTION]

    def set_view(self, view: App):
        self._view = view

    def on_shop_changed(self, shop_index: int):
        if self._view is None:
            raise RuntimeError()

        if shop_index != self._UNSELECTED_SHOP_INDEX:
            self._view.set_enabled_data_fields(True)
            shop = self._model.get_shop_by_index(shop_index)
            shop_month_values = self._model.get_month_values(shop_index)
            self._view.refresh_shop(shop, shop_month_values)
            self._view.enable_confirm_button(True)
        else:
            self._view.clear_data_fields()
            self._view.set_enabled_data_fields(False)
            self._view.enable_confirm_button(False)

    def on_add_shop_clicked(self):
        if self._view is None:
            raise RuntimeError()

        shop_name, ok = self._view.show_add_shop_dialog()
        if ok and shop_name:
            self._model.add_new_shop(shop_name)
            self._view.add_shop(shop_name)

    def on_delete_shop_clicked(self, shop_index: int):
        if self._view is None:
            raise RuntimeError()

        if shop_index != self._UNSELECTED_SHOP_INDEX:
            self._model.delete_shop(shop_index)
            self._view.remove_shop(shop_index)

    def on_data_update_clicked(self, shop_index: int):
        if self._view is None:
            raise RuntimeError()

        months_new_values_with_name = self._view.get_months_new_values_with_name()
        month_values, sum_consumption, max_consumption_month_name, = self._calculate_months_data(
            months_new_values_with_name)

        shop_name = self._model.get_shop_name(shop_index)
        formatted_shop = ShopModel.format_shop(shop_name, month_values, sum_consumption, max_consumption_month_name)

        self._model.update_shop_record(shop_index, formatted_shop)
        self._view.set_shop_total(formatted_shop[13])
        self._view.set_shop_max_consumption(formatted_shop[14])

    def on_open_total_clicked(self):
        if self._view is None:
            raise RuntimeError()

        totals = self._model.get_monthly_totals()
        self._view.show_total_dialog(ShopModel.format_totals(totals))

    def on_file_load_triggered(self):
        if self._view is None:
            raise RuntimeError()

        csv_path = self._view.show_open_file_name_dialog()
        if csv_path:
            self._clear_data()
            try:
                csv_data = self._file_repository.load_from_csv(csv_path)
                shop_list = self._model.load_shop_list(csv_data, UIStrings.TOTAL)
                for row in shop_list:
                    self._view.add_shop(row[0])
            except Exception:
                self._view.show_error_message(ErrorStrings.FILE_PARSE_FAILED)

    def on_file_save_triggered(self):
        if self._view is None:
            raise RuntimeError()

        shop_list = [self._first_line]
        shop_list.extend(self._model.get_shop_list())
        shop_list.append(self._get_total_line())
        if len(shop_list) > 2:
            csv_path = self._view.show_save_file_name_dialog()
            if csv_path:
                try:
                    if csv_path.endswith(".csv"):
                        self._file_repository.save_to_csv(csv_path, shop_list)
                    elif csv_path.endswith(".xlsx"):
                        self._file_repository.save_to_xlsx(csv_path, shop_list)
                except Exception:
                    self._view.show_error_message(ErrorStrings.FILE_SAVE_FAILED)
        else:
            self._view.show_error_message(ErrorStrings.SHOPS_NOT_FOUND)

    # noinspection PyMethodMayBeStatic
    def _calculate_months_data(self, months_new_values_with_name: list[tuple[float, str]]) -> \
            tuple[list[float], float, str]:
        sum_consumption = 0.0
        max_consumption = 0.0
        max_consumption_month_name = UIStrings.NOT_FOUND
        month_values = []

        for month_value, month_name in months_new_values_with_name:
            sum_consumption += month_value
            month_values.append(month_value)

            if month_value > max_consumption:
                max_consumption = month_value
                max_consumption_month_name = month_name

        return month_values, sum_consumption, max_consumption_month_name

    def _clear_data(self):
        if self._view is None:
            raise RuntimeError()

        self._model.clear_shops()
        self._view.clear_data_fields()

    def _get_total_line(self) -> list[str]:
        total_line = []

        totals = self._model.get_monthly_totals()
        if not totals:
            return total_line

        total_line.append(UIStrings.TOTAL)
        total_line.extend(ShopModel.format_totals(totals))
        return total_line
