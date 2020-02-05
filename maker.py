#!/usr/bin/env python3
# coding: utf-8
import re
import shutil
import string
import sys
from pathlib import Path

import requests
from fire import Fire


def ico2png(ico_file):
    # TODO: pillow
    return "result.png"


def png2icns(png_file):
    # os.system("rm -rf icons.iconset/*")
    #
    # # TODO: 转 png
    #
    # for i in """
    #     sips -z 16 16     icon.png --out icons.iconset/icon_16x16.png
    # sips -z 32 32     icon.png --out icons.iconset/icon_16x16@2x.png
    # sips -z 32 32     icon.png --out icons.iconset/icon_32x32.png
    # sips -z 64 64     icon.png --out icons.iconset/icon_32x32@2x.png
    # sips -z 128 128   icon.png --out icons.iconset/icon_128x128.png
    # sips -z 256 256   icon.png --out icons.iconset/icon_128x128@2x.png
    # sips -z 256 256   icon.png --out icons.iconset/icon_256x256.png
    # sips -z 512 512   icon.png --out icons.iconset/icon_256x256@2x.png
    # sips -z 512 512   icon.png --out icons.iconset/icon_512x512.png""".strip().splitlines():
    #     status, output = subprocess.getstatusoutput(i)
    #
    # status, output = subprocess.getstatusoutput("iconutil -c icns icons.iconset -o icon.icns")

    return "result.icns"


def make(url, title=None, args="", icon=None, ):
    """
    生成可直接在Chrome以app模式打开网址的 macOS app
    :param url: 网址
    :param title: 标题，可空，默认从网址的Title标签抓取
    :param args: Chrome额外启动参数，可空
    :param icon: 自定义图标文件，可空，默认从网址favicon抓取
    :return:
    """
    # TODO: 添加隐身模式选项
    from urllib.parse import urlparse
    url_parsed = urlparse(url)

    if title is None:

        content = requests.get(url).content.decode()
        pattern = '<title>([\S\s]*?)<\/title>'
        titles = re.findall(pattern, content, re.S)
        if len(titles):
            title = titles[0].replace("\n", "")  # TODO: 过滤
        else:
            title = url_parsed.netloc
    print("title", title)
    dest = Path("apps") / (title + ".app")
    base_app = Path("resources") / "base.app"

    args = '--app=%s %s' % (url, args)

    if Path(dest).is_dir():
        shutil.rmtree(dest)

    shutil.copytree(str(base_app), dest)

    plist_src = base_app / "Contents" / "Info.plist"
    plist = dest / "Contents" / "Info.plist"
    runner = dest / "Contents" / "MacOS" / "runner"
    icon_dest = dest / "Contents" / "Resources" / "icon.icns"

    with open(str(plist_src), "rt", encoding="utf-8") as f:
        content = f.read()
        with open(str(plist), "wt", encoding="utf-8") as fw:
            content = string.Template(content).safe_substitute({
                "CFBundleName": title,
                "CFBundleIdentifier": "com.test.id." + title,
                "CFBundleDisplayName": title
            })
            fw.write(content)

    runner_content = """#!/bin/sh
open --wait-apps --new -b com.google.Chrome --args {args}
"""

    if icon is None:
        # icon_url = "%s://%s/favicon.ico" % (url_parsed.scheme, url_parsed.netloc)
        # r = requests.get(icon_url)
        # ico_file = "tmp_icon.ico"
        # with open(ico_file, "wb") as f:
        #     f.write(r.content)
        # png_file = ico2png(ico_file)
        # icon = png2icns(ico_file)

        # TODO: 图标格式转换 ico->png->icns
        icon = "resources/default.icns"
        shutil.copy(icon, str(icon_dest))
    runner_content = runner_content.format(args=args)
    print(runner_content)
    with open(str(runner), "wt", encoding="utf-8") as f:
        f.write(runner_content)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append("--help")
    Fire(make)
