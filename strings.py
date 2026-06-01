from enum import Enum


class _SharedStrings:
    MONTH_JAN = "Январь"
    MONTH_FEB = "Февраль"
    MONTH_MAR = "Март"
    MONTH_APR = "Апрель"
    MONTH_MAY = "Май"
    MONTH_JUN = "Июнь"
    MONTH_JUL = "Июль"
    MONTH_AUG = "Август"
    MONTH_SEP = "Сентябрь"
    MONTH_OCT = "Октябрь"
    MONTH_NOV = "Ноябрь"
    MONTH_DEC = "Декабрь"

    MONTHS = (
        MONTH_JAN, MONTH_FEB, MONTH_MAR, MONTH_APR, MONTH_MAY, MONTH_JUN,
        MONTH_JUL, MONTH_AUG, MONTH_SEP, MONTH_OCT, MONTH_NOV, MONTH_DEC
    )


class UIStrings:
    ERROR_DEFAULT = "Ошибка"
    NOT_FOUND = "Не найдено"

    SHOP_NAME = "Название цеха"
    ENTER_NEW_SHOP_NAME = "Введите название нового цеха"

    CHOOSE_FILE = "Выберите файл"
    SAVE_FILE = "Сохраните файл"

    MONTHS = _SharedStrings.MONTHS


class CSVStrings:
    SHOPS_LIST = "Список цехов"
    TOTAL = "Итог"
    TOTAL_PER_YEAR = "Итог за год"
    MAX_CONSUMPTION = "Максимальное потребление"
    MONTHS = _SharedStrings.MONTHS


class ErrorStrings(str, Enum):
    FILE_PARSE_FAILED = "Файл не может быть проанализирован"
    FILE_SAVE_FAILED = "Невозможно записать файл"

    SHOPS_NOT_FOUND = "Записи о цехах не найдены"
