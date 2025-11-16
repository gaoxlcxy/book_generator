# -*- coding: utf-8 -*-
"""
生成大纲模块
"""

import os
from config import OUTLINE_FILE, PANDOC_COMMAND

"""
大纲的结构如下：

总共有四级菜单，分别是：
# 书籍标题
## 章节标题
### 小节标题
- 要点1
- 要点2

生成正文时，循环所有的章节标题，根据该章节标题以及该章节标题下所有的小节标题以及要点，生成该章节的正文内容。
这么做的好处是避免api多次调用，提升效率。
"""

class GenerateOutline:

    def __init__(self,api_client_instance):
        """
        初始化生成大纲模块

        Args:
            api_client_instance (AIClient): AI 客户端实例
        """
        self.api_client=api_client_instance

    def build_markdown(self,topic,output_file=OUTLINE_FILE):
        """
        生成大纲 Markdown 文件
        
        Args:
            topic (str): 用于生成大纲的提示语
            output_file (str): 输出大纲文件路径
        """
        prompt = f"""
            请根据书籍主题：“{topic}“生成一个专业书籍的大纲。
            生成的大纲应符合以下要求：
            1.结构为三层结构（章节->小节->要点）
            2.学术口吻、逻辑清晰。
            3.章节数量要求为最少两个章节，最多为两个章节。
            4.每个章节下包含2个小节，每个小节下包含2个要点。
            5.输出格式 Markdown，以下是示例格式：
            # 书籍主题
            # 章节标题
            ## 小节标题
            - 要点1
            - 要点2 
        """
        outline_text = self.api_client.generate_text(prompt, max_tokens=1000)
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(outline_text)
        
        print(f"✓ 已生成大纲文件: {output_file}")

