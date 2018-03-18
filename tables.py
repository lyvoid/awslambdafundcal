from dynamodb_tool import Table, AssistColumnClass


class ChinaIndexEveryDay(Table):
    __table__ = 'china_index_every_day'

    today_index_value = AssistColumnClass()
    date = AssistColumnClass()
    avg_30_index = AssistColumnClass()
    avg_90_index = AssistColumnClass()
    avg_180_index = AssistColumnClass()
