from xlsxwriter.workbook import Workbook

from strings import UIStrings


class ShopData:
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

    def save_data_as_xlsx(self, data, path):
        wb = Workbook(path)
        worksheet = wb.add_worksheet()
        row = 0
        for shop in data:
            col = 0
            for item in shop:
                cell_format = wb.add_format()
                cell_format.set_border(1)
                if row == 0:
                    if col == 0:
                        cell_format.set_bg_color("yellow")
                    elif 0 < col < 13:
                        cell_format.set_bg_color("red")
                    elif col >= 13:
                        cell_format.set_bg_color("orange")
                else:
                    cell_format.set_bg_color("white")
                if (item != "") and (0 < row < len(shop)) and (0 < col < 14):
                    worksheet.write(row, col, float(item.replace(",", ".")), cell_format)
                else:
                    worksheet.write(row, col, item, cell_format)
                col += 1
            row += 1
        wb.close()
