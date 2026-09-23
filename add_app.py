#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全能签软件源管理脚本
用法:
    python3 add_app.py add     --name "应用名" --bundle "com.xxx" --version "1.0" \
                               --ipa "apps/xxx.ipa" --icon "icons/xxx.png" \
                               --minios "15.0" --desc "描述" [--date "2026-09-23"]
    python3 add_app.py list
    python3 add_app.py remove --bundle "com.xxx"
    python3 add_app.py gen

说明:
    --ipa / --icon 填仓库内的相对路径(推荐)或完整 https 链接。
    自动把相对路径换算成 Pages 上的完整直链(https://leiting2327.github.io/qnq-source/...)。
    运行后 appstore.json 自动更新,提交推送即可生效。
"""
import argparse
import json
import os
import sys
from datetime import datetime

BASE = "https://leiting2327.github.io/qnq-source"
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "appstore.json")


def load_manifest():
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return json.load(f)


def save_manifest(data):
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write("\n")


def to_url(p):
    p = p.replace("\\", "/")
    if p.startswith("http://") or p.startswith("https://"):
        return p
    p = p.lstrip("./")
    return BASE + "/" + p


def do_add(args):
    data = load_manifest()
    apps = data.get("apps", [])
    for a in apps:
        if a.get("bundleId") == args.bundle:
            sys.exit(f"错误: bundleId {args.bundle} 已存在,先 remove 再 add")
    date = args.date or datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    entry = {
        "name": args.name,
        "type": "4",
        "version": args.version,
        "versionDate": date,
        "versionDescription": args.desc or "",
        "bundleId": args.bundle,
        "icon": to_url(args.icon) if args.icon else "",
        "downUrl": to_url(args.ipa),
        "minIos": args.minios or "",
    }
    apps.append(entry)
    data["apps"] = apps
    save_manifest(data)
    print(f"已添加: {args.name} ({args.bundle})")
    print(f"  downUrl: {entry['downUrl']}")


def do_list(_):
    data = load_manifest()
    apps = data.get("apps", [])
    if not apps:
        print("当前源内没有应用")
        return
    for a in apps:
        print(f"- {a.get('name')}  v{a.get('version')}  {a.get('bundleId')}")
        print(f"    {a.get('downUrl')}")


def do_remove(args):
    data = load_manifest()
    apps = data.get("apps", [])
    new = [a for a in apps if a.get("bundleId") != args.bundle]
    if len(new) == len(apps):
        sys.exit(f"未找到 bundleId: {args.bundle}")
    data["apps"] = new
    save_manifest(data)
    print(f"已移除: {args.bundle}")


def do_gen(_):
    do_list(_)


def main():
    p = argparse.ArgumentParser(description="全能签软件源管理脚本")
    sub = p.add_subparsers(dest="cmd", required=True)

    pa = sub.add_parser("add", help="添加一个应用")
    pa.add_argument("--name", required=True)
    pa.add_argument("--bundle", required=True)
    pa.add_argument("--version", required=True)
    pa.add_argument("--ipa", required=True)
    pa.add_argument("--icon", default="")
    pa.add_argument("--minios", default="")
    pa.add_argument("--desc", default="")
    pa.add_argument("--date", default="")
    pa.set_defaults(func=do_add)

    pl = sub.add_parser("list", help="列出应用")
    pl.set_defaults(func=do_list)

    pr = sub.add_parser("remove", help="移除应用")
    pr.add_argument("--bundle", required=True)
    pr.set_defaults(func=do_remove)

    pg = sub.add_parser("gen", help="重新生成清单")
    pg.set_defaults(func=do_gen)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
