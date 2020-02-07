# macOS 上快速将网站打包为桌面app (基于Chrome, 不含图标app大小<1KB)

## 为什么不使用 Nativefier ？

Electron 太大。

## 为什么点击图标一闪而过，不能点击图标回到页面？

~~本想使用 系统API记录打开的窗口句柄，但是对于每个独立的app都需要开启辅助访问授权，太复杂~~

~~TODO: 使用管道通信 只需要给maker授权一次~~


~~1.[x] 打开网站后 保留dock  (oc编译体积小,swift/qt库大, c++ 调用cocoa等API太复杂)~~
~~2.[x] 点击dock时，用applescript控制chrome切换回窗口 (完毕)~~
~~3.[x] 监控窗口列表，关闭时退出dock~~
~~4.[x] 因为Launcher需要写死路径，需要在固定位置创建替身~~
```shell script
osascript -e 'tell application "Finder" to make alias file to POSIX file src at POSIX file dest'
```

~~[ ] 通过socket/http/管道通信 (不能让Launcher启动Maker，不然Launcher要授权，权限面还有些问题)~~


**太复杂了**，而且速度慢体验不好

目前的版本直接用python作为启动文件，不常驻dock(但可以将图标放在dock，初次启动打开窗口，再次启动打开上次窗口)

但是每个app需要独立授权

TODO: debug

[ ]每个webapp的窗口id文件需要独立