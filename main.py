import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from os.path import join
from os import getcwd
from PyQt5 import QtCore, QtGui, QtWidgets
import views.myviews as V
import views.counter as C
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep
from template.UI import Ui_MainWindow
import datetime


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.label.setPixmap(QtGui.QPixmap(join(getcwd(), "template", "admin.jpg")))
        self.ui.label_18.setPixmap(
            QtGui.QPixmap(join(getcwd(), "template", "icons", "cross.jpg"))
        )

        self.ui.label_19.setPixmap(
            QtGui.QPixmap(join(getcwd(), "template", "icons", "cross.jpg"))
        )
        self.ui.label_17.setPixmap(
            QtGui.QPixmap(join(getcwd(), "template", "icons", "cross.jpg"))
        )
        self.ui.label_22.setPixmap(
            QtGui.QPixmap(join(getcwd(), "template", "icons", "sighnup.jpg"))
        )
        self.ui.label_23.setPixmap(
            QtGui.QPixmap(join(getcwd(), "template", "icons", "recharge.jpg"))
        )
        self.ui.label_25.setPixmap(
            QtGui.QPixmap(join(getcwd(), "template", "icons", "cross.jpg"))
        )
        self.worker = worker()
        self.worker2 = worker2()
        self.worker3 = soundeffect()
        self.worker5 = worker5()

        self.worker4 = sighnup()
        # -------------------------------------------------------------------------------
        # Buttom Section:
        self.ui.memmberdelet_B.setEnabled(False)
        button = None
        self.ui.detail_B_2.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_8)
        )
        self.ui.pushButton.clicked.connect(self.admin)
        self.ui.sighnup_B.clicked.connect(lambda: self.snup("page"))
        self.ui.sighnup_B_2.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_3)
        )
        self.ui.detail_B_6.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_17)
        )
        self.ui.sighnup_B_3.clicked.connect(lambda: self.scan(button))
        self.ui.sighnup_B_8.clicked.connect(self.ncodeCounter)
        self.ui.sighnup_B_5.clicked.connect(self.ncodePage)
        self.ui.sighnup_B_4.clicked.connect(self.gif)
        self.ui.sighnup_B_9.clicked.connect(lambda: self.snup("record"))
        self.ui.sighnup_B_10.clicked.connect(self.snupClear)
        self.ui.recharge_B.clicked.connect(self.recharge_page)
        self.ui.acceptRecharge_B.clicked.connect(self.recharg)
        self.ui.sighnup_B_6.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_11, "historyrchive", self.ui.crossTable, False],
                self.ui.stackedWidget_4,
            )
        )
        self.ui.sighnup_B_12.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_13, "history", self.ui.presentTable, False],
                self.ui.stackedWidget_4,
            )
        )
        self.ui.sighnup_B_11.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_12, "memmber", self.ui.memTable, False],
                self.ui.stackedWidget_4,
            )
        )
        self.ui.sighnup_B_13.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_14, "history", self.ui.presentTable_2, V.didntTag()],
                self.ui.stackedWidget_4,
            )
        )
        self.ui.sighnup_B_14.clicked.connect(
            lambda: self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_15)
        )
        self.ui.acceptRecharge_B_3.clicked.connect(self.costDefine)
        self.ui.acceptRecharge_B_4.clicked.connect(self.adminDefine)
        self.ui.fullnamesearch.clicked.connect(
            lambda: self.searchMember(["fullname", self.ui.fullname_13.text()])
        )
        self.ui.ncodesearch.clicked.connect(
            lambda: self.searchMember(["nationalcode", self.ui.ncoode.text()])
        )
        self.ui.serialsearch.clicked.connect(self.idSearch)
        self.ui.editacceptin_B.clicked.connect(self.edit)
        self.ui.memmberdelet_B.clicked.connect(self.delete)
        self.ui.editacceptin_B.setEnabled(False)
        self.ui.member_B.clicked.connect(
            lambda: self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_10)
        )

        self.ui.fullnamesearch_2.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_11, "historyrchive", self.ui.crossTable, "filterd"],
                self.ui.stackedWidget_4,
            )
        )
        self.ui.fullnamesearch_3.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_11, "historyrchive", self.ui.crossTable, "today"],
                self.ui.stackedWidget_4,
            )
        )
        self.ui.detail_B.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_21, "logg", self.ui.memTable_2, False],
                self.ui.stackedWidget_2,
            )
        )
        self.ui.fullnamesearch_5.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_19, "logg", self.ui.memTable_2, "filterd2"],
                self.ui.stackedWidget_5,
            )
        )
        self.ui.fullnamesearch_7.clicked.connect(
            lambda: self.showTables(
                [self.ui.page_19, "logg", self.ui.memTable_2, "today"],
                self.ui.stackedWidget_5,
            )
        )
        self.ui.sighnup_B_19.clicked.connect(self.tred)
        QTimer.singleShot(1, self.admin)
        self.button = self.ui.sighnup_B_2
        self.inp = self.ui.counterLog_3

    # -------------------------------------------------------------------------------
    def idSearch(self):
        self.worker.stop()
        V.tagReader("stop")
        self.searchMember(["ID", V.tagReader("start")])

    def tred(self):
        self.enableButton(self.button)
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_16)
        self.worker.stop()
        V.tagReader("stop")
        self.worker5.start()

        self.worker5.data_signal5.connect(self.set_text4)

    def searchMember(self, where):
        self.worker3.run("select")

        global info
        info = V.select("*", "memmber", where)
        if info != None:
            self.ui.editLog.setText(
                f"""آقای {info[1]} به کد ملی {info[2]} باشماره تماس  {info[3]}"""
            )
            self.ui.editacceptin_B.setEnabled(True)
            self.ui.memmberdelet_B.setEnabled(True)
        else:
            self.ui.editLog.setText("""هیچ عضوی با این مشخصات یافت نشد""")
            self.ui.editacceptin_B.setEnabled(False)
            self.ui.memmberdelet_B.setEnabled(False)

    def edit(self):
        admin = V.select("ussername", "onlineadmin", None)[0][0]

        cul = [
            "fullname",
            "phone",
            "nationalcode",
            "debt",
        ]
        val = [
            self.ui.fullname_10.text(),
            self.ui.phonenumber_2.text(),
            self.ui.ncode_4.text(),
            self.ui.debt_3.text(),
        ]
        for cu, va in zip(cul, val):
            if len(va) != 0:
                V.execute(f"UPDATE memmber SET {cu} = %s WHERE ID = %s", (va, info[0]))
            else:
                continue
        self.ui.editacceptin_B.setEnabled(False)

        self.ui.editLog.setText("تغییرات با موفقیت در پایگاه داده ثبت شد")
        self.worker3.run("Accept3")
        self.ui.fullname_10.clear()
        self.ui.phonenumber_2.clear()
        self.ui.ncode_4.clear()
        self.ui.debt_3.clear()

    def delete(self):
        V.execute("DELETE FROM memmber WHERE ID = %s", (info[0],))
        self.ui.editLog.setText("عضو مورد نظر با موفقیت از پایگاه داده حذف گردید")
        admin = V.select("ussername", "onlineadmin", None)[0][0]
        V.execute(
            "INSERT INTO logg(adm, date0, tim, typ, customer) VALUES(%s, %s, %s, %s, %s)",
            (
                admin,
                str(datetime.date.today()),
                str(time.ctime()[11:19]),
                "حذف عضو ",
                info[1],
            ),
        )

        self.worker3.run("delete")

    def adminDefine(self):
        mass = V.setting(
            self.ui.fullname_3.text(),
            self.ui.fullname_4.text(),
            self.ui.fullname_9.text(),
        )
        self.ui.label_37.setText(mass)

    def costDefine(self):
        mass = V.costDefine(
            self.ui.recharge_categ_3.currentText(),
            self.ui.fullname_2.text(),
            self.ui.fullname_5.text(),
            self.ui.fullname_6.text(),
            self.ui.fullname_8.text(),
        )
        self.ui.label_37.setText(mass)

    def recharge_page(self):
        self.enableButton(self.button)
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_9)
        self.worker.stop()
        V.tagReader("stop")

    def recharg(self):
        mass = V.recharg(
            self.ui.recharge_categ.currentText(), self.ui.recharge_categ_2.currentText()
        )
        self.ui.counterLog_4.setText(mass[0])
        self.worker3.run(mass[1])

    def ncodePage(self):
        self.enableButton(self.button)
        self.ui.sighnup_B_5.setEnabled(False)
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_7)
        self.ui.sighnup_B_5.setEnabled(True)

    def ncodeCounter(self):
        self.enableButton(self.button)
        mass = C.count_analog(self.ui.entryNcode.text())
        self.ui.entryNcode.clear()
        V.soundSystem(mass[1])
        self.ui.counterLog_3.setText(mass[0])

    def show(self):
        self.main_win.show()

    def scan(self, button):
        self.enableButton(self.button)

        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_5)
        self.startcounter()

    def showTables(self, var, widg):
        self.enableButton(self.button)
        widg.setCurrentWidget(var[0])
        data = V.Tables(var[1])
        var[2].setRowCount(0)
        if var[-1] != False:
            data = var[-1]
        if var[-1] == "filterd":
            data = [
                tuple
                for tuple in V.Tables(var[1])
                if self.ui.fullname_18.text() in tuple
            ]
        if var[-1] == "filterd2":
            data = [
                tuple
                for tuple in V.Tables(var[1])
                if self.ui.fullname_20.text() in tuple
            ]

        if var[-1] == "today":
            data = [
                tuple
                for tuple in V.Tables(var[1])
                if V.date_convert(str(datetime.date.today())) in tuple
            ]
        if data != None:
            for i, row in enumerate(data):
                var[2].insertRow(i)
                for j, col in enumerate(row):
                    var[2].setItem(i, j, QTableWidgetItem(col))

    def enableButton(self, bt):
        bt.setEnabled(True)

    def gif(self):
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_6)

        self.enableButton(self.button)
        self.ui.sighnup_B_4.setEnabled(False)
        self.worker.stop()
        self.worker2.start()
        self.worker2.data_signal.connect(self.set_text2)
        self.button = self.ui.sighnup_B_4
        self.inp = self.ui.counterLog_2

    def admin(self):
        self.worker.stop()
        self.enableButton(self.button)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        if V.administrator(self.ui.lineEdit.text(), self.ui.lineEdit_2.text()):
            V.soundSystem("Passed")
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
        else:
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()

    def startcounter(self):
        self.enableButton(self.button)
        self.ui.sighnup_B_3.setEnabled(False)
        # V.tagReader("stop")
        self.worker.start()
        self.ui.counterLog.setText("سنسور روشن شد")
        self.worker.data_signal.connect(self.set_text)
        self.button = self.ui.sighnup_B_3

    def snup(self, ind):
        self.enableButton(self.button)
        if ind == "page":
            self.worker.stop()
            V.tagReader("stop")
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_4)
        else:
            mass = V.Register(
                self.ui.fullname.text(),
                self.ui.ncode.text(),
                self.ui.phoneNumber.text(),
                self.ui.debt.text(),
                self.ui.category.currentText(),
                self.ui.tredmil.currentText(),
            )
            self.worker4.run(mass[1])
            self.ui.label_11.setText(mass[0])

    def snupClear(self):
        self.ui.fullname.clear(),
        self.ui.ncode.clear(),
        self.ui.phoneNumber.clear(),
        self.ui.debt.clear(),
        self.ui.label_11.setText("عملیات ثبت نام متوقف شد")

    def set_text(self, mass):
        self.ui.counterLog.setText(mass)

    def set_text2(self, mass):
        self.ui.counterLog_2.setText(mass)
        return True

    def set_text3(self, mass):
        self.ui.counterLog_3.setText(mass)

    def inputCleaner(self, inp):
        inp.clear()

    def set_text4(self, mass):
        self.ui.counterLog_5.setText(mass)
        sleep(0.5)


class worker(QThread):
    data_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = True

    def run(self):
        self._is_running = True
        while self._is_running:
            mass = C.count_auto()
            if mass == "same":
                print("same card")
            else:
                self.data_signal.emit(mass[0])
                V.soundSystem(mass[1])
                sleep(2)
                V.tagReader("stop")
                if self.isInterruptionRequested():
                    break

    def stop(self):
        self._is_running = False
        self.requestInterruption()
        V.tagReader("stop")


class worker2(QThread):
    data_signal = pyqtSignal(str)

    def run(self):
        V.tagReader("stop")
        self.data_signal.emit(V.giftCounter())


class worker5(QThread):
    data_signal5 = pyqtSignal(str)

    def run(self):
        self.data_signal5.emit(V.tredCounter())


class sighnup(QThread):
    data_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self, ind):
        V.soundSystem(ind)


class soundeffect(QThread):
    def run(self, ind):
        V.soundSystem(ind)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
