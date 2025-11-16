# -*- coding: utf-8 -*-
"""
生成大纲模块
"""

import os
import re
from config import BOOK_MD_FILE,OUTLINE_FILE, PANDOC_COMMAND,GLOSSARY_FILE,IMAGE_DIR
from glossary import Glossary
import uuid
from time import sleep

class GenerateBook:
    # ---- 字段声明区（纯注释，提升可读性） ----
    # self.outline_lines: list[str]      # 原始大纲
    # self.chapters: list[tuple]         # 解析后的章节数据
    # self.image_counter: int            # 用于生成图片命名
    # self.book_content : str           # 最终书籍内容
    # -----------------------------------
    def __init__(self,api_client_instance):
        """
        初始化生成书籍模块

        Args:
            api_client_instance (AIClient): AI 客户端实例
        """
        self.api_client=api_client_instance

        self.outline_lines = []
        self.chapters=[] 
        self.book_content=""

    def build_markdown(self,output_file=BOOK_MD_FILE,outline_file=OUTLINE_FILE):
        """
        生成书籍 Markdown 文件
        
        Args:
            output_file (str): 输出书籍文件路径
        """
        prompt = f"""

        """
        # 读取大纲文件，将大纲文件的每一行存入outline_lines列表(字符串列表) 
        with open(outline_file, "r", encoding="utf-8") as f:
            outline_lines = f.readlines()
            self.outline_lines=outline_lines

        # 解析大纲，获取章节标题和对应的小节、要点列表
        self.write_outline()

        # 术语对照表
        glossary = Glossary()

        # 循环每个章节，生成正文
        for chapter_title, chapter_outline_lines in self.chapters:
            # print(f"正在生成章节: {chapter_title}")
            chapter_text = self.generate_chapter(chapter_title, chapter_outline_lines)
            self.book_content += f"# {chapter_title}\n\n{chapter_text}\n\n"
            # print(f"✓ 章节生成完成: {chapter_title}") 
            sleep(1)  # 避免请求过快

        # 将最终书籍内容写入 Markdown 文件
        # 在生成的md文档头部加入字体限定，否则pandoc转换为pdf是中文不会正常显示
        with open(BOOK_MD_FILE,"w",encoding="utf-8") as f:
            f.write("""---
                    mainfont: "Microsoft YaHei"
                    cjkmainfont: "Microsoft YaHei"
                    ---
            """)
            f.write(self.book_content)
            print("✓ 已生成 book.md，支持 LaTeX 公式，包含AI生成的真实图片")
            print("可使用 Pandoc 导出 PDF，例如：")
            print("pandoc book.md -o book.pdf --pdf-engine=xelatex")


 
    def write_outline(self):
        """
        获取所有的章节标题和对应的小节以及要点列表
        """
        
        # 用于存放所有解析出来的章节，每个章节会包含：章节标题（string）该章节下面的所有小节、要点要行（list of strings）
        # []是泛型集合，()是元组tuple(可以简单的理解为不可变的列表)
        # 在这个方法中，chapters是一个list，里面的每一项是一个tuple，tuple的第一个元素是章节标题字符串，第二个元素是该章节下的大纲行列表
        # 当我们在循环读取chapter时，我们获取到的每一个item都是一个tuple，包含章节标题和该章节下的大纲行列表
        # 最终chapter的数据结构:
        # 其中"第一章 自然哲学的起源与发展"代表章节标题，后面的列表代表该章节下的小节、要点列表
        # chapters = [
        #     (
        #         "第一章 自然哲学的起源与发展",
        #         [
        #             "### 1.1 自然哲学的定义与范畴",
        #             "- 自然哲学作为古代科学的前身",
        #             "- 自然哲学与形而上学的关系",
        #             "### 1.2 古代文明中的自然哲学萌芽",
        #             "- 古埃及与美索不达米亚的自然观",
        #         ]
        #     ),
        #     (
        #         "第二章 巴拉巴拉……",
        #         [...]
        #     )
        # ]

        chapters = []
        # 记录当前读取的章节标题，只包含一二级标题，也就是# 或 ## 开头的标题
        current_chapter = None
        # 用于收集当前章节下的所有小节、要点等大纲内容。
        chapter_outline_lines = []

        # 逐行读取大纲内容
        for line in self.outline_lines:
            # 通过正则判断当前读取的是一级或二级章节标题：# xxx 或 ## xxx
            if re.match(r"^#{1,2}\s+[^#]", line):
                # 如果之前有章节，先保存，current_chapter不为空说明之前有章节
                if current_chapter is not None:
                    chapters.append((current_chapter, chapter_outline_lines))
                    chapter_outline_lines = []
                    ##print("之前有章节：", current_chapter)
                    ##input("按回车继续...")

                # 获取标题文本
                current_chapter = line.strip().lstrip("#").strip()
                
                ##print("读取章节：", current_chapter)
                ##input("按回车继续...")

            else:
                # 不是# xxx或者 ## xxx 说明是普通大纲行，也就是小标题,### 1.xxx
                chapter_outline_lines.append(line)
                ##print("普通大纲行", line.strip())

        # 保存最后一个章节
        if current_chapter is not None:
            chapters.append((current_chapter, chapter_outline_lines))
        self.chapters = chapters
        # print("解析到的章节数：", len(chapters))
        # for chapters_title,chapter_outline_lines in chapters:
        #     for ol_line in chapter_outline_lines:
        #         print(" 当前章节名称", chapters_title)
        #         print("大纲行内容:", ol_line.strip())
        #         input("按回车继续...")



    def generate_chapter(self,chapter_title,chapter_outline_lines):
        """
        根据章节名称和大纲行列表生成章节正文
        包含 LaTeX 公式
        包含插图占位符
        Args:
            chapter_title (str): 章节标题
            chapter_outline_lines (list): 该章节下的大纲行列表
        """
        outline_text = "".join(chapter_outline_lines)
        prompt = f"""
        请根据章节标题以及大纲内容，生成该章节的详细正文内容，要求学术口吻、逻辑清晰,且内容切合章节标题以及大纲内容。
        章节标题: "{chapter_title}"
        大纲内容: "{outline_text}"

        生成要求：
        1. 每个小节独立成段
        2. 文字专业、学术口吻
        3. 生成的正文内容应包含一个 LaTeX 公式表示复杂的数学公式。
        4. 有数学公式或物理公式直接使用 Pandoc 兼容的格式：行内公式使用 $...$, 块公式使用 $$...$$
        5. 中文、英文文字正常输出
        6. 遇到 LaTeX 命令时使用 Pandoc 支持的命令
        7. 不要使用 \( ... \) 或 \[ ... \)
        8. 为每个小节生成一张示意图的描述（只生成文字说明，不生成图片 URL），格式为：![示意图：描述内容]
        9. 输出直接可用于 Pandoc 转 PDF，无需二次处理
        10.输出格式 Markdown。
        """
        try:
            content = self.api_client.generate_text(prompt, max_tokens=3000)
            glossary = Glossary()
            # 替换术语
            content = glossary.replace_terms(content)
            print(f"生成的正文内容：{content}")
            # 解析文本中的“示意图描述”，生成真实图片 
            content = self.replace_placeholder_with_image(content)
            print(f"替换图片后的正文内容：{content}")
            return content
        except Exception as e:
            print(f"⚠ 章节正文生成失败: {e}")
            return ""

    def replace_placeholder_with_image(self, content):
        """
        遍历文本中的占位符 ![示意图: 描述]
        如果找到占位符，调用 AI 生成图片并替换
        返回处理后的文本
        """
        def repl(match):
            desc = match.group(1)
            print(desc)
            # 生成默认图片文件名
            image_path = f"image_{uuid.uuid4()}.png"
            saved_path = self.api_client.generate_image(desc, image_path)
            print(saved_path)
            if saved_path:
                return f"![{desc}]({saved_path})"
            else:
                return f"![{desc}](#)"  # 失败用占位符

        # 使用正则替换所有占位符
        # return re.sub(r"!\[示意图: (.*?)\]", repl, content)
        return re.sub(r"!\[示意图：(.+?)\]", repl, content, flags=re.DOTALL)
 


