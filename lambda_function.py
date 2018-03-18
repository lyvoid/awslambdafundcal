import json
from util import *
from tables import *
import logging
from strategy import *

logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    logging.info(event)
    logging.info(context)
    cal()
    response_dict = {}
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response_dict),
        "isBase64Encoded": False
    }
    return response


def cal():
    date_today = get_today_date()
    # get yesterday value
    date_yest = get_yest_date(date_today)
    date_yy = get_yest_date(date_yest)
    logging.info("today date is %s, yesterday date %s is" %
                 (str(date_today), str(date_yest)))
    sz_values_yy = ChinaIndexEveryDay()
    if not sz_values_yy.load(str(date_yy)):
        logging.error('cannot get index value of the day before yesterday')
        return

    sz_values_y = ChinaIndexEveryDay()
    if sz_values_y.load(str(date_yest)):
        logging.info(
            'yesterday sz index value is exist. value: %s"' %
            sz_values_y.today_index_value)
    else:
        # if yesterday index value is not in database, update new average date
        # in this case, i don't care whether yesterday is trade day or not
        # save yesterday index value to database
        sz_values_y.date = str(date_yest)
        sz_values_y.today_index_value = get_yest_sz_index()
        # calculate new average of 30 90 180 days' value
        sz_values_tail = ChinaIndexEveryDay()
        sz_values_head = ChinaIndexEveryDay()

        sz_values_tail.load(str(get_next_n_date(date_yest, -30 + 15)))
        # need delete, -1 more
        sz_values_head.load(str(get_next_n_date(date_yest, -30 - 15 - 1)))
        sz_values_y.avg_30_index = (
                                           sz_values_yy.avg_30_index * 31 +
                                           sz_values_tail.today_index_value -
                                           sz_values_head.today_index_value
                                   ) / 31

        sz_values_tail.load(str(get_next_n_date(date_yest, - 90 + 15)))
        sz_values_head.load(str(get_next_n_date(date_yest, - 90 - 15 - 1)))
        sz_values_y.avg_90_index = (
                                           sz_values_yy.avg_90_index * 31 +
                                           sz_values_tail.today_index_value -
                                           sz_values_head.today_index_value
                                   ) / 31

        sz_values_tail.load(str(get_next_n_date(date_yest, - 180 + 15)))
        sz_values_head.load(str(get_next_n_date(date_yest, - 180 - 15 - 1)))
        sz_values_y.avg_180_index = (
                                            sz_values_yy.avg_180_index * 31 +
                                            sz_values_tail.today_index_value -
                                            sz_values_head.today_index_value
                                    ) / 31

        sz_values_y.commit()

    cur_30_rate = sz_values_y.today_index_value / sz_values_y.avg_30_index - 1
    cur_90_rate = sz_values_y.today_index_value / sz_values_y.avg_90_index - 1
    cur_180_rate = sz_values_y.today_index_value / sz_values_y.avg_180_index - 1

# -------------------------------------- prepare email content -----------------------------------
    decision = fund_strategy(cur_30_rate, cur_90_rate, cur_180_rate)
    email_title = decision
    email_content = """
yesterday date: %s
-----------------------
-------strategy--------
%s
--------------------------
-------index value--------
yesterday index_value:\t%s
average_30_index_value:\t%s
average_90_index_value:\t%s
average_180_index_value:\t%s
---------------------------------------------
--------increase rate of yesterday from------
30 days ago:\t%s
90 days ago:\t%s
180 days ago:\t%s
--------------------
--------help--------
%s
"""
    email_content = email_content % (
        str(date_yest),
        email_title,
        sz_values_y.today_index_value,
        sz_values_y.avg_30_index,
        sz_values_y.avg_90_index,
        sz_values_y.avg_180_index,
        cur_30_rate * 100, cur_90_rate * 100,
        cur_180_rate * 100,
        fund_config_str,
    )

    emails = ChinaIndexEveryDay()
    emails.load('email')

    # send emails
    for address in emails.email_list:
        send_email(address, email_title, email_content)


