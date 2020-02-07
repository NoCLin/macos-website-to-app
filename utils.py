import shutil
import subprocess
from pathlib import Path

from PIL import Image


def ico2png(ico_file):
    tmp_png = "tmp.png"
    Image.open(ico_file).save(tmp_png)
    return tmp_png


def png2icns(png_file):
    iconset = "tmp_icons.iconset"
    if Path(iconset).is_dir():
        shutil.rmtree(str(Path(iconset)))

    Path(iconset).mkdir(exist_ok=True)

    #
    # # TODO: 转 png
    #
    for i in """
    sips -z 16 16     {png} --out {iconset}/icon_16x16.png
    sips -z 32 32     {png} --out {iconset}/icon_16x16@2x.png
    sips -z 32 32     {png} --out {iconset}/icon_32x32.png
    sips -z 64 64     {png} --out {iconset}/icon_32x32@2x.png
    sips -z 128 128   {png} --out {iconset}/icon_128x128.png
    sips -z 256 256   {png} --out {iconset}/icon_128x128@2x.png
    sips -z 256 256   {png} --out {iconset}/icon_256x256.png
    sips -z 512 512   {png} --out {iconset}/icon_256x256@2x.png
    sips -z 512 512   {png} --out {iconset}/icon_512x512.png""".strip().splitlines():
        i = i.strip().format(png=png_file, iconset=iconset)
        print(i)
        status, output = subprocess.getstatusoutput(i)
        print(status,output)
        print()

    icns = "icon.icns"
    cmd = "iconutil -c icns {iconset} -o {icns}".format(iconset=iconset, icns=icns)
    print(cmd)
    status, output = subprocess.getstatusoutput(cmd)
    print(output)
    return icns
