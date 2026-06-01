from uuid import UUID

from shop import Shop


class ShopModel:
    _SHOP_INIT_CONSUMPTION = 0.0

    def __init__(self):
        self._shops: dict[UUID, Shop] = {}

    def get_shop_list(self) -> list[Shop]:
        return list(self._shops.values())

    def get_shop_by_id(self, shop_id: UUID) -> Shop | None:
        return self._shops.get(shop_id)

    def add_new_shop(self, shop_name: str):
        new_shop = Shop(shop_name, [ShopModel._SHOP_INIT_CONSUMPTION] * 12)
        self._add_shop(new_shop)
        return new_shop

    def add_shops(self, shops: list[Shop]):
        for shop in shops:
            self._add_shop(shop)

    def delete_shop(self, shop_id: UUID):
        self._shops.pop(shop_id, None)

    def get_monthly_and_yearly_totals(self) -> list[float]:
        totals: list[float] = []

        if not self._shops:
            return totals

        totals = [ShopModel._SHOP_INIT_CONSUMPTION] * 13
        for shop in self._shops.values():
            for month_index in range(12):
                totals[month_index] += shop.months_values[month_index]
            totals[12] += shop.total_per_year
        return totals

    def update_shop_record(self, shop_id: UUID, new_shop: Shop):
        if shop_id in self._shops:
            self._shops[shop_id] = new_shop

    def clear_shops(self):
        self._shops.clear()

    def _add_shop(self, shop: Shop):
        self._shops[shop.id] = shop
