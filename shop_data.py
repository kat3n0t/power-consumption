from enum import Enum

from xlsxwriter.format import Format
from xlsxwriter.workbook import Workbook

from strings import UIStrings


class ShopData:
    class _BgColor(str, Enum):
        YELLOW = "yellow"
        RED = "red"
        ORANGE = "orange"
        WHITE = "white"

    def __init__(self):
        self._shop_list: list[list[str]] = []

    @property
    def first_line(self) -> list[str]:
        return [UIStrings.SHOPS_LIST,
                UIStrings.MONTH_JAN, UIStrings.MONTH_FEB, UIStrings.MONTH_MAR, UIStrings.MONTH_APR,
                UIStrings.MONTH_MAY, UIStrings.MONTH_JUN, UIStrings.MONTH_JUL, UIStrings.MONTH_AUG,
                UIStrings.MONTH_SEP, UIStrings.MONTH_OCT, UIStrings.MONTH_NOV, UIStrings.MONTH_DEC,
                UIStrings.TOTAL_PER_YEAR, UIStrings.MAX_CONSUMPTION]

    def get_shop_list(self):
        return self._shop_list

    def get_shop_by_number(self, shop_number: int):
        return self._shop_list[shop_number]

    def load_shop_list(self, reader):
        for row in reader:
            if (row[0] != "") and not (reader.line_num == 1) and not (self._is_totals_row(row, reader)):
                self._add_shop_loaded_data(row)

    def _is_totals_row(self, row, reader):
        return (self._is_last_row(reader)) and (row[0] == UIStrings.TOTAL)

    def _is_last_row(self, reader):
        try:
            list_r = [reader]  # список позволяет копировать объект
            new_reader = list_r.copy()
            next(new_reader)  # переключаемся по новому reader'у
            return False
        except:
            return True

    def _add_shop_loaded_data(self, *shop_data):
        self._shop_list.append(*shop_data)

    def add_shop(self, name_shop):  # добавление нового цеха
        self._shop_list.append([name_shop, "0,00", "0,00", "0,00", "0,00", "0,00", "0,00", "0,00", "0,00", "0,00",
                                "0,00", "0,00", "0,00", "0,00", ""])

    def clear_shops(self):  # очистка списка цехов
        self._shop_list = []

    def del_shop(self, number_shop):
        if self._shop_list:
            del self._shop_list[number_shop]

    def get_value_for_month(self, number_shop, number_month):
        try:
            return float(self._shop_list[number_shop][number_month].replace(",", "."))
        except ValueError:
            return 0.0

    def get_shop_name(self, shop_number):
        return self._shop_list[shop_number][0]

    def get_total_line(self):
        total_line = [UIStrings.TOTAL]
        number_month = 1
        while number_month < 14:
            sum_month = 0.0
            for row in self._shop_list:
                if row[number_month] != "":
                    sum_month += float(row[number_month].replace(",", "."))
            total_line.append(str(sum_month).replace(".", ","))
            number_month += 1
        return total_line

    def save_data_as_xlsx(self, shop_list: list[list[str]], path: str):
        with Workbook(path) as wb:
            worksheet = wb.add_worksheet()

            fmt_yellow = self._create_format(wb, self._BgColor.YELLOW)
            fmt_red = self._create_format(wb, self._BgColor.RED)
            fmt_orange = self._create_format(wb, self._BgColor.ORANGE)
            fmt_white = self._create_format(wb, self._BgColor.WHITE)

            for row, shop in enumerate(shop_list):
                for col, item in enumerate(shop):
                    if row == 0:
                        if col == 0:
                            cell_format = fmt_yellow
                        elif 0 < col < 13:
                            cell_format = fmt_red
                        elif col >= 13:
                            cell_format = fmt_orange
                        else:
                            cell_format = fmt_white
                    else:
                        cell_format = fmt_white
                    if item and (row > 0) and (0 < col < 14):
                        worksheet.write(row, col, float(item.replace(",", ".")), cell_format)
                    else:
                        worksheet.write(row, col, item, cell_format)

    # noinspection PyMethodMayBeStatic
    def _create_format(self, wb: Workbook, bg_color: _BgColor) -> Format:
        fmt = wb.add_format()
        fmt.set_border(1)
        fmt.set_bg_color(bg_color)
        return fmt
