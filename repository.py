import csv
from enum import Enum

from xlsxwriter import Workbook
from xlsxwriter.format import Format


class FileRepository:
    _ENCODING = "utf-8-sig"
    _DELIMITER = ";"

    class _BgColor(str, Enum):
        YELLOW = "yellow"
        RED = "red"
        ORANGE = "orange"
        WHITE = "white"

    def load_from_csv(self, file_path: str) -> list[list[str]]:
        with open(file_path, "r", encoding=self._ENCODING) as file:
            csv_reader = csv.reader(file, delimiter=self._DELIMITER)
            return [row for row in csv_reader if row and row[0].strip()]

    def save_to_csv(self, file_path: str, shop_list: list[list[str]]):
        with open(file_path, "w", encoding=self._ENCODING, newline='') as file:
            csv_writer = csv.writer(file, delimiter=self._DELIMITER, lineterminator="\n")
            for line in shop_list:
                csv_writer.writerow(line)

    def save_to_xlsx(self, file_path: str, shop_list: list[list[str]]):
        with Workbook(file_path) as wb:
            worksheet = wb.add_worksheet()

            fmt_yellow = self._create_format(wb, self._BgColor.YELLOW)
            fmt_red = self._create_format(wb, self._BgColor.RED)
            fmt_orange = self._create_format(wb, self._BgColor.ORANGE)
            fmt_white = self._create_format(wb, self._BgColor.WHITE)

            for row, line in enumerate(shop_list):
                for col, item in enumerate(line):
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
