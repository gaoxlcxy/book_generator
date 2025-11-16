# -*- coding: utf-8 -*-
"""
程序主入口
"""
 
from ai_client import AIClient 
from generate_book import GenerateBook
from generate_outline import GenerateOutline
from markdown_to_pdf import MarkdownToPDF
from config import BOOK_MD_FILE, PANDOC_COMMAND

def main():
    # 1️⃣ 初始化模块
    ai_client = AIClient()
    inputStr = ""
    inputStr = input("请选择操作类型（1-生成大纲，2-根据大纲生成书籍正文，3-将正文转换为pdf文件）：")
    match inputStr:
        case "1":
            strTopic = input("请输入书籍主题: ")
            generate_outline = GenerateOutline(ai_client)
            generate_outline.build_markdown(strTopic)
        case "2":
            generate_book = GenerateBook(ai_client)
            generate_book.build_markdown()
        case "3":
            markdown_to_pdf = MarkdownToPDF(BOOK_MD_FILE)
            markdown_to_pdf.convert()
        case _:
            print("无效的操作类型，请输入1、2或3。")
     
if __name__ == "__main__":
    main()
