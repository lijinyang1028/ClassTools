import json
import random
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class RandomToolApp(tk.Tk):
    """主应用程序类，实现Win10风格的随机数生成器与点名器"""

    def __init__(self):
        super().__init__()

        self.title("随机工具 - 随机数生成器 & 点名器")
        self.geometry("900x600")
        self.minsize(800, 500)

        # 设置窗口背景颜色和默认字体（Win10风格）
        self.configure(bg="#f0f0f0")
        self.option_add("*Font", ("Segoe UI", 9))

        # 配置ttk样式，使其更接近Win10风格
        self.setup_styles()

        # 创建主选项卡控件
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建两个页面
        self.random_frame = ttk.Frame(self.notebook)
        self.rollcall_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.random_frame, text="🎲 随机数生成器")
        self.notebook.add(self.rollcall_frame, text="📋 JSON点名器")

        # 初始化各个页面的UI
        self.init_random_number_tab()
        self.init_rollcall_tab()

    def setup_styles(self):
        """配置ttk样式，模拟Win10的扁平化、现代风格"""
        style = ttk.Style()
        # 使用默认主题，并修改部分参数
        style.theme_use('clam')

        # 主背景色
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", foreground="#333333")
        style.configure("TLabelframe", background="#f0f0f0", foreground="#333333")
        style.configure("TLabelframe.Label", background="#f0f0f0", foreground="#333333")

        # 按钮样式：扁平、浅灰背景、深色边框效果
        style.configure("TButton",
                        background="#ffffff",
                        foreground="#333333",
                        borderwidth=1,
                        focusthickness=0,
                        padding=(8, 4))
        style.map("TButton",
                  background=[("active", "#e5e5e5"), ("pressed", "#d0d0d0")],
                  relief=[("pressed", "sunken")])

        # 输入框样式
        style.configure("TEntry",
                        fieldbackground="#ffffff",
                        borderwidth=1,
                        padding=4)
        style.configure("TSpinbox",
                        fieldbackground="#ffffff",
                        borderwidth=1,
                        padding=4)

        # 选项卡样式
        style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
        style.configure("TNotebook.Tab",
                        background="#e0e0e0",
                        padding=[12, 4],
                        borderwidth=1)
        style.map("TNotebook.Tab",
                  background=[("selected", "#ffffff"), ("active", "#eeeeee")])

    # ==================== 随机数生成器页面 ====================
    def init_random_number_tab(self):
        """初始化随机数生成器界面"""
        # 主框架使用grid布局，分为上下两个区域
        main_container = ttk.Frame(self.random_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ---------- 参数设置区域 ----------
        settings_frame = ttk.LabelFrame(main_container, text="参数设置", padding=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))

        # 第一行：最小值 / 最大值
        row1 = ttk.Frame(settings_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Label(row1, text="最小值:").pack(side=tk.LEFT, padx=(0, 5))
        self.min_entry = ttk.Entry(row1, width=12)
        self.min_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.min_entry.insert(0, "1")

        ttk.Label(row1, text="最大值:").pack(side=tk.LEFT, padx=(0, 5))
        self.max_entry = ttk.Entry(row1, width=12)
        self.max_entry.pack(side=tk.LEFT)
        self.max_entry.insert(0, "100")

        # 第二行：生成数量 / 数据类型
        row2 = ttk.Frame(settings_frame)
        row2.pack(fill=tk.X, pady=5)

        ttk.Label(row2, text="生成数量:").pack(side=tk.LEFT, padx=(0, 5))
        self.count_spinbox = ttk.Spinbox(row2, from_=1, to=1000, width=10)
        self.count_spinbox.pack(side=tk.LEFT, padx=(0, 20))
        self.count_spinbox.set(1)

        self.data_type_var = tk.IntVar(value=0)  # 0:整数, 1:浮点数
        ttk.Radiobutton(row2, text="整数", variable=self.data_type_var, value=0).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(row2, text="浮点数", variable=self.data_type_var, value=1).pack(side=tk.LEFT)

        # 生成按钮
        self.generate_btn = ttk.Button(settings_frame, text="生成随机数", command=self.generate_random_numbers)
        self.generate_btn.pack(pady=(10, 0))

        # ---------- 结果显示区域 ----------
        result_frame = ttk.LabelFrame(main_container, text="生成结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # 使用Listbox + 滚动条显示多个结果
        listbox_frame = ttk.Frame(result_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                                         font=("Segoe UI", 9), selectbackground="#0078d7",
                                         bg="#ffffff", relief=tk.FLAT, highlightthickness=0)
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_listbox.yview)

        # 底部操作按钮
        btn_frame = ttk.Frame(result_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="清空结果", command=self.clear_random_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="复制全部", command=self.copy_all_results).pack(side=tk.LEFT, padx=5)

    def generate_random_numbers(self):
        """生成随机数逻辑"""
        try:
            min_val = self.min_entry.get().strip()
            max_val = self.max_entry.get().strip()
            if not min_val or not max_val:
                messagebox.showerror("输入错误", "最小值与最大值不能为空")
                return

            min_val = float(min_val)
            max_val = float(max_val)
            if min_val > max_val:
                messagebox.showerror("范围错误", "最小值不能大于最大值")
                return

            count = self.count_spinbox.get()
            if not count.isdigit():
                messagebox.showerror("输入错误", "生成数量必须是正整数")
                return
            count = int(count)
            if count <= 0 or count > 1000:
                messagebox.showerror("输入错误", "生成数量请设置在1~1000之间")
                return

            # 根据数据类型生成随机数
            is_float = self.data_type_var.get() == 1
            results = []
            for _ in range(count):
                if is_float:
                    # 生成浮点数，保留6位小数
                    val = random.uniform(min_val, max_val)
                    results.append(f"{val:.6f}")
                else:
                    # 整数生成，范围需要取整
                    int_min = int(min_val)
                    int_max = int(max_val)
                    if int_min > int_max:
                        int_min, int_max = int_max, int_min
                    val = random.randint(int_min, int_max)
                    results.append(str(val))

            # 将结果添加到Listbox
            for res in results:
                self.result_listbox.insert(tk.END, res)

            # 自动滚动到底部
            self.result_listbox.see(tk.END)
            # 提示生成成功（状态栏效果不单独做，用短暂的标题提示）
            self.title(f"随机工具 - 已生成{len(results)}个随机数")

        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字(最小值/最大值)")

    def clear_random_results(self):
        """清空随机数结果列表"""
        self.result_listbox.delete(0, tk.END)
        self.title("随机工具 - 随机数生成器 & 点名器")

    def copy_all_results(self):
        """复制全部结果到剪贴板"""
        results = self.result_listbox.get(0, tk.END)
        if not results:
            messagebox.showinfo("提示", "没有可复制的结果")
            return
        text = "\n".join(results)
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("复制成功", f"已复制 {len(results)} 条结果到剪贴板")

    # ==================== 点名器页面 ====================
    def init_rollcall_tab(self):
        """初始化点名器界面"""
        main_container = ttk.Frame(self.rollcall_frame)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 分成左右两个区域：左侧名单管理，右侧点名操作和显示
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_panel = ttk.Frame(main_container, width=250)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_panel.pack_propagate(False)

        # ---------- 左侧：名单列表区 ----------
        list_frame = ttk.LabelFrame(left_panel, text="当前名单", padding=5)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # 名单列表框
        listbox_container = ttk.Frame(list_frame)
        listbox_container.pack(fill=tk.BOTH, expand=True, pady=5)

        scrollbar = ttk.Scrollbar(listbox_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.namelist_box = tk.Listbox(listbox_container, yscrollcommand=scrollbar.set,
                                       font=("Segoe UI", 9), selectbackground="#0078d7",
                                       bg="#ffffff", relief=tk.FLAT, highlightthickness=0)
        self.namelist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.namelist_box.yview)

        # 人数显示标签
        self.total_count_label = ttk.Label(list_frame, text="总人数: 0")
        self.total_count_label.pack(anchor=tk.W, pady=(5, 0))

        # 左侧底部按钮：导入/清空/删除添加等
        list_buttons = ttk.Frame(list_frame)
        list_buttons.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(list_buttons, text="📂 导入JSON", command=self.import_json_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_buttons, text="🗑️ 清空名单", command=self.clear_name_list).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_buttons, text="❌ 删除选中", command=self.delete_selected_name).pack(side=tk.LEFT, padx=2)

        # 手动添加姓名区域
        add_frame = ttk.Frame(list_frame)
        add_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(add_frame, text="新姓名:").pack(side=tk.LEFT, padx=(0, 5))
        self.new_name_entry = ttk.Entry(add_frame)
        self.new_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(add_frame, text="➕ 添加", command=self.add_manual_name).pack(side=tk.LEFT)

        # ---------- 右侧：点名操作区 ----------
        rollcall_frame = ttk.LabelFrame(right_panel, text="点名", padding=15)
        rollcall_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # JSON键名提示输入框（方便自定义JSON结构）
        ttk.Label(rollcall_frame, text="JSON数组键名(可选):", font=("Segoe UI", 8)).pack(anchor=tk.W)
        self.json_key_entry = ttk.Entry(rollcall_frame)
        self.json_key_entry.pack(fill=tk.X, pady=(2, 10))
        self.json_key_entry.insert(0, "自动探测")
        self.json_key_entry.bind("<FocusIn>", lambda e: self.json_key_entry.delete(0, tk.END) if self.json_key_entry.get() == "自动探测" else None)

        # 点名按钮
        self.call_btn = ttk.Button(rollcall_frame, text="🎤 随机点名", command=self.rollcall, width=20)
        self.call_btn.pack(pady=(10, 15))

        # 点名结果显示区域
        result_label = ttk.Label(rollcall_frame, text="点名结果:", font=("Segoe UI", 9, "bold"))
        result_label.pack(anchor=tk.W)

        self.rollcall_result_var = tk.StringVar(value="等待点名...")
        result_display = ttk.Label(rollcall_frame, textvariable=self.rollcall_result_var,
                                   font=("Segoe UI", 16, "bold"), foreground="#0078d7",
                                   background="#f0f0f0", wraplength=220, justify=tk.CENTER)
        result_display.pack(fill=tk.BOTH, expand=True, pady=10)

        # 提示信息
        info_label = ttk.Label(rollcall_frame, text="提示: 支持JSON数组或含指定键名的对象", font=("Segoe UI", 8), foreground="gray")
        info_label.pack(side=tk.BOTTOM, pady=(10, 0))

        # 初始化内部名单存储列表
        self.name_list = []   # 存储姓名字符串

    def update_name_list_display(self):
        """更新Listbox显示和总人数标签"""
        self.namelist_box.delete(0, tk.END)
        for name in self.name_list:
            self.namelist_box.insert(tk.END, name)
        self.total_count_label.config(text=f"总人数: {len(self.name_list)}")

    def import_json_file(self):
        """导入JSON文件，解析为名单列表"""
        file_path = filedialog.askopenfilename(
            title="选择JSON文件",
            filetypes=[("JSON文件", "*.json"), ("所有文件", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 解析JSON得到名单列表
            name_list = self.parse_json_to_list(data)
            if name_list is None:
                messagebox.showerror("解析失败", "JSON结构无效。\n请确保根为数组，或包含常见键名(names/students/list等)，或手动指定键名。")
                return

            if not name_list:
                messagebox.showwarning("空名单", "JSON中未找到任何姓名条目")
                return

            # 替换当前名单
            self.name_list = name_list
            self.update_name_list_display()
            messagebox.showinfo("导入成功", f"成功导入 {len(name_list)} 个姓名")

        except json.JSONDecodeError:
            messagebox.showerror("文件错误", "无法解析JSON文件，请检查文件格式")
        except Exception as e:
            messagebox.showerror("错误", f"读取文件时发生错误: {str(e)}")

    def parse_json_to_list(self, data):
        """根据用户输入的键名或自动探测，从JSON数据中提取姓名列表"""
        # 获取用户指定的键名（若不为空且不是默认提示）
        key_name = self.json_key_entry.get().strip()
        if key_name == "" or key_name == "自动探测":
            key_name = None

        # 情况1: data本身就是列表
        if isinstance(data, list):
            # 确保列表元素都是字符串
            return [str(item) for item in data if item]

        # 情况2: data是字典
        if isinstance(data, dict):
            # 如果用户指定了键名，优先使用
            if key_name and key_name in data:
                val = data[key_name]
                if isinstance(val, list):
                    return [str(item) for item in val if item]
                else:
                    messagebox.showerror("键值错误", f"键 '{key_name}' 对应的值不是列表")
                    return None

            # 自动探测常见键名
            common_keys = ['names', 'students', 'list', 'members', 'data', 'name_list', 'rollcall']
            for k in common_keys:
                if k in data and isinstance(data[k], list):
                    return [str(item) for item in data[k] if item]
            # 若字典中只有一个键且值为列表，也尝试使用
            if len(data) == 1:
                first_val = list(data.values())[0]
                if isinstance(first_val, list):
                    return [str(item) for item in first_val if item]
            # 都失败则提示
            messagebox.showerror("解析失败", "字典中未找到包含名单列表的常见键名。请在'JSON数组键名'中输入正确的键名。")
            return None

        # 其他类型不支持
        messagebox.showerror("格式错误", "JSON根必须是数组或对象")
        return None

    def clear_name_list(self):
        """清空当前名单"""
        if self.name_list and messagebox.askyesno("确认清空", "确定要清空所有名单吗？"):
            self.name_list = []
            self.update_name_list_display()
            self.rollcall_result_var.set("名单已清空")
        elif not self.name_list:
            messagebox.showinfo("提示", "名单已经是空的")

    def delete_selected_name(self):
        """删除选中的姓名"""
        selected = self.namelist_box.curselection()
        if not selected:
            messagebox.showinfo("提示", "请先选中要删除的姓名")
            return
        index = selected[0]
        deleted_name = self.name_list.pop(index)
        self.update_name_list_display()
        self.rollcall_result_var.set(f"已删除: {deleted_name}")

    def add_manual_name(self):
        """手动添加姓名"""
        new_name = self.new_name_entry.get().strip()
        if not new_name:
            messagebox.showwarning("警告", "姓名不能为空")
            return
        if new_name in self.name_list:
            messagebox.showinfo("提示", "该姓名已存在，为避免重复未添加")
            return
        self.name_list.append(new_name)
        self.update_name_list_display()
        self.new_name_entry.delete(0, tk.END)
        self.rollcall_result_var.set(f"已添加: {new_name}")

    def rollcall(self):
        """随机点名"""
        if not self.name_list:
            messagebox.showwarning("无法点名", "名单为空，请先导入JSON或手动添加姓名")
            return
        chosen = random.choice(self.name_list)
        self.rollcall_result_var.set(chosen)

        # 在Listbox中高亮显示被点中的人
        try:
            index = self.name_list.index(chosen)
            self.namelist_box.selection_clear(0, tk.END)
            self.namelist_box.selection_set(index)
            self.namelist_box.see(index)
        except ValueError:
            pass  # 理论上不会发生


if __name__ == "__main__":
    app = RandomToolApp()
    app.mainloop()