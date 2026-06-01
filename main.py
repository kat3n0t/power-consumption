import sys

from PyQt5 import QtWidgets

from app_presenter import AppPresenter
from power_consumption import App
from repository import FileRepository
from shop_model import ShopModel


def main():
    app_main = QtWidgets.QApplication(sys.argv)
    model = ShopModel()
    file_repository = FileRepository()
    presenter = AppPresenter(model, file_repository)
    window = App(presenter)
    presenter.set_view(window)
    window.show()
    sys.exit(app_main.exec_())


if __name__ == "__main__":
    main()
