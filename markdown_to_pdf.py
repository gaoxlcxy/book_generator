import os
import subprocess

class MarkdownToPDF:
    
    def __init__(self,markdown_file,pdf_file=None,pdf_engine="xelatex"):
        """
        初始化方法
        :param markdown_file: 要转换的 Markdown 文件路径
        :param pdf_file: 输出的 PDF 文件路径，如果为空，则默认与 Markdown 同名
        :param pdf_engine: 使用的 PDF 引擎，默认 xelatex
        """
        self.markdown_file = markdown_file
        if pdf_file:
            self.pdf_file = pdf_file
        else:
            # 默认 PDF 文件名和 Markdown 同名，只是扩展名改为 .pdf
            self.pdf_file = os.path.splitext(markdown_file)[0] + ".pdf"
        self.pdf_engine = pdf_engine

    def convert(self):
        """
        执行转换操作
        """
        if not os.path.exists(self.markdown_file):
            raise FileNotFoundError(f"Markdown 文件不存在: {self.markdown_file}")

        # 构造 Pandoc 命令
        # 示例命令：pandoc book.md -o book.pdf --pdf-engine=xelatex
        cmd = [
            "pandoc",
            self.markdown_file,
            "-o",
            self.pdf_file,
            f"--pdf-engine={self.pdf_engine}"
        ]

        try:
            # 使用 subprocess 执行命令
            subprocess.run(cmd, check=True)
            print(f"✓ 成功生成 PDF: {self.pdf_file}")
            return self.pdf_file
        except subprocess.CalledProcessError as e:
            print(f"⚠ PDF 生成失败: {e}")
            return None
