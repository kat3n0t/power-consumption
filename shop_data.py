from xlsxwriter.workbook import Workbook


class ShopData:
    __shop_list = []

    def is_totals_row(self, row, reader):
        return (self.is_last_row(reader)) and (row[0] == "Итог")

    @staticmethod
    def is_last_row(reader):
        try:
            list_r = [reader]  # список позволяет копировать объект
            new_reader = list_r.copy()
            next(new_reader)  # переключаемся по новому reader'у
            return False
        except:
            return True

    def load_shop_list(self, reader):
        for row in reader:
            if (row[0] != "") and not(reader.line_num == 1) and not(self.is_totals_row(row, reader)):
                self.add_shop_loaded_data(row)

    def get_shop_list(self):    
        return self.__shop_list

    def add_shop_loaded_data(self, *shop_data):  # добавление загружаемых данных о цехе
        self.__shop_list.append(*shop_data)

    def add_shop(self, name_shop):  # добавление нового цеха
        self.__shop_list.append([name_shop, "0,00", "0,00", "0,00", "0,00", "0,00", "0,00", "0,00", "0,00", "0,00",
                                 "0,00", "0,00", "0,00", "0,00", ""])

    def clear_shops(self):  # очистка списка цехов
        self.__shop_list = []

    def del_shop(self, number_shop):
        if self.__shop_list:
            del self.__shop_list[number_shop]

    def get_value_for_month(self, number_shop, number_month):
        try:
            return float(self.__shop_list[number_shop][number_month].replace(",", "."))
        except ValueError:
            return 0.0

    def get_shop_name(self, shop_number):
        return self.__shop_list[shop_number][0]

    @staticmethod
    def get_first_line():
        return ["Список цехов", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь",
                "Октябрь", "Ноябрь", "Декабрь", "Итог за год", "Максимальное потребление"]

    def get_total_line(self):
        total_line = ["Итог"]
        number_month = 1
        while number_month < 14:
            sum_month = 0.0
            for row in self.__shop_list:
                if row[number_month] != "":
                    sum_month += float(row[number_month].replace(",", "."))
            total_line.append(str(sum_month).replace(".", ","))
            number_month += 1
        return total_line

    @staticmethod
    def save_data_as_xlsx(data, path):
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
