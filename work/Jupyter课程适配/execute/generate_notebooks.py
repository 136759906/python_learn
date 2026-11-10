"""从阶段一的原始练习生成可逐段运行的 Notebook。"""

import ast
import hashlib
import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COURSES = ROOT / "stage01_core"


def cell(kind: str, source: str) -> dict:
    cell_id = hashlib.sha1(f"{kind}:{source}".encode("utf-8")).hexdigest()[:12]
    result = {"cell_type": kind, "id": cell_id, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        result.update(execution_count=None, outputs=[])
    return result


for path in sorted(COURSES.glob("[0-9][0-9]_*.py")):
    source = path.read_text(encoding="utf-8-sig")
    title = ast.get_docstring(ast.parse(source)) or path.stem
    cells = [cell("markdown", f"# {title}\n\n按顺序运行单元格。修改前面的代码后，重新运行相关单元格，再运行验证。")]

    if path.name.startswith("01_"):
        sections = re.split(r"(?=^# =+\n# (?:\d+\. |【练习】))", source, flags=re.MULTILINE)
        for section in sections:
            if not section.strip():
                continue
            if "# 【练习】" in section:
                cells.append(cell("markdown", "## 自己动手\n\n完成下面四道题，在下一格编写并运行代码。"))
                cells.append(cell("code", section))
            else:
                cells.append(cell("code", section))
    else:
        lines = source.splitlines(keepends=True)
        main = next((n for n in ast.parse(source).body if isinstance(n, ast.If) and
                     isinstance(n.test, ast.Compare) and isinstance(n.test.left, ast.Name)
                     and n.test.left.id == "__name__"), None)
        if main is None:
            raise ValueError(f"缺少验证代码: {path}")
        cells.append(cell("code", "".join(lines[:main.lineno - 1])))
        cells.append(cell("markdown", "## 验证\n\n先完成上面的 TODO，再运行下一格；未完成时断言失败是正常的。"))
        cells.append(cell("code", textwrap.dedent("".join(lines[main.lineno:main.end_lineno]))))

    notebook = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                               "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
    target = path.with_suffix(".ipynb")
    target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(target.relative_to(ROOT))
