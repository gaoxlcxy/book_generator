# -*- coding: utf-8 -*-
"""
AI 接口调用模块
封装文本生成和图片生成
包含python语法解释，以便理解python的语法
"""

import requests
from openai import OpenAI
# OpenAI的相关配置
from config import API_BASE_URL, API_KEY, IMAGE_DIR
import os

class AIClient:
    """
    OpenAI相关操作
    """
    #构造函数，可以理解为C#的public AI_Client(){} ,self等于C#里的this
    def __init__(self):
        """
        初始化 OpenAI / Nuwa 客户端
        """
        #python不需要预先写字段声明，所以这个self.client等于C#的this.client
        self.client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY
        )

    def generate_text(self, prompt, max_tokens=1500, temperature=0.2):
        """
        根据 prompt 生成文本内容

        Args:
            prompt (str): 用户输入的提示词
            max_tokens (int): 最大返回长度
            temperature (float): 随机程度

        Returns:
            str: 生成的文本内容
        """
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4.1-mini",#gpt大模型类别
                messages=[{"role": "user", "content": prompt}],#构建gpt对话
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"⚠ 文本生成失败: {e}")
            return ""

    def generate_image(self, prompt, filename):
        """
        根据描述生成图片并保存到指定文件名
        返回图片保存路径，如果失败返回 None
        Args:
            prompt (str): 图片描述文本
            filename (str): 保存图片的文件名
        """
        ##return "https://oaidalleapiprodscus.blob.core.windows.net/private/org-0bgNtRmQOkeNVWKH6a7cXcCi/user-lWyiHCzMyXynSTpcBEK56lka/img-o6cnrp2KqAmfcRJ2kCkQ1Tgl.png?st=2025-11-16T07%3A46%3A24Z&se=2025-11-16T09%3A46%3A24Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=ed3ea2f9-5e38-44be-9a1b-7c1e65e4d54f&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-16T04%3A59%3A38Z&ske=2025-11-17T04%3A59%3A38Z&sks=b&skv=2024-08-04&sig=ktmtU%2B/QsbuydyhNfEqCrbCAGUjgLBvM6/cLAMrLJio%3D"
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                response_format="url",
                n = 1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            print(f"图片生成成功，URL: {image_url}")
            os.makedirs(IMAGE_DIR, exist_ok=True)
            save_path = os.path.join(IMAGE_DIR, filename)
            print("filename:",filename)
            print("save_path:",save_path)
            r = requests.get(image_url)
            with open(save_path, "wb") as f:
                f.write(r.content)
            return save_path
        except Exception as e:
            print(f"⚠ 图片生成失败: {prompt}, 错误: {str(e)}")
            return None
