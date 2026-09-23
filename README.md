# 全能签自建软件源 (qnq-source)

在 GitHub Pages 上免费托管的「全能签」软件源。全站 HTTPS,满足全能签读取要求。

## 源地址
```
https://leiting2327.github.io/qnq-source/appstore.json
```
在全能签 → 资源 → 软件源 → 添加第三方源,粘贴上面链接即可。

## 目录结构
```
qnq-source/
├── appstore.json      # 源清单(核心)
├── add_app.py         # 管理脚本: 添加/移除/列出应用
├── apps/              # 放 IPA 文件
├── icons/             # 放应用图标 (png)
└── README.md
```

## 添加一个应用(推荐用脚本)
把 `xxx.ipa` 放进 `apps/`,图标 `xxx.png` 放进 `icons/`,然后:
```bash
python3 add_app.py add \
  --name "我的应用" \
  --bundle "com.your.app" \
  --version "1.0" \
  --ipa "apps/xxx.ipa" \
  --icon "icons/xxx.png" \
  --minios "15.0" \
  --desc "更新说明"
```
脚本会自动把相对路径换算成 Pages 完整直链并写入 `appstore.json`。提交推送后刷新源即可看到。

其他命令:
```bash
python3 add_app.py list                 # 查看应用
python3 add_app.py remove --bundle com.your.app   # 移除应用
```

## 手动编辑清单
不装 Python 也可以直接改 `appstore.json`,每个应用一条记录:
```json
{
    "name": "我的应用",
    "type": "4",
    "version": "1.0",
    "versionDate": "2026-09-23T12:00:00+08:00",
    "versionDescription": "更新说明",
    "bundleId": "com.your.app",
    "icon": "https://leiting2327.github.io/qnq-source/icons/xxx.png",
    "downUrl": "https://leiting2327.github.io/qnq-source/apps/xxx.ipa",
    "minIos": "15.0"
}
```
> 编码必须是 UTF-8;改完可用 https://jsonlint.com 校验,不能有多余逗号。

## 注意
- **IPA 必须是 HTTPS 直链**,不能是网盘/跳转页链接。
- 单个文件超过 100MB 无法推到 GitHub,大 IPA 请改用 Vercel / 对象存储托管,再把直链填进 `downUrl`。
- 源只是 IPA 下载清单,签名由全能签 App 本地完成;需要你自己导入证书。
- **只放你自己开发、拥有版权的 IPA**,不要分发破解、盗版、多开外挂类应用,有法律风险。

## 发布更新
改完文件后本地提交并推送即可,Pages 自动更新:
```bash
git add -A
git commit -m "update source"
git push origin main
```
