import datetime

# サーバーがアメリカとかにあっても大丈夫なようutcからずらした日本時間の時刻を返す。
def now():
    return datetime.datetime.utcnow()+datetime.timedelta(hours=9)

def now_minute():
    return (datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime("%H:%M")

def now_day():
    return (datetime.datetime.utcnow()+datetime.timedelta(hours=9)).strftime("%Y-%m-%d")

# YYYY-MM-DD形式の文字列が今日より前かどうかを判別し、bool値で返す。
def if_date_before_today(date_string):
    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    except:
        return True # YYYY-MM-DD形式でないものもTrueとして処理する。
    return date < (datetime.datetime.utcnow()+datetime.timedelta(hours=9)).date()

# 今日から換算してn日後の日付をYYYY-MM-DD形式で返す。
def future_date(n):
    return ((datetime.datetime.utcnow()+datetime.timedelta(hours=9)).date() + datetime.timedelta(days=n)).strftime("%Y-%m-%d")