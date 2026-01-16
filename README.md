# pack-folder-tool
Merge a folder snapshot into one UTF-8 text file (directory tree + readable file contents; .db preview). 
将目录树与可读文本内容合并为单一文本，便于分享/排查（含 .db 预览）

# 一句话，把脚本目录中的全部代码输出到一个txt，并带层级结构。

# Pack Folder Tool / 目录打包合并工具

Merge a folder snapshot into one UTF-8 text file:
- directory tree
- readable text file contents
- `.db` files: preview the first row of the first table

将当前目录的“快照”合并为一个 UTF-8 文本文件：
- 目录树（tree）
- 可读文本文件内容（递归合并）
- `.db` 数据库：仅预览“第一个表的第一行”

---

## Features / 功能
- Recursively walks the folder and writes a directory tree.
- Merges readable text files into one output file.
- Skips binary/non-text files (UnicodeDecodeError).
- For `.db` (SQLite) files, only extracts a small preview (first row of first table).

---

## Requirements / 环境
- Python 3.x (standard library only)

---

## Usage / 用法

### Basic / 基本用法
Run the script in the folder you want to package:

在你想合并的目录中运行：

```bash
python3 pack_folder.py
