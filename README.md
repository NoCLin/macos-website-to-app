# macOS 上快速将网站打包为桌面app (基于Chrome, 不含图标app大小<1KB)

## 为什么不使用 Nativefier ？

Electron 太大。

## 为什么点击图标一闪而过，不能点击图标回到页面？

~~本想使用 系统API记录打开的窗口句柄，但是对于每个独立的app都需要开启辅助访问授权，太复杂~~

TODO: 使用管道通信 只需要给maker授权一次

[ ] 打开网站后 保留dock
[ ] 点击dock时，用applescript控制chrome切换回窗口 (完毕)
[ ] 监控窗口列表，关闭时退出dock
