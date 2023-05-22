from PyQt5.QtCore import QDate, QLocale
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the user interface from Designer.
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set the locale of the calendar widget to Persian (Iran).
        locale = QLocale(QLocale.Persian, QLocale.Iran)
        self.ui.calendarWidget.setLocale(locale)

        # Set the selected date of the calendar widget.
        date = QDate(1400, 2, 20)  # Jalali date: 1400/02/20
        self.ui.calendarWidget.setSelectedDate(date)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
