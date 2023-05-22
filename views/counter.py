import views.myviews as V
import datetime
import asyncio

run = True
card = None


def count_auto():
    global card
    while run:
        id = V.tagReader("start")
        if V.checkSystem("memmber", ["ID", id]) == 1:
            info = V.select("*", "memmber", ["ID", id])
            days = V.diff(info[5])
            if int(info[7]) >= 1 and days > 0:
                if V.checkSystem("history", ["ID", id]) == 0:
                    V.history(id, 1)
                    V.update(["credit"], [str(int(info[7]) - 1)], ["ID", id])
                    mass = f"""
                    آقای {info[1]} وارد باشگاه شد
                    تعداد جلسه های باقیمانده {info[7]}
                    تعداد روز های باقی مانده {days}
                    تعداد جلسه های مهمان {info[8]}
                    تعداد جلسات تردمیل {info[11]}
                    مقدار بدهی {info[9]}
                    نوع طرح ایشان {info[6]} """

                    return [mass, "Accept1"]
                elif V.checkSystem("history", ["ID", id]) == 1:
                    crosstime = V.history(id, 2)
                    mass = f""" 
                    آقای {info[1]}  از باشگاه خارج شد.
                    ساعت ورود ایشان {crosstime[1]} است.
                    ساعت خروج ایشان {crosstime[2]} است.
                    ایشان {crosstime[0]} در باشگاه حضور داشتند."""
                    return [mass, "Accept1"]
                if int(info[7]) < 1:
                    mass = "اعتبار شما تمام شده است"
                    return [mass, "Error1"]
                else:
                    mass = "تاریخ انتقضا تمام شده است"
                    return [mass, "Error1"]
        mass = "این تگ اعتبار ندارد"
        return [mass, "Error1"]


def count_analog(ncode):
    if V.checkSystem("memmber", ["nationalcode", ncode]) == 1:
        info = V.select("*", "memmber", ["nationalcode", ncode])
        fullname = info[1]
        days = V.diff(info[5])

        if int(info[7]) > 0 and days > 0:
            if V.checkSystem("history", ["ID", info[0]]) == 0:
                V.history(info[0], 1)
                V.update(
                    [
                        "credit",
                    ],
                    [str(int(info[7]) - 1)],
                    [
                        "ID",
                        info[0],
                    ],
                )  # update_credit(, id)
                mass = f"""
                آقای {fullname} وارد باشگاه شد
                تعداد جلسه های باقیمانده {info[7]}
                تعداد روز های باقی مانده {days}
                تعداد جلسه های مهمان {info[8]}
                مقدار بدهی {info[9]}
                نوع طرح ایشان {info[6]} """
                return [mass, "Accept1"]
            if V.checkSystem("history", ["ID", info[0]]) == 1:
                crosstime = V.history(info[0], 2)

                mass = f""" 
                آقای {fullname}  از باشگاه خارج شد.
                ساعت ورود ایشان {crosstime[1]} است.
                ساعت خروج ایشان {crosstime[2]} است.
                ایشان {crosstime[0]} در باشگاه حضور داشتند."""
                return [mass, "Accept1"]
        else:
            mass = "اعتبار یا تاریخ شما تمام شده است"
            return [mass, "Error1"]

    return [mass, "Error1"]
