# -*- coding: utf-8 -*-
"""
术语处理模块
用于替换文中专业术语
"""

import os
import re
from config import GLOSSARY_FILE

class Glossary:
    def __init__(self, file_path=GLOSSARY_FILE):
        """
        初始化，读取术语表
        术语表格式：原词 => 替换词
        """
        # 用于存放术语对照表（字典）item: {key: 人工智能,value: AI}
        self.terms = {}
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "=>" in line:
                        k, v = line.strip().split("=>")
                        self.terms[k.strip()] = v.strip()

    def replace_terms(self, text):
        """
        替换文本中的术语,如果输入的文本中包含术语表中的key，则替换为对应的value
        Args:
            text (str): 输入文本
        """
        print("正在替换术语...")
        for k, v in self.terms.items():
            text = re.sub(rf"\b{k}\b", v, text)
        return text
