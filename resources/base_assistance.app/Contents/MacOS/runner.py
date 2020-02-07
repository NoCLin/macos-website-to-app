#!/usr/bin/env python
# coding: utf-8
import logging
import os
import sys
import time
import traceback

from apple_script import get_window_id_list, bring_window_to_front_by_id

log_format = '[%(asctime)s][%(thread)d][%(filename)s][L: %(lineno)d][%(levelname)s]  %(message)s'

logging.basicConfig(
    format=log_format,
    level=logging.DEBUG,
    datefmt='%Y%m-%d %H:%M',
    filename="/tmp/webapp_maker.log",
    filemode='a+')

def main():
    last_id = None
    try:
        with open("/tmp/webapp_maker_last_win_id", "rt") as f:
            last_id = int(f.read())
    except:
        pass
    logging.info("last_id %s" % last_id)
    window_id_list = get_window_id_list()
    logging.info("window_id_list %s" % window_id_list)

    if len([i for i in window_id_list if i == last_id]):
        logging.info("show")
        bring_window_to_front_by_id(last_id)
    else:
        logging.info("run")
        run_command = """$RUN_COMMAND$"""

        win_id = None

        win_id_list_1 = get_window_id_list()
        logging.info("win_id_list_1 %s" % win_id_list_1)

        os.system(run_command)

        for i in range(100):
            time.sleep(0.1)
            win_id_list_2 = get_window_id_list()
            logging.info("win_id_list_2 %s" % win_id_list_2)
            if len(win_id_list_1) + 1 == len(win_id_list_2):
                diff_id = [_id for _id in win_id_list_2 if _id not in win_id_list_1]

                if len(diff_id) == 1:
                    win_id = diff_id[0]
                    logging.info("window locked")
                    logging.info(win_id)

                    with open("/tmp/webapp_maker_last_win_id", "wt") as f:
                        f.write(str(win_id))

                    print(win_id)
                    break

        if not win_id:
            print("error")
            sys.exit()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())


