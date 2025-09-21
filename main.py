import os
import pypandoc
from dotenv import load_dotenv
import tkinter as tk
from tkinter import filedialog

import pathlib
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

def generate_text(pdf_path: str) -> str:
    pdf_file = pathlib.Path(pdf_path)
    system_prompt = pathlib.Path("prompt.txt").read_text(encoding="utf-8")
    response = client.models.generate_content_stream(
        model="gemini-2.5-pro",
        contents=[
            types.Part.from_bytes(
                data=pdf_file.read_bytes(),
                mime_type='application/pdf',
            ),
            "帮我整理，谢谢！"
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            thinking_config=types.ThinkingConfig(
                thinking_budget=32768,
                include_thoughts=True
            )
        ),
    )

    thoughts = ""
    answer = ""

    for chunk in response:
        for part in chunk.candidates[0].content.parts:
            if not part.text:
                continue
            elif part.thought:
                if not thoughts:
                    print("思考总结：")
                    print('--------------------')
                print(part.text)
                thoughts += part.text
            else:
                if not answer:
                    print('--------------------')
                print('part:', len(part.text), 'total:', len(answer))
                answer += part.text

    print("\n")
    return answer

def write_docx(pdf_path: str, save_path: str):
    markdown_output = generate_text(pdf_path)
    pathlib.Path("output.md").write_text(markdown_output, encoding="utf-8")

    print(f"正在将 Markdown 转换为 DOCX 并保存到: {save_path}")

    pypandoc.convert_text(
        markdown_output,
        'docx',
        format='md',
        outputfile=save_path,
        encoding='utf-8'
    )

    print(f"文件已成功保存到: {save_path}")

def main():
    root = tk.Tk()
    root.withdraw()

    pdf_path = filedialog.askopenfilename(
        title="请选择一个 PDF 文件进行分析",
        filetypes=[("PDF Files", "*.pdf")]
    )
    
    if not pdf_path:
        print("用户取消了文件选择，程序退出。")
        return
    
    print(f"已选择文件: {pdf_path}")

    base_name = os.path.basename(pdf_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    default_save_name = f"{file_name_without_ext}.docx"

    save_path = filedialog.asksaveasfilename(
        title="请选择保存位置",
        initialfile=default_save_name,
        defaultextension=".docx",
        filetypes=[("Word Document", "*.docx")]
    )

    if not save_path:
        print("取消保存，程序退出。")
        return
    
    write_docx(pdf_path, save_path)

if __name__ == "__main__":
    main()
