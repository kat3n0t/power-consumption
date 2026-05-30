class ShopModel:
    _SHOP_INIT_CONSUMPTION = "0,00"
    _SHOP_INIT_MAX_CONSUMPTION = ""

    def __init__(self):
        self._shop_list: list[list[str]] = []  # list[Shop]

    @staticmethod
    def format_shop(shop_name: str, month_values: list[float],
                    sum_consumption: float, max_consumption_month_name: str) -> list[str]:
        formatted_values = [str(val).replace(".", ",") for val in month_values]
        formatted_sum = f"{sum_consumption:.2f}".replace(".", ",")
        return [shop_name] + formatted_values + [formatted_sum, max_consumption_month_name]

    @staticmethod
    def format_totals(totals: list[float]) -> list[str]:
        return [f"{val:.2f}".replace(".", ",") for val in totals]

    def get_shop_list(self) -> list[list[str]]:
        return [shop.copy() for shop in self._shop_list]

    def get_shop_by_index(self, shop_index: int) -> list[str]:  # нужно искать по id
        return self._shop_list[shop_index].copy()

    def get_shop_name(self, shop_index: int) -> str:  # нужно искать по id
        return self._shop_list[shop_index][0]

    def add_new_shop(self, shop_name: str):
        new_shop = [shop_name] + [ShopModel._SHOP_INIT_CONSUMPTION] * 13 + [ShopModel._SHOP_INIT_MAX_CONSUMPTION]
        self._add_shop(new_shop)

    def load_shop_list(self, shop_list: list[list[str]], total_marker: str) -> list[list[str]]:
        if not shop_list:
            return self._shop_list
        if shop_list[-1][0] == total_marker:
            shop_list.pop()
        for row in shop_list[1:]:
            self._add_shop(row)
        return self._shop_list

    def delete_shop(self, shop_index: int):
        if 0 <= shop_index < len(self._shop_list):  # нужно передавать id
            del self._shop_list[shop_index]

    def get_month_values(self, shop_index: int) -> list[float]:
        values = []
        shop_data = self._shop_list[shop_index]
        for month_number in range(1, 13):
            try:
                values.append(float(shop_data[month_number].replace(",", ".")))
            except ValueError:
                values.append(0.0)
        return values

    def get_monthly_totals(self) -> list[float]:
        totals: list[float] = []

        if not self._shop_list:
            return totals

        for month_number in range(1, 14):
            month_sum = 0.0
            for shop in self._shop_list:
                if shop[month_number]:
                    month_sum += float(shop[month_number].replace(",", "."))
            totals.append(month_sum)
        return totals

    def update_shop_record(self, shop_index: int, new_shop: list[str]):
        self._shop_list[shop_index] = new_shop

    def clear_shops(self):
        self._shop_list.clear()

    def _add_shop(self, shop: list[str]):
        self._shop_list.append(shop)
