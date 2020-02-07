#!/usr/bin/env python3
# coding: utf-8
# coding: utf-8
import os
import re
import shutil
import string
import sys
import traceback
from pathlib import Path
from urllib.parse import urlparse

import requests
from fire import Fire

from utils import ico2png, png2icns


def make(url, title=None, additional_args="", icon=None, enable_assistance=False):
    """
    生成可直接在Chrome以app模式打开网址的 macOS app
    :param url: 网址
    :param title: 标题，可空，默认从网址的Title标签抓取
    :param args: Chrome额外启动参数，可空
    :param icon: 自定义图标文件，可空，默认从网址favicon抓取
    :return:
    """
    # TODO: 添加隐身模式选项

    url_parsed = urlparse(url)

    if title is None:
        print("从%s获取标题" % url)
        try:
            content = requests.get(url).content.decode()
            pattern = '<title>([\S\s]*?)<\/title>'
            titles = re.findall(pattern, content, re.S)
            if len(titles):
                title = titles[0].replace("\n", "")  # TODO: 过滤
                print("获取标题成功，使用%s作为标题。" % title)
            else:
                raise Exception("正则获取标题失败。")
        except Exception as e:
            print(e)
            title = url_parsed.netloc
            print("获取标题失败，使用域名%s作为标题。" % title)

    dest_app = Path("apps") / (title + ".app")

    if enable_assistance:
        base_app = Path("resources") / "base_assistance.app"
    else:
        base_app = Path("resources") / "base.app"
    print("模板app路径", base_app.absolute())
    print("生成app路径", dest_app.absolute())

    print("Chrome参数", dest_app.absolute())

    if Path(dest_app).is_dir():
        shutil.rmtree(dest_app)
        print("删除原先生成的app")

    shutil.copytree(str(base_app), dest_app)

    plist_src = base_app / "Contents" / "Info.plist"
    plist = dest_app / "Contents" / "Info.plist"

    icon_dest = dest_app / "Contents" / "Resources" / "icon.icns"

    with open(str(plist_src), "rt", encoding="utf-8") as f:
        content = f.read()
        with open(str(plist), "wt", encoding="utf-8") as fw:
            content = string.Template(content).safe_substitute({
                "CFBundleName": title,
                "CFBundleIdentifier": "com.test.id." + title,
                "CFBundleDisplayName": title
            })
            fw.write(content)

    if icon is None:

        icon_url = "%s://%s/favicon.ico" % (url_parsed.scheme, url_parsed.netloc)
        print("未提供图标，从%s下载" % icon_url)
        try:
            r = requests.get(icon_url)
            ico_file = "tmp_icon.ico"
            with open(ico_file, "wb") as f:
                f.write(r.content)
            png_file = ico2png(ico_file)
            print("生成的png",png_file)
            icns = png2icns(png_file)
            print("生成的icns", icns)
        except Exception as e:
            print("创建图标时出错，使用默认图标")
            print(traceback.format_exc())
            print(e)
            icns = "resources/default.icns"

        else:
            pass

        # TODO: 图标格式转换 ico->png->icns

        shutil.copy(icns, str(icon_dest))

    if enable_assistance:
        runner = dest_app / "Contents" / "MacOS" / "runner.py"
    else:
        runner = dest_app / "Contents" / "MacOS" / "runner"

    chrome_args = '--app=%s %s' % (url, additional_args)
    chrome_run_command = """open --wait-apps --new -b com.google.Chrome --args %s""" % chrome_args

    with open(str(runner), "rt", encoding="utf-8") as f:
        runner_content = f.read()
        runner_content = runner_content.replace("$RUN_COMMAND$", chrome_run_command)

        with open(str(runner), "wt", encoding="utf-8") as fw:
            fw.write(runner_content)
    print(str(dest_app.absolute()))
    os.system('open --reveal "%s"' % str(dest_app))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    Fire(make)
