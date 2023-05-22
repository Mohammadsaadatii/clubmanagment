import datetime
import mysql.connector
import serial
import time
from dateutil.relativedelta import relativedelta
from playsound import playsound
from os.path import join
from os import getcwd
import jdatetime


ser = None
card = None


def database():
    try:
        db = mysql.connector.connect(
            user="root",
            host="localhost",
            password="Mohamad7139211@#",
            database="hellal_ahmar",
        )
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS adminbank(ussername varchar(255), pass varchar(255))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS onlineadmin(ussername varchar(255), pass varchar(255))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS accounting(adm varchar(255), date0 varchar(255), tim varchar(255), typ varchar(255), cost varchar(255), debt varchar(255))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS setting(adm varchar(255), A varchar(255), B varchar(255), C varchar(255), guest varchar(255), tred varchar(255))"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS logg(id varchar(255), adm varchar(255), date0 varchar(255), tim varchar(255), typ varchar(255), customer varchar(255))"
        )

        db.commit()
        print("connected to database")
        return db
    except:
        raise


database()


def select(cul, tabl, where):
    db = database()
    cursor = db.cursor()
    if where != None:
        cursor.execute(f"SELECT {cul} FROM {tabl} where {where[0]} = %s ", (where[1],))
        result = cursor.fetchone()
        db.close()
        return result

    cursor.execute(f"SELECT* FROM {tabl}")
    result = cursor.fetchall()
    db.close()
    return result


def date_convert(date0):
    shamsi = date0.split("-")
    return str(
        jdatetime.date.fromgregorian(
            day=int(shamsi[2]), month=int(shamsi[1]), year=int(shamsi[0])
        )
    )


def Tables(table):
    result = []

    if len(data := select(None, table, None)[::-1]) != 0:
        for tuple in data:
            temp = []
            for item in tuple[1:]:
                if item != None and "-" in item and ":" not in item:
                    temp.append(date_convert(item))
                else:
                    temp.append(item)
            result.append(temp)
        return result


def soundSystem(index):
    dict = {
        "Error1": "Error1.wav",
        "Error2": "Error2.mp3",
        "Accept1": "Accept1.mp3",
        "Accept2": "Accept2.mp3",
        "Accept3": "Accept3.wav",
        "select": "select.wav",
        "delete": "delete.wav",
        "Accept4": "Accept4.wav",
        "Passed": "Passed.wav",
    }
    playsound(join(getcwd(), "template", "sound", dict[index]))


def tagReader(ind):
    global ser

    if ind == "start":
        if ser == None:
            ser = serial.Serial("COM4", 9600)
        try:
            print("Place the card on the sensor...")
            result = str(ser.readline())[2:14]

            return result
        finally:
            if ser == None:
                ser.close()
                ser = None

    elif ind == "stop":
        if ser != None:
            if ser.isOpen:
                ser.close()
                ser = None


def execute(query, val):
    db = database()
    cursor = db.cursor()
    cursor.execute(query, val)
    db.commit()
    db.close()


def history(id, index):
    time0 = str(time.ctime()[11:19])
    date0 = str(datetime.date.today())
    info1 = select("*", "memmber", ["ID", id])
    if index == 1:
        execute(
            "INSERT INTO history (ID, fullname, date0, enter) values (%s, %s, %s, %s)",
            (
                id,
                info1[1],
                date0,
                time0,
            ),
        )
    if index == 2:
        info2 = select("*", "history", ["ID", id])
        t1 = datetime.datetime.strptime(str(info2[3]), "%H:%M:%S")
        t2 = datetime.datetime.strptime(str(time0), "%H:%M:%S")

        execute("DELETE FROM history WHERE ID = %s", (id,))
        execute(
            """INSERT INTO historyrchive(ID, fullname, date0, enter, exxit, diff)
                VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                info2[0],
                info2[1],
                info2[2],
                info2[3],
                time0,
                t2 - t1,
            ),
        )
        return t2 - t1, info2[3], time0


def update(var, val, where):
    for a, b in zip(var, val):
        execute(
            f"""UPDATE memmber SET {a} =%s where {where[0]} = %s """,
            (
                b,
                where[1],
            ),
        )


def checkSystem(tabl, where):
    result = select(where[0], tabl, where)
    return 1 if result != None else 0


def category(index, tred):
    def datetim(step):
        return str(datetime.date.today() + relativedelta(months=+step))

    info = select("*", "setting", None)[0][1:]
    dict1 = {
        "طرح A": {"cr": "20", "gi": "2", "co": info[0], "ex": datetim(1)},
        "طرح B": {"cr": "16", "gi": "1", "co": info[1], "ex": datetim(1)},
        "طرح C": {"cr": "12", "gi": "1", "co": info[2], "ex": datetim(1)},
        "": 0,
    }
    dict2 = {
        "دارد": {"cred": "12", "cos": info[4]},
        "ندارد": {"cred": "0", "cos": "0"},
        "": 0,
    }
    return (
        dict1[index]["cr"],
        dict1[index]["gi"],
        dict1[index]["co"],
        dict1[index]["ex"],
        dict2[tred]["cred"],
        dict2[tred]["cos"],
    )


def Register(fullname, nationalcode0, phone0, debt0, categ0, tred):
    result = category(categ0, tred)
    id = tagReader("start")
    if checkSystem("memmber", ["ID", id]) == 0:
        val = (
            id,
            fullname,
            nationalcode0,
            str(datetime.date.today()),
            str(result[3]),
            categ0,
            result[0],
            result[1],
            result[2],
            debt0,
            phone0,
            result[4],
        )
        execute(
            """INSERT INTO memmber (ID, fullname, nationalcode, date1, date2, category, credit, gift, cost, debt, phone, tred)
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            val,
        )
        admin = select("ussername", "onlineadmin", None)[0][0]
        execute(
            "INSERT INTO accounting(adm, date0,tim, typ, cost, debt) VALUES(%s,%s,%s,  %s, %s, %s)",
            (
                admin,
                str(datetime.date.today()),
                str(time.ctime()[11:19]),
                "ثبت نام",
                str(int(result[2]) + int(result[5])),
                debt0,
            ),
        )
        execute(
            "INSERT INTO logg(adm, date0, tim, typ, customer) VALUES(%s, %s, %s, %s, %s)",
            (
                admin,
                str(datetime.date.today()),
                str(time.ctime()[11:19]),
                "ثبت نام",
                fullname,
            ),
        )
        return ["ثبت نام با موفقیت انجام شد.", "Accept2"]
    return ["این تگ قبلا ثبت شده است", "Error2"]


def giftCounter():
    id = tagReader("start")

    if checkSystem("memmber", ["ID", id]) == 1:
        g = select("gift", "memmber", ["ID", id])[0]
        if int(g) <= 0:
            return "اعتبار مهمان شما تمام شده است!"
        execute("UPDATE memmber SET gift =%s ", ((str(int(g) - 1)),))

        return f"یک روز از اعتبار مهمان شما کسر گردید"
    return "شما هنوز ثبت نام نکرده اید"


def tredCounter():
    id = tagReader("start")

    if checkSystem("memmber", ["ID", id]) == 1:
        t = select("tred", "memmber", ["ID", id])[0]
        if int(t) <= 0:
            return "اعتبار تردمیل شما تمام شده است!"
        execute(
            "UPDATE memmber SET tred =%s where ID= %s",
            (
                (str(int(t) - 1)),
                id,
            ),
        )

        return "یک روز از اعتبار تردمیل شما کسر گردید"
    return "شما هنوز ثبت نام نکرده اید"


def recharg(index, tred):
    id = tagReader("start")
    if checkSystem("memmber", ["ID", id]) == 1:
        name = select("fullname", "memmber", ["ID", id])
        result = category(index, tred)
        date1 = str(datetime.date.today())
        update(
            ("credit", "gift", "cost", "date1", "date2", "tred", "category"),
            (
                result[0],
                result[1],
                result[2],
                date1,
                str(result[3]),
                result[4],
                index,
            ),
            ["ID", id],
        )
        date3 = str(result[3]).split("-")
        date4 = str(
            jdatetime.date.fromgregorian(
                day=int(date3[2]), month=int(date3[1]), year=int(date3[0])
            )
        )
        admin = select("ussername", "onlineadmin", None)[0][0]
        execute(
            "INSERT INTO accounting(adm, date0,tim, typ, cost, debt) VALUES(%s,%s,%s,  %s, %s, %s)",
            (
                admin,
                str(datetime.date.today()),
                str(time.ctime()[11:19]),
                "ثبت نام",
                str(int(result[2]) + int(result[5])),
                result[2],
            ),
        )
        execute(
            "INSERT INTO logg(adm, date0, tim, typ, customer) VALUES(%s, %s, %s, %s, %s)",
            (
                admin,
                str(datetime.date.today()),
                str(time.ctime()[11:19]),
                "شارژ مجدد",
                name[0],
            ),
        )

        return [
            f"آقای {name[0]} تا تاریخ {date4} تعداد {result[0]} جلسه شارژ شد! ",
            "Accept4",
        ]
    return ["این تگ ثبت نشده است", False]


def diff(exdate):
    d1 = datetime.datetime.strptime(exdate, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
    return (d1 - d2).days


def didntTag():
    offender = []
    result = select("*", "history", None)
    for tup in result:
        for item in tup:
            if item != None and "-" in item:
                if diff(item) < 0:
                    lst = list(tup)
                    lst.append(str(diff(item) * -1))
                    lst.remove(None)
                    offender.append(lst[1:])
    return offender


def administrator(uss, pas):
    db = database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM onlineadmin")
    cursor.execute("SELECT ussername , pass FROM adminbank ")
    usser = cursor.fetchall()
    if len(usser) == 0:
        cursor.execute(
            "INSERT INTO adminbank(ussername, pass) values (%s, %s)",
            (
                "عادل عشرتی",
                "7139211",
            ),
        )
        db.commit()
    usser_list = [f"{tup[0]}-{tup[1]}" for tup in usser]
    if f"{uss}-{pas}" in usser_list:
        cursor.execute(
            "INSERT INTO onlineadmin(ussername, pass) VALUES(%s, %s)", (uss, pas)
        )
        db.commit()
        return True
    return False


def setting(uss, pas, admin_pass):
    admin = select("ussername", "onlineadmin", None)[0][0]
    if admin_pass == "7139211":
        execute(
            "INSERT INTO adminbank(ussername , pass ) VALUES(%s, %s)",
            (
                uss,
                pas,
            ),
        )
        return "ادمین جدید با موفقیت تعریف شد"
    return "  شما اجازه تعریف ادمین جدید ندارید لطفا به کاربر روت اطلاع دهید"


def logg(type):
    admin = select("ussername", "onlineadmin", None)[0][0]
    date = str(datetime.date.today())
    time = str(time.ctime()[11:19])
    execute(
        "INSERT INTO logg(adm, date0, tim, typ) values(%s, %s, %s, %s)",
        (admin, date, time, type),
    )


def costDefine(category, categoryCost, gues, tredmil, admin_pass):
    admin = select("ussername", "onlineadmin", None)[0][0]
    if admin_pass == "7139211":
        cul = {
            "طرح A": "A",
            "طرح B": "B",
            "طرح C": "C",
        }

        item = [admin, categoryCost, gues, tredmil]
        column = ["adm", cul[category], "guest", "tred"]
        for val, cul in zip(item, column):
            if len(val) != 0:
                execute(f"UPDATE setting SET {cul}= %s", (val,))
            else:
                continue
        return "نرخ ها با موفقیت ثبت شدند"
    return "شما اجازه تغییر نرخ ها را ندارید لطفا به کاربر روت اطلاع دهید"
