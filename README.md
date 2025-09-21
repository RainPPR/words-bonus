## 词汇整理

让人工智能整理、补充英语词汇积累的工具。

流程是把老师发的 Word 先手动转成 PDF 然后用 API 喂给 Gemini 让他补充输出 Markdown 然后用 PyPandoc 转成 Word。

修改 `.env.example` 为 `.env` 并写入你的 API KEY，在命令行中运行即可。

运行前请确保该目录下可以允许 `pandoc` 命令，程序中没有相关检测，可能会出错。

国内网络环境可能无法使用 Gemini，本工具没有做 OpenAI 风格的 API 的计划，请自行选择更好的网络环境。
