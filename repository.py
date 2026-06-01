import csv
from enum import Enum

from xlsxwriter import Workbook
from xlsxwriter.format import Format

from formatter import ConsumptionFormatter
from shop import Shop
from strings import CSVStrings


class FileRepository:
    _ENCODING = "utf-8-sig"
    _DELIMITER = ";"

    class _BgColor(str, Enum):
        YELLOW = "yellow"
        RED = "red"
        ORANGE = "orange"
        WHITE = "white"

    class _Columns(int, Enum):
        TITLE = 0
        MONTH_FIRST = 1
        MONTH_LAST = MONTH_FIRST + len(CSVStrings.MONTHS) - 1
        TOTAL = MONTH_LAST + 1
        MAX = TOTAL + 1

    def load_from_csv(self, file_path: str) -> list[Shop]:
        with open(file_path, "r", encoding=FileRepository._ENCODING) as file:
            csv_reader = csv.reader(file, delimiter=FileRepository._DELIMITER)
            csv_rows: list[list[str]] = [row for row in list(csv_reader)[1:-1] if row and row[0].strip()]
            return self._parse_csv_rows_to_shops(csv_rows)

    def save_to_csv(self, file_path: str, shops: list[Shop], totals: list[float]):
        with open(file_path, "w", encoding=FileRepository._ENCODING, newline="") as file:
            csv_writer = csv.writer(file, delimiter=FileRepository._DELIMITER, lineterminator="\n")
            csv_writer.writerows(self._serialize_shops_to_rows(shops, totals))

    def save_to_xlsx(self, file_path: str, shops: list[Shop], totals: list[float]):
        with Workbook(file_path) as wb:
            worksheet = wb.add_worksheet()

            fmt_yellow = self._create_format(wb, FileRepository._BgColor.YELLOW)
            fmt_red = self._create_format(wb, FileRepository._BgColor.RED)
            fmt_orange = self._create_format(wb, FileRepository._BgColor.ORANGE)
            fmt_white = self._create_format(wb, FileRepository._BgColor.WHITE)

            first_line = self._get_first_line()
            for col, item in enumerate(first_line):
                if col == FileRepository._Columns.TITLE:
                    cell_format = fmt_yellow
                elif FileRepository._Columns.MONTH_FIRST <= col <= FileRepository._Columns.MONTH_LAST:
                    cell_format = fmt_red
                else:
                    cell_format = fmt_orange
                worksheet.write(0, col, item, cell_format)

            shop_list = [self._serialize_shop_to_row_for_xlsx(shop) for shop in shops]
            shop_list.append(self._get_total_line_for_xlsx(totals))
            for row, line in enumerate(shop_list):
                for col, item in enumerate(line):
                    cell_format = fmt_white
                    worksheet.write(row + 1, col, item, cell_format)

    # noinspection PyMethodMayBeStatic
    def _parse_csv_rows_to_shops(self, rows: list[list[str]]) -> list[Shop]:
        shops: list[Shop] = []
        for row in rows:
            shop_name = row[0]
            shop_months_consumption: list[float] = []
            for month_index in range(FileRepository._Columns.MONTH_FIRST, FileRepository._Columns.MONTH_LAST + 1):
                month_consumption = row[month_index]
                shop_months_consumption.append(ConsumptionFormatter.parse_csv_value(month_consumption))
            shops.append(Shop(shop_name, shop_months_consumption))
        return shops

    def _serialize_shops_to_rows(self, shops: list[Shop], totals: list[float]) -> list[list[str]]:
        shop_list = [self._get_first_line()]
        shop_list.extend(self._serialize_shop_to_row(shop) for shop in shops)
        shop_list.append(self._get_total_line_for_csv(totals))
        return shop_list

    def _serialize_shop_to_row(self, shop: Shop) -> list[str]:
        months = ConsumptionFormatter.format_values(shop.months_values)
        total = ConsumptionFormatter.format_value(shop.total_per_year)

        max_month_index = shop.max_consumption_month_index
        max_month_name = self._get_max_month_name(max_month_index)
        return [shop.name] + months + [total, max_month_name]

    def _serialize_shop_to_row_for_xlsx(self, shop: Shop) -> list[str | float]:
        max_month_index = shop.max_consumption_month_index
        max_month_name = self._get_max_month_name(max_month_index)
        return [shop.name] + shop.months_values + [shop.total_per_year, max_month_name]

    # noinspection PyMethodMayBeStatic
    def _get_first_line(self) -> list[str]:
        return [CSVStrings.SHOPS_LIST, *CSVStrings.MONTHS, CSVStrings.TOTAL_PER_YEAR, CSVStrings.MAX_CONSUMPTION]

    # noinspection PyMethodMayBeStatic
    def _get_total_line_for_csv(self, totals: list[float]) -> list[str]:
        total_line = []

        if not totals:
            return total_line

        total_line.append(CSVStrings.TOTAL)
        total_line.extend(ConsumptionFormatter.format_values(totals))
        return total_line

    # noinspection PyMethodMayBeStatic
    def _get_total_line_for_xlsx(self, totals: list[float]) -> list[str | float]:
        total_line = []

        if not totals:
            return total_line

        total_line.append(CSVStrings.TOTAL)
        total_line.extend(totals)
        return total_line

    # noinspection PyMethodMayBeStatic
    def _get_max_month_name(self, max_month_index: int | None) -> str:
        return CSVStrings.MONTHS[max_month_index] if max_month_index is not None else ""

    # noinspection PyMethodMayBeStatic
    def _create_format(self, wb: Workbook, bg_color: _BgColor) -> Format:
        fmt = wb.add_format()
        fmt.set_border(1)
        fmt.set_bg_color(bg_color)
        return fmt
