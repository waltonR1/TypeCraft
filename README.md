# TypeCraft

TypeCraft 是一款专为 Notion、Obsidain 等现代编辑器设计的**真人模拟打字工具**。它不仅能模拟人类的打字速度、抖动和错误，还能智能识别 Markdown 结构，并根据编辑器的自动补全行为进行自动化交互。

## 核心特性

- **真人行为模拟**：
  - 动态字符延迟与随机抖动。
  - 智能标点符号与句末停顿。
  - 模拟输入错误并自动退格修正。
- **Markdown 智能识别**：
  - **代码块隔离**：进入代码块后自动切换到字面量输入模式，防止 Markdown 语法干扰。
  - **表格转换**：支持将 Markdown 表格自动转换为编辑器中的真实表格，并自定义单元格跳转脚本。
  - **列表续行**：自动处理项目符号、数字列表和引用块的换行逻辑。
- **编辑器适配**：
  - **自动补全处理**：智能跳过编辑器自动生成的括号 `()`、引号 `""`、大括号 `{}` 等。
  - **macOS 优化**：针对 macOS 双击空格变句号的问题进行了专门的延迟保护。
- **自定义脚本系统**：
  - 支持录制和自定义复杂的按键序列（如 `tab`、`cmd+enter`、`delay:0.5`）。
  - 内置可视化按键录制器。

## 项目结构

```text
TypeCraft/
├── main.py                # 程序入口
├── core/
│   ├── engine.py          # 打字引擎状态机
│   ├── processor.py       # 文本解析引擎
│   ├── keyboard_manager.py# 键盘驱动与脚本解析
│   └── handlers/          # 打字逻辑拆分
│       ├── character_handler.py # 字符输入逻辑
│       ├── table_handler.py     # 表格逻辑
│       └── line_handler.py      # 换行逻辑
├── ui/
│   ├── app.py             # UI 主框架
│   ├── dialogs/           # 录制弹窗
│   └── tabs/              # 功能选项卡 (输入/设置/Markdown/日志)
└── utils/
    ├── constants.py       # 全局常量
    └── os_helper.py       # OS 识别工具
```

## 快速开始

1. **环境准备**：
   确保已安装 Python 3.8+ 并安装依赖：
   ```bash
   pip install pynput
   ```

2. **运行程序**：
   ```bash
   python main.py
   ```

3. **使用流程**：
   - 在“输入文本”页粘贴 Markdown 内容。
   - 在“打字设置”页调整模拟参数。
   - 在“Markdown/表格”页配置目标编辑器的自动行为和按键脚本。
   - 点击“开始执行”，并在 5 秒内切换到你的目标编辑器窗口。

## 开发调试

本项目采用了高度模块化的设计，方便开发者自行扩展：
- 如果需要修改打字时的符号跳过逻辑，请查看 `core/handlers/character_handler.py`。
- 如果需要调整代码块的识别方式，请查看 `core/engine.py` 中的状态机部分。
- UI 的各个部分已拆分至 `ui/tabs/` 目录下。

## 许可证

MIT License
