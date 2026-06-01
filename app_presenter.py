from uuid import UUID

from formatter import ConsumptionFormatter
from power_consumption import App
from repository import FileRepository
from shop import Shop
from shop_model import ShopModel
from strings import ErrorStrings


class AppPresenter:
    def __init__(self, model: ShopModel, file_repository: FileRepository):
        self._model = model
        self._file_repository = file_repository
        self._view: App | None = None

        self._current_shop: Shop | None = None

    def set_view(self, view: App):
        self._view = view

    def on_shop_changed(self, shop_id: UUID | None):
        if self._view is None:
            raise RuntimeError()

        if shop_id is None:
            self._current_shop = None
            self._view.clear_data_fields()
            self._view.set_enabled_data_fields(False)
            self._view.enable_confirm_button(False)
            return

        shop = self._model.get_shop_by_id(shop_id)
        if shop is not None:
            self._current_shop = shop

            self._view.set_enabled_data_fields(True)
            self._view.refresh_shop(shop)
            self._view.enable_confirm_button(True)

    def on_add_shop_clicked(self):
        if self._view is None:
            raise RuntimeError()

        shop_name, ok = self._view.show_add_shop_dialog()
        if ok and shop_name:
            new_shop = self._model.add_new_shop(shop_name)
            self._view.add_shop(new_shop)

    def on_delete_shop_clicked(self):
        if self._view is None:
            raise RuntimeError()

        if self._current_shop is None:
            return
        shop_id = self._current_shop.id
        if shop_id is not None:
            self._current_shop = None
            self._model.delete_shop(shop_id)
            self._view.remove_shop(shop_id)

    def on_data_update_clicked(self):
        if self._view is None:
            raise RuntimeError()

        if self._current_shop is None:
            return
        shop_id = self._current_shop.id
        if shop_id is None:
            return

        months_new_values = self._view.get_months_new_values()
        self._current_shop.months_values = months_new_values

        self._model.update_shop_record(shop_id, self._current_shop)
        self._view.refresh_calculated_shop_fields(self._current_shop)

    def on_open_total_clicked(self):
        if self._view is None:
            raise RuntimeError()

        totals = self._model.get_monthly_and_yearly_totals()
        if not totals:
            self._view.show_error_message(ErrorStrings.SHOPS_NOT_FOUND)
            return
        self._view.show_total_dialog(ConsumptionFormatter.format_values(totals))

    def on_file_load_triggered(self):
        if self._view is None:
            raise RuntimeError()

        csv_path = self._view.show_open_file_name_dialog()
        if csv_path:
            self._clear_data()
            try:
                shop_list = self._file_repository.load_from_csv(csv_path)
                self._model.add_shops(shop_list)
                for shop in shop_list:
                    self._view.add_shop(shop)
            except Exception as e:
                print(e)
                self._view.show_error_message(ErrorStrings.FILE_PARSE_FAILED)

    def on_file_save_triggered(self):
        if self._view is None:
            raise RuntimeError()

        shops = self._model.get_shop_list()
        if len(shops) > 0:
            csv_path = self._view.show_save_file_name_dialog()
            if csv_path:
                totals = self._model.get_monthly_and_yearly_totals()
                try:
                    if csv_path.endswith(".csv"):
                        self._file_repository.save_to_csv(csv_path, shops, totals)
                    elif csv_path.endswith(".xlsx"):
                        self._file_repository.save_to_xlsx(csv_path, shops, totals)
                except Exception as e:
                    print(e)
                    self._view.show_error_message(ErrorStrings.FILE_SAVE_FAILED)
        else:
            self._view.show_error_message(ErrorStrings.SHOPS_NOT_FOUND)

    def _clear_data(self):
        if self._view is None:
            raise RuntimeError()

        self._current_shop = None
        self._model.clear_shops()
        self._view.clear_data_fields()
