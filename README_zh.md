# 高中班级百宝箱

一个基于 Python + Tkinter 的多功能桌面工具集，为班级日常使用提供趣味性与实用性。

## 功能清单

* **精美图形化时钟**  
支持多种主题、12/24小时制、窗口置顶、淡入动画。
* **今日人品测试**  
随机生成人品值（1\~100），附带趣味评价和“欧皇”彩蛋窗口。
* **可扩展功能面板**  
所有小工具统一从面板启动，新增功能只需在 `main.py` 中注册一行。

## 快速开始

### 环境要求

* Python 3.6+
* 仅依赖标准库（tkinter, random, datetime, time）

### 运行方法

```bash
git clone https://github.com/lijinyang1028/my\\\_own\\\_library.git
cd my\\\_own\\\_library
python "精美图形化时钟.py"
```

> 如果遇到中文字体问题，可以将代码中的 `'苹方\\\_XX'` 替换为系统支持的字体（如 `'微软雅黑'`、`'Arial'`）。

### 快捷键（在时钟窗口下）

|按键|功能|
|-|-|
|`ESC`|退出程序|
|`空格`|切换时钟主题|
|`F1`|切换 12/24 小时制|
|`F2`|显示/隐藏秒|
|`F3`|打开人品测试（或功能面板中点击）|

## 项目结构

```
.
├── 精美图形化时钟.py      # 主入口，包含时钟和功能面板
├── main.py               # 功能面板容器，动态管理所有小工具
├── lucktest.py           # 人品测试模块
├── websearcher.py        # （待完善）网络请求模块
└── README.md
```

## 如何添加新功能？

1. 在 `main.py` 中导入你的模块。
2. 在 `FunctionPanel.\\\_\\\_init\\\_\\\_` 中调用 `self.register\\\_function("按钮文字", self.你的方法名)`。
3. 在类中实现 `self.你的方法名`，通常创建一个新的 `Toplevel` 窗口来展示功能。

示例：

```python
def \\\_my\\\_new\\\_feature(self):
    import my\\\_module
    my\\\_module.show\\\_window(self.winfo\\\_toplevel())
```

## 注意事项

* 因为 `tkinter` 的某些主题切换不会自动刷新子组件的背景色，如果你希望功能面板也跟随主题，可以在 `FunctionPanel` 中增加一个 `refresh\\\_theme(bg, fg)` 方法，然后在时钟的 `apply\\\_theme` 中调用它。
* 人品测试的“隐藏款”窗口使用了 `Toplevel`，请确保父窗口存在，否则可能出现异常（代码已做处理）。

## 未来计划

* \[ ] 网络内容搜索（聚合班级通知等）
* \[ ] 课程表提醒
* \[ ] 倒计时（高考、期末）
* \[ ] 随机点名器

## 贡献

欢迎任何人提交 PR 或提出新功能建议！

## 许可证

MIT License

