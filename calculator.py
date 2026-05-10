import tkinter as tk
from tkinter import ttk
import math
from datetime import datetime

# Цветовая схема (тёмная тема с неоновым акцентом)
COLORS = {
    'bg': '#1e1e2e',           # тёмный фон
    'display': '#181825',       # фон дисплея
    'display_text': '#cdd6f4',  # цвет текста на дисплее
    'btn_normal': '#313244',    # обычная кнопка
    'btn_normal_text': '#cdd6f4',
    'btn_operator': '#89b4fa',  # операторы (синий)
    'btn_operator_text': '#1e1e2e',
    'btn_equal': '#a6e3a1',     # равно (зелёный)
    'btn_equal_text': '#1e1e2e',
    'btn_clear': '#f38ba8',     # очистка (красный)
    'btn_clear_text': '#1e1e2e',
    'btn_special': '#cba6f7',   # научные/память (фиолетовый)
    'btn_special_text': '#1e1e2e',
    'btn_memory': '#94e2d5',    # память (бирюзовый)
    'btn_memory_text': '#1e1e2e',
    'hover': '#45475a',         # цвет при наведении
    'tab_bg': '#11111b',        # фон вкладок
    'tab_fg': '#cdd6f4',
    'status_bg': '#11111b',
}

class ModernButton(tk.Button):
    """Кнопка с эффектом наведения и закруглёнными углами"""
    def __init__(self, master, text, color_type='normal', **kwargs):
        self.color_type = color_type
        self.default_bg = self.get_bg_color()
        self.default_fg = self.get_fg_color()
        
        super().__init__(
            master, text=text,
            font=('Segoe UI', 11, 'bold'),
            bg=self.default_bg, fg=self.default_fg,
            relief=tk.FLAT, bd=0,
            activebackground=self.get_hover_color(),
            activeforeground=self.default_fg,
            cursor='hand2',
            **kwargs
        )
        
        # Привязываем события наведения
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
        # Делаем тень
        self.configure(highlightthickness=0)
    
    def get_bg_color(self):
        return {
            'normal': COLORS['btn_normal'],
            'operator': COLORS['btn_operator'],
            'equal': COLORS['btn_equal'],
            'clear': COLORS['btn_clear'],
            'special': COLORS['btn_special'],
            'memory': COLORS['btn_memory']
        }.get(self.color_type, COLORS['btn_normal'])
    
    def get_fg_color(self):
        return {
            'normal': COLORS['btn_normal_text'],
            'operator': COLORS['btn_operator_text'],
            'equal': COLORS['btn_equal_text'],
            'clear': COLORS['btn_clear_text'],
            'special': COLORS['btn_special_text'],
            'memory': COLORS['btn_memory_text']
        }.get(self.color_type, COLORS['btn_normal_text'])
    
    def get_hover_color(self):
        hover_map = {
            'normal': '#45475a',
            'operator': '#b4befe',
            'equal': '#a6e3a1',
            'clear': '#f9e2af',
            'special': '#f5c2e7',
            'memory': '#b4befe'
        }
        return hover_map.get(self.color_type, COLORS['hover'])
    
    def on_enter(self, event):
        self.config(bg=self.get_hover_color())
    
    def on_leave(self, event):
        self.config(bg=self.default_bg)


class ModernDisplay(tk.Frame):
    """Современный дисплей с тенью"""
    def __init__(self, parent, textvariable, **kwargs):
        super().__init__(parent, bg=COLORS['display'], highlightthickness=0)
        
        self.label = tk.Label(
            self, textvariable=textvariable,
            font=('Segoe UI', 24, 'bold'),
            bg=COLORS['display'], fg=COLORS['display_text'],
            anchor='e', padx=15, pady=15
        )
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Добавляем рамку
        self.configure(highlightbackground=COLORS['bg'], highlightthickness=2)


class SimpleCalculator:
    """Обычный калькулятор с красивым интерфейсом"""
    def __init__(self, parent, shared_memory, add_to_history):
        self.parent = parent
        self.shared_memory = shared_memory
        self.add_to_history = add_to_history
        self.expression = ""
        
        # Настройка фона
        parent.configure(bg=COLORS['bg'])
        
        # Дисплей
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Панель кнопок
        buttons_frame = tk.Frame(parent, bg=COLORS['bg'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Кнопки с цветовой дифференциацией
        buttons = [
            ('7', 1, 0, 'normal'), ('8', 1, 1, 'normal'), ('9', 1, 2, 'normal'), ('/', 1, 3, 'operator'), ('⌫', 1, 4, 'clear'),
            ('4', 2, 0, 'normal'), ('5', 2, 1, 'normal'), ('6', 2, 2, 'normal'), ('*', 2, 3, 'operator'), ('√', 2, 4, 'special'),
            ('1', 3, 0, 'normal'), ('2', 3, 1, 'normal'), ('3', 3, 2, 'normal'), ('-', 3, 3, 'operator'), ('x²', 3, 4, 'special'),
            ('0', 4, 0, 'normal'), ('.', 4, 1, 'normal'), ('±', 4, 2, 'special'), ('+', 4, 3, 'operator'), ('1/x', 4, 4, 'special'),
            ('MC', 5, 0, 'memory'), ('MR', 5, 1, 'memory'), ('M+', 5, 2, 'memory'), ('M-', 5, 3, 'memory'), ('=', 5, 4, 'equal'),
        ]
        
        for text, row, col, color in buttons:
            btn = ModernButton(buttons_frame, text=text, color_type=color,
                              command=lambda t=text: self.click(t))
            btn.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
        
        # Настройка сетки
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Горячие клавиши
        parent.bind('<Key>', self.hotkey)
    
    def hotkey(self, event):
        key = event.char
        if key.isdigit() or key in '+-*/.':
            self.click(key)
        elif key == '\r':
            self.click('=')
        elif key == '\x08':
            current = self.display_var.get()
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
    
    def click(self, key):
        if key == '⌫':
            current = self.display_var.get()
            if len(current) > 1:
                self.display_var.set(current[:-1])
            else:
                self.display_var.set("0")
        elif key.isdigit() or key == '.':
            self.number_click(key)
        elif key in '+-*/':
            self.operator_click(key)
        elif key == '=':
            self.calculate()
        elif key == 'C' or key == 'c':
            self.clear()
        elif key == '±':
            self.negate()
        elif key == '√':
            self.square_root()
        elif key == 'x²':
            self.square()
        elif key == '1/x':
            self.reciprocal()
        elif key == 'MC':
            self.shared_memory[0] = 0
        elif key == 'MR':
            self.display_var.set(str(self.shared_memory[0]))
        elif key == 'M+':
            try:
                self.shared_memory[0] += float(self.display_var.get())
            except:
                pass
        elif key == 'M-':
            try:
                self.shared_memory[0] -= float(self.display_var.get())
            except:
                pass
    
    def number_click(self, num):
        current = self.display_var.get()
        if current == "0" or current == "Ошибка":
            self.display_var.set(num)
        else:
            self.display_var.set(current + num)
    
    def operator_click(self, op):
        current = self.display_var.get()
        if current not in '+-*/' and not current.endswith('.'):
            self.expression = current + op
            self.display_var.set(current + op)
    
    def calculate(self):
        try:
            expr = self.display_var.get()
            result = eval(expr)
            result = round(result, 10)
            self.add_to_history(f"{expr} = {result}")
            self.display_var.set(str(result))
            self.expression = ""
        except:
            self.display_var.set("Ошибка")
    
    def clear(self):
        self.display_var.set("0")
        self.expression = ""
    
    def negate(self):
        try:
            current = float(self.display_var.get())
            self.display_var.set(str(-current))
        except:
            pass
    
    def square_root(self):
        try:
            current = float(self.display_var.get())
            self.display_var.set(str(round(math.sqrt(current), 10)))
        except:
            self.display_var.set("Ошибка")
    
    def square(self):
        try:
            current = float(self.display_var.get())
            self.display_var.set(str(round(current ** 2, 10)))
        except:
            pass
    
    def reciprocal(self):
        try:
            current = float(self.display_var.get())
            self.display_var.set(str(round(1 / current, 10)))
        except:
            self.display_var.set("Ошибка")


class ScientificCalculator:
    """Научный калькулятор с красивым интерфейсом"""
    def __init__(self, parent, shared_memory, add_to_history):
        self.parent = parent
        self.shared_memory = shared_memory
        self.add_to_history = add_to_history
        
        parent.configure(bg=COLORS['bg'])
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
        buttons_frame = tk.Frame(parent, bg=COLORS['bg'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Кнопки научного калькулятора
        row1 = [('sin', 0, 0, 'special'), ('cos', 0, 1, 'special'), ('tan', 0, 2, 'special'),
                ('log', 0, 3, 'special'), ('ln', 0, 4, 'special'), ('C', 0, 5, 'clear')]
        row2 = [('7', 1, 0, 'normal'), ('8', 1, 1, 'normal'), ('9', 1, 2, 'normal'),
                ('^', 1, 3, 'operator'), ('√', 1, 4, 'special'), ('(', 1, 5, 'operator')]
        row3 = [('4', 2, 0, 'normal'), ('5', 2, 1, 'normal'), ('6', 2, 2, 'normal'),
                ('*', 2, 3, 'operator'), ('/', 2, 4, 'operator'), (')', 2, 5, 'operator')]
        row4 = [('1', 3, 0, 'normal'), ('2', 3, 1, 'normal'), ('3', 3, 2, 'normal'),
                ('+', 3, 3, 'operator'), ('-', 3, 4, 'operator'), ('=', 3, 5, 'equal')]
        row5 = [('0', 4, 0, 'normal'), ('.', 4, 1, 'normal'), ('±', 4, 2, 'special'),
                ('π', 4, 3, 'special'), ('e', 4, 4, 'special'), ('MC', 4, 5, 'memory')]
        row6 = [('MR', 5, 0, 'memory'), ('M+', 5, 1, 'memory'), ('M-', 5, 2, 'memory'),
                ('', 5, 3, 'normal'), ('', 5, 4, 'normal'), ('', 5, 5, 'normal')]
        
        all_rows = [row1, row2, row3, row4, row5, row6]
        
        for row_idx, row in enumerate(all_rows):
            for text, r, c, color in row:
                if text:
                    btn = ModernButton(buttons_frame, text=text, color_type=color,
                                      command=lambda t=text: self.click(t))
                    btn.grid(row=row_idx, column=c, sticky="nsew", padx=4, pady=4)
        
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        parent.bind('<Key>', self.hotkey)
    
    def hotkey(self, event):
        key = event.char
        if key.isdigit() or key in '+-*/.':
            self.click(key)
        elif key == '\r':
            self.click('=')
    
    def click(self, key):
        if key.isdigit() or key == '.':
            self.number_click(key)
        elif key == 'C':
            self.clear()
        elif key == '=':
            self.calculate()
        elif key in '+-*/^':
            self.operator_click(key)
        elif key == '±':
            self.negate()
        elif key == '√':
            self.square_root()
        elif key == 'π':
            self.display_var.set(str(math.pi))
        elif key == 'e':
            self.display_var.set(str(math.e))
        elif key == 'sin':
            self.scientific_func(math.sin, lambda x: math.radians(x))
        elif key == 'cos':
            self.scientific_func(math.cos, lambda x: math.radians(x))
        elif key == 'tan':
            self.scientific_func(math.tan, lambda x: math.radians(x))
        elif key == 'log':
            self.scientific_func(math.log10, lambda x: x)
        elif key == 'ln':
            self.scientific_func(math.log, lambda x: x)
        elif key == '(' or key == ')':
            self.add_paren(key)
        elif key == 'MC':
            self.shared_memory[0] = 0
        elif key == 'MR':
            self.display_var.set(str(self.shared_memory[0]))
        elif key == 'M+':
            try:
                self.shared_memory[0] += float(self.display_var.get())
            except:
                pass
        elif key == 'M-':
            try:
                self.shared_memory[0] -= float(self.display_var.get())
            except:
                pass
    
    def number_click(self, num):
        current = self.display_var.get()
        if current == "0" or current == "Ошибка":
            self.display_var.set(num)
        else:
            self.display_var.set(current + num)
    
    def operator_click(self, op):
        current = self.display_var.get()
        if current not in '+-*/^' and not current.endswith('.'):
            self.display_var.set(current + op)
    
    def add_paren(self, paren):
        current = self.display_var.get()
        self.display_var.set(current + paren)
    
    def scientific_func(self, func, converter):
        try:
            current = float(self.display_var.get())
            result = func(converter(current))
            self.add_to_history(f"{func.__name__}({current}) = {round(result, 10)}")
            self.display_var.set(str(round(result, 10)))
        except:
            self.display_var.set("Ошибка")
    
    def calculate(self):
        try:
            expr = self.display_var.get()
            expr = expr.replace('^', '**')
            result = eval(expr)
            result = round(result, 10)
            self.add_to_history(f"{expr} = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def clear(self):
        self.display_var.set("0")
    
    def negate(self):
        try:
            current = float(self.display_var.get())
            self.display_var.set(str(-current))
        except:
            pass
    
    def square_root(self):
        try:
            current = float(self.display_var.get())
            self.display_var.set(str(round(math.sqrt(current), 10)))
        except:
            self.display_var.set("Ошибка")


class ProgrammerCalculator:
    """Программистский калькулятор с красивым интерфейсом"""
    def __init__(self, parent, shared_memory, add_to_history):
        self.parent = parent
        self.shared_memory = shared_memory
        self.add_to_history = add_to_history
        self.current_base = "DEC"
        self.current_value = 0
        
        parent.configure(bg=COLORS['bg'])
        
        # Переключатель систем счисления (стильный)
        base_frame = tk.Frame(parent, bg=COLORS['bg'])
        base_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        self.dec_btn = ModernButton(base_frame, text="DEC", color_type='special',
                                    command=lambda: self.set_base("DEC"))
        self.dec_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        self.hex_btn = ModernButton(base_frame, text="HEX", color_type='normal',
                                    command=lambda: self.set_base("HEX"))
        self.hex_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        self.bin_btn = ModernButton(base_frame, text="BIN", color_type='normal',
                                    command=lambda: self.set_base("BIN"))
        self.bin_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Дисплей
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки
        buttons_frame = tk.Frame(parent, bg=COLORS['bg'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        row1 = [('7', 0, 0, 'normal'), ('8', 0, 1, 'normal'), ('9', 0, 2, 'normal'),
                ('A', 0, 3, 'special'), ('B', 0, 4, 'special'), ('C', 0, 5, 'special')]
        row2 = [('4', 1, 0, 'normal'), ('5', 1, 1, 'normal'), ('6', 1, 2, 'normal'),
                ('D', 1, 3, 'special'), ('E', 1, 4, 'special'), ('F', 1, 5, 'special')]
        row3 = [('1', 2, 0, 'normal'), ('2', 2, 1, 'normal'), ('3', 2, 2, 'normal'),
                ('<<', 2, 3, 'operator'), ('>>', 2, 4, 'operator'), ('C', 2, 5, 'clear')]
        row4 = [('0', 3, 0, 'normal'), ('AND', 3, 1, 'operator'), ('OR', 3, 2, 'operator'),
                ('XOR', 3, 3, 'operator'), ('NOT', 3, 4, 'operator'), ('=', 3, 5, 'equal')]
        row5 = [('MC', 4, 0, 'memory'), ('MR', 4, 1, 'memory'), ('M+', 4, 2, 'memory'),
                ('M-', 4, 3, 'memory'), ('', 4, 4, 'normal'), ('', 4, 5, 'normal')]
        
        all_rows = [row1, row2, row3, row4, row5]
        
        for row_idx, row in enumerate(all_rows):
            for text, r, c, color in row:
                if text:
                    btn = ModernButton(buttons_frame, text=text, color_type=color,
                                      command=lambda t=text: self.click(t))
                    btn.grid(row=row_idx, column=c, sticky="nsew", padx=4, pady=4)
        
        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        parent.bind('<Key>', self.hotkey)
    
    def set_base(self, base):
        self.current_base = base
        self.update_button_styles()
        self.update_display()
    
    def update_button_styles(self):
        # Обновляем стиль кнопок переключения
        for btn, base in [(self.dec_btn, "DEC"), (self.hex_btn, "HEX"), (self.bin_btn, "BIN")]:
            if base == self.current_base:
                btn.config(bg=COLORS['btn_special'], fg=COLORS['btn_special_text'])
            else:
                btn.config(bg=COLORS['btn_normal'], fg=COLORS['btn_normal_text'])
    
    def update_display(self):
        if self.current_base == "DEC":
            self.display_var.set(str(self.current_value))
        elif self.current_base == "HEX":
            self.display_var.set(hex(self.current_value)[2:].upper())
        elif self.current_base == "BIN":
            self.display_var.set(bin(self.current_value)[2:])
    
    def get_input_value(self):
        text = self.display_var.get()
        try:
            if self.current_base == "DEC":
                return int(text) if text else 0
            elif self.current_base == "HEX":
                return int(text, 16) if text else 0
            elif self.current_base == "BIN":
                return int(text, 2) if text else 0
        except:
            return 0
    
    def hotkey(self, event):
        key = event.char.upper()
        if key in '0123456789ABCDEF':
            self.click(key)
        elif key == '\r':
            self.click('=')
    
    def click(self, key):
        if key in '0123456789ABCDEF':
            self.number_click(key)
        elif key == '=':
            pass
        elif key == 'C':
            self.current_value = 0
            self.update_display()
        elif key == '<<':
            self.current_value <<= 1
            self.update_display()
            self.add_to_history(f"Сдвиг влево: {self.current_value}")
        elif key == '>>':
            self.current_value >>= 1
            self.update_display()
            self.add_to_history(f"Сдвиг вправо: {self.current_value}")
        elif key == 'AND':
            val = self.get_input_value()
            self.current_value &= val
            self.update_display()
        elif key == 'OR':
            val = self.get_input_value()
            self.current_value |= val
            self.update_display()
        elif key == 'XOR':
            val = self.get_input_value()
            self.current_value ^= val
            self.update_display()
        elif key == 'NOT':
            self.current_value = ~self.current_value & 0xFFFFFFFF
            self.update_display()
        elif key == 'MC':
            self.shared_memory[0] = 0
        elif key == 'MR':
            self.current_value = self.shared_memory[0]
            self.update_display()
        elif key == 'M+':
            self.shared_memory[0] += self.current_value
        elif key == 'M-':
            self.shared_memory[0] -= self.current_value
    
    def number_click(self, num):
        current = self.display_var.get()
        if current == "0" or current == "Ошибка":
            self.display_var.set(num)
        else:
            self.display_var.set(current + num)
        self.current_value = self.get_input_value()


class HistoryTab:
    """Вкладка истории с красивым оформлением"""
    def __init__(self, parent):
        self.parent = parent
        parent.configure(bg=COLORS['bg'])
        
        self.history_text = tk.Text(
            parent, 
            font=('Consolas', 10),
            bg=COLORS['display'],
            fg=COLORS['display_text'],
            relief=tk.FLAT,
            bd=0,
            wrap=tk.WORD,
            insertbackground=COLORS['display_text']
        )
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 10))
        
        scrollbar = tk.Scrollbar(self.history_text, bg=COLORS['bg'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
        clear_btn = ModernButton(parent, text="Очистить историю", color_type='clear',
                                 command=self.clear_history)
        clear_btn.pack(pady=(0, 15))
    
    def add_entry(self, entry):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_text.insert(tk.END, f"[{timestamp}] {entry}\n")
        self.history_text.see(tk.END)
    
    def clear_history(self):
        self.history_text.delete(1.0, tk.END)


class MultiCalculator:
    """Главное окно с красивым интерфейсом"""
    def __init__(self, root):
        self.root = root
        self.root.title("✨ MultiCalc — Современный калькулятор")
        self.root.geometry("650x700")
        self.root.configure(bg=COLORS['bg'])
        
        # Иконка окна (можно добавить, если есть)
        try:
            self.root.iconbitmap('calc.ico')
        except:
            pass
        
        # Общая память
        self.shared_memory = [0]
        
        # История
        self.history = []
        
        # Стиль для вкладок
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=COLORS['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=COLORS['btn_normal'], 
                       foreground=COLORS['display_text'], padding=[15, 5],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', COLORS['btn_special'])])
        
        # Вкладки
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        # Создаём вкладки
        self.simple_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.scientific_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.programmer_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.history_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        
        self.notebook.add(self.simple_frame, text="🧮 Обычный")
        self.notebook.add(self.scientific_frame, text="🔬 Научный")
        self.notebook.add(self.programmer_frame, text="💻 Программист")
        self.notebook.add(self.history_frame, text="📜 История")
        
        # Инициализация калькуляторов
        self.simple_calc = SimpleCalculator(self.simple_frame, self.shared_memory, self.add_to_history)
        self.scientific_calc = ScientificCalculator(self.scientific_frame, self.shared_memory, self.add_to_history)
        self.programmer_calc = ProgrammerCalculator(self.programmer_frame, self.shared_memory, self.add_to_history)
        self.history_tab = HistoryTab(self.history_frame)
        
        # Статус-бар
        self.status_var = tk.StringVar()
        self.status_var.set(f"💾 Общая память: {self.shared_memory[0]}")
        status_bar = tk.Label(
            root, textvariable=self.status_var,
            bg=COLORS['status_bg'], fg=COLORS['display_text'],
            font=('Segoe UI', 9), anchor='w', padx=10, pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Обновление статуса
        self.update_status()
    
    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_tab.add_entry(entry)
    
    def update_status(self):
        self.status_var.set(f"💾 Общая память: {self.shared_memory[0]} (доступна во всех калькуляторах)")
        self.root.after(500, self.update_status)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiCalculator(root)
    root.mainloop()