

## 💼 项目展示：智能生成书籍服务

这是一个基于 ChatGPT 的 生成书籍服务，用户可以输入主题来自动生成一本书籍并转换成PDF文件。

- 项目语言：Python + OpenAI 接口
- 中间件：PanDoc（转换PDF功能） 、 KaTeX（数学公式渲染引擎）
- 功能：通过文本描述生成一本完整的书籍并转换为PDF文件


🔗 **项目源码：** [GitHub 仓库地址](https://github.com/gaoxlcxy/book_generator.git)


--

## 💼项目结构

book_generator/
│
├── images/             # AI 生成图片存放
├── config.py           # 配置文件，API Key、文件路径等
├── glossary.py         # 术语替换
├── ai_client.py        # AI 调用接口封装
├── generate_book.py    # 书籍生成
├── generate_outline.py # 书籍目录结构生成
├── markdown_to_pdf.py  # MarkDown转换pdf
└── main.py             # 程序入口，控制流程



--- 
