# -*- coding: utf-8 -*-
"""
配置文件
存放 API Key、文件路径等全局配置
"""

# OpenAI / Nuwa API 配置
API_BASE_URL = "https://api.nuwaapi.com/v1"
API_KEY = "sk-K0voLfbmeOFkR7T4PEyY0fhO03ImuBjOobzNbm2I1N3Sxj6K"

# 输入输出文件路径
OUTLINE_FILE = "outline.md"  # 大纲文件
GLOSSARY_FILE = "glossary.txt"  # 术语表
BOOK_MD_FILE = "book.md"     # 输出 Markdown 文件
IMAGE_DIR = "images"         # 存放生成图片的文件夹

#输出中文字体（需要系统中已安装）
CHINESE_FONT = "Microsoft YaHei"  
LATEX_ENGINE = "xelatex"  # XeLaTeX 支持中文

# Pandoc 转 PDF 的默认命令
PANDOC_COMMAND = "pandoc book.md -o book.pdf --pdf-engine=xelatex"
