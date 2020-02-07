# !/usr/bin/python
# coding: utf-8
import logging
import timeit
from subprocess import Popen, PIPE


def log_func(func):
    def wrapper(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        arg_str = ', '.join(repr(arg) for arg in args)

        logging.info('[%0.8fs] %s (%s)==%s' % (elapsed, func.__name__,arg_str, result))
        return result

    return wrapper


def applescript_call(src):

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(src)
    if len(stderr) > 0:
        logging.error("apple script src:\n%s\n" % src)
        logging.error("apple script error:\n%s\n" % stderr)
        raise Exception(stderr)
    print(stdout)
    # logging.debug("result:\n%s\n" % stdout)
    return stdout.rstrip("\n")


@log_func
def get_window_id_list():
    text = applescript_call(r"""
        	tell application "Google Chrome"
        		set window_number to 0
        		set list_text to ""
        		repeat with window_obj in windows
        			set list_text to list_text & (id of window_obj as text) & " "
        		end repeat
        		return list_text
        	end tell
        """)
    text = text.strip()
    if text == "":
        return []
    return list(map(int, text.split(" ")))


@log_func
def bring_window_to_front_by_id(_id):
    applescript_call(r"""
	tell application "Google Chrome"
	set window_number to 0
	repeat with window_obj in windows
		set window_number to window_number + 1
		if %d is id of window_obj then
			# https://stackoverflow.com/questions/10366003/applescript-google-chrome-activate-a-certain-window/16727145#16727145
			# changing the index raises the window, but for example keyboard shortcuts are still registered by the previously frontmost window.
			window_number
			set index of window window_number to 1
			activate
			exit repeat
		end if
		
	end repeat
	
end tell
        """ % _id)
    # applescript_call(r"""
    #     tell application "Google Chrome"
    #         set window_number to 0
    #         repeat with window_obj in windows
    #             set window_number to window_number + 1
    #             if %d is id of window_obj then
    #                 tell application "System Events" to tell process "Google Chrome"
    #                     perform action "AXRaise" of window window_number
    #                     set frontmost to true
    #                 end tell
    #                 exit repeat
    #             end if
    #
    #         end repeat
    #
    #     end tell
    #         """ % _id)


@log_func
def get_windows():
    csv_text = applescript_call(r"""
    on GetChromeWindowListCSV()
    	tell application "Google Chrome"
    		set window_number to 0
    		set csv_text to "id,number,title
"

    		repeat with window_obj in windows
    			set window_number to window_number + 1
    			set csv_text to csv_text & (id of window_obj as text) & "," & window_number & ",\"" & title of window_obj & "\"
"
    		end repeat

    		return csv_text
    	end tell
    end GetChromeWindowListCSV
    GetChromeWindowListCSV()
    """)
    # print(csv_text)
    import csv, io
    csv_f = io.StringIO(csv_text)
    reader = csv.DictReader(csv_f)
    result = []
    for row in reader:
        result.append({
            "title": row["title"].strip(),
            "id": int(row["id"].strip()),
            "number": int(row["number"].strip()),
        })
    csv_f.close()
    return result
