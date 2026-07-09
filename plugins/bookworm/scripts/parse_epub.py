#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPUB 解析脚本 — 将 EPUB 电子书转为纯文本。

仅使用 Python 标准库（zipfile + xml），零 pip 依赖，跨平台。
用法：
    python parse_epub.py <epub路径> <输出txt路径>

EPUB 本质是 zip 包，内含 spine 顺序排列的 XHTML 文件。
本脚本按 spine 顺序提取各章文本并拼接为纯文本输出。
"""

import sys
import os
import zipfile
import xml.etree.ElementTree as ET
import re
from html.parser import HTMLParser


# EPUB XHTML 的命名空间
NS = {
    "container": "urn:oasis:names:tc:opendocument:xmlns:container",
    "opf": "http://www.idpf.org/2007/opf",
    "xhtml": "http://www.w3.org/1999/xhtml",
}


class TextExtractor(HTMLParser):
    """从 HTML/XHTML 中提取纯文本，保留块级元素换行。"""

    BLOCK_TAGS = {
        "p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6",
        "li", "tr", "section", "article", "header", "footer",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip = True
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = False
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    def get_text(self):
        text = "".join(self.parts)
        # 合并多余空行
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def find_opf_path(zf):
    """从 META-INF/container.xml 中定位 OPF 文件路径。"""
    try:
        with zf.open("META-INF/container.xml") as f:
            tree = ET.parse(f)
        root = tree.getroot()
        rootfile = root.find(".//container:rootfile", NS)
        if rootfile is None:
            # 退回无命名空间查找
            rootfile = root.find(".//{*}rootfile")
        if rootfile is None:
            raise RuntimeError("container.xml 中未找到 rootfile")
        return rootfile.get("full-path")
    except KeyError:
        raise RuntimeError("EPUB 缺少 META-INF/container.xml，可能不是标准 EPUB")


def get_spine_order(opf_root, opf_dir):
    """按 spine 顺序返回 manifest 中文档项的 href 列表。"""
    manifest = {}
    for item in opf_root.findall(".//opf:item", NS):
        item_id = item.get("id")
        href = item.get("href")
        media_type = item.get("media-type", "")
        if item_id and href:
            manifest[item_id] = (href, media_type)

    spine = opf_root.find(".//opf:spine", NS)
    if spine is None:
        spine = opf_root.find(".//{*}spine")
    if spine is None:
        raise RuntimeError("OPF 中未找到 spine")

    ordered = []
    for itemref in spine.findall(".//{*}itemref"):
        idref = itemref.get("idref")
        if idref and idref in manifest:
            href, media_type = manifest[idref]
            # 只取 XHTML/HTML 文档，跳过图片、样式、封面等
            if "html" in media_type or "xml" in media_type or href.endswith((".html", ".xhtml", ".htm")):
                ordered.append(href)
    return ordered, manifest


def read_xhtml_text(zf, opf_dir, href):
    """读取并解析单个 XHTML 文件为纯文本。"""
    full_path = href if os.path.isabs(href) else os.path.normpath(os.path.join(opf_dir, href))
    # Windows 路径分隔符统一为正斜杠（zip 内部用正斜杠）
    full_path = full_path.replace("\\", "/")
    try:
        with zf.open(full_path) as f:
            content = f.read().decode("utf-8", errors="replace")
    except KeyError:
        # 尝试大小写不敏感查找
        names = zf.namelist()
        lower_map = {n.lower(): n for n in names}
        actual = lower_map.get(full_path.lower())
        if not actual:
            return ""
        with zf.open(actual) as f:
            content = f.read().decode("utf-8", errors="replace")

    extractor = TextExtractor()
    extractor.feed(content)
    return extractor.get_text()


def parse_epub(epub_path, output_path):
    if not os.path.exists(epub_path):
        print(f"错误：找不到文件 {epub_path}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(epub_path, "r") as zf:
        opf_path = find_opf_path(zf)
        opf_dir = os.path.dirname(opf_path)
        with zf.open(opf_path) as f:
            opf_root = ET.parse(f).getroot()

        spine_order, manifest = get_spine_order(opf_root, opf_dir)
        if not spine_order:
            raise RuntimeError("未在 spine 中找到任何 XHTML 文档")

        all_text = []
        for href in spine_order:
            chapter_text = read_xhtml_text(zf, opf_dir, href)
            if chapter_text:
                all_text.append(chapter_text)

        full_text = "\n\n".join(all_text)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    print(f"解析完成：{epub_path} -> {output_path}")
    print(f"共 {len(spine_order)} 个文档段，{len(full_text)} 字符")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python parse_epub.py <epub路径> <输出txt路径>", file=sys.stderr)
        sys.exit(1)
    sys.exit(parse_epub(sys.argv[1], sys.argv[2]))
