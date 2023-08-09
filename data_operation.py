import jst_time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from logging import getLogger

logger = getLogger("Log").getChild("data_operation")

# 多次元リストを一次元化する再帰処理。
flatten = lambda x: [z for y in x for z in (flatten(y) if hasattr(y, '__iter__') and not isinstance(y, str) else (y,))]

# Googleスプレッドシートに接続し、予定表のデータとbotのセリフのフォーマットを読み込む。
def get_data(jsonf, sheet_key):
    logger.debug("Executing get_data...")
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    spread_sheet = gspread.authorize(credentials).open_by_key(sheet_key)
    data, prefix = spread_sheet.get_worksheet(0).get_all_values(), spread_sheet.get_worksheet(1).get_all_values()
    logger.debug("get_data executed.")
    return data, prefix

# Googleスプレッドシートに接続して指定日時分先までの日付をシートに自動で記入し、不要になったリマインドの履歴を別シートにアーカイブする。
def auto_arrange(jsonf, sheet_key, margin):
    logger.debug("Executing auto_arrange...")
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    spread_sheet = gspread.authorize(credentials).open_by_key(sheet_key)
    data_sheet, archive_sheet = spread_sheet.get_worksheet(0), spread_sheet.get_worksheet(2)
    data = data_sheet.get_all_values()[3:]
    del_idx_list = []
    insert_list = []
    for i in range(len(data)):
        if jst_time.if_date_before_today(data[i][0]):
            del_idx_list.append(i+3)
            insert_list.append(list(map(lambda x: str(x), flatten(data[i]))))
    for i in reversed(del_idx_list):
        data_sheet.delete_rows(i+1)
    archive_sheet.insert_rows(insert_list, row=1)
    data = sorted(data_sheet.get_all_values()[3:])
    for i in range(len(data)):
        data[i] = list(map(lambda x: str(x), flatten(data[i])))
    
    # 指定日時分先までの日付がなかった場合付け足す。高速化の余地あり。めんどいのでやらん。
    for i in range(margin):
        found = False
        for j in range(len(data)):
            if data[j][0] == jst_time.future_date(i):
                found = True
                break
        if not found:
            data.append([jst_time.future_date(i)]+[""]*5)
    data = sorted(data)
    data_sheet.update("A4", data)
    logger.debug("auto_arrange executed.")
    return

# データの中から引数で指定された日時の活動場所やイベントなどをリスト形式で返す。
def search(data, day):
    logger.debug("Executing search...")
    place_lists = []
    place_rooms = []
    place_remarks = []
    # ここ2分探索すればちょい早い。けどめんどいので放置。
    found = False
    for i in range(3, len(data)):
        if data[i][0] == day:
            Y = i
            found = True
            break
    if not found:
        logger.debug("search executed.")
        return None # 該当日時のデータがない場合何も返さない。
    for i in range(1, len(data[0])):
        if data[1][i]:
            place_lists.append(data[1][i])
        if data[2][i]:
            if i % 2 == 0:
                place_remarks.append(data[Y][i])
            else:
                place_rooms.append(data[Y][i])
        if i > 1 and data[0][i+1]:
            X = i+1
            break
    event_names = data[Y][X].replace('、',',').split(',')
    event_places = data[Y][X+1].replace('、',',').split(',')
    event_remarks = data[Y][X+2].split(',')
    messages = data[Y][X+3]
    res = [[place_lists, place_rooms, place_remarks], [event_names, event_places, event_remarks], [messages]]
    logger.debug("search executed.")
    return res
