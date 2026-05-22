import sys

from PyQt5 import QtWidgets

from power_consumption import App


def main():
    app_main = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app_main.exec_())


if __name__ == "__main__":
    main()
