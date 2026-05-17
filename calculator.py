import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime, timedelta
import numpy as np
import json
import csv
from fractions import Fraction
import calendar

# Попытка импорта matplotlib с обработкой ошибок
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Для работы графика установите: pip install matplotlib numpy")

# Цветовая схема (тёмная тема с неоновым акцентом)
COLORS = {
    'bg': "#4e4e58",
    'display': '#181825',
    'display_text': '#cdd6f4',
    'btn_normal': "#6D71B6",
    'btn_normal_text': '#cdd6f4',
    'btn_operator': '#89b4fa',
    'btn_operator_text': '#1e1e2e',
    'btn_equal': '#a6e3a1',
    'btn_equal_text': '#1e1e2e',
    'btn_clear': '#f38ba8',
    'btn_clear_text': '#1e1e2e',
    'btn_special': '#cba6f7',
    'btn_special_text': '#1e1e2e',
    'btn_memory': '#94e2d5',
    'btn_memory_text': '#1e1e2e',
    'btn_finance': '#fab387',
    'btn_finance_text': '#1e1e2e',
    'btn_converter': '#b4befe',
    'btn_converter_text': '#1e1e2e',
    'hover': '#45475a',
    'tab_bg': '#11111b',
    'tab_fg': '#cdd6f4',
    'status_bg': '#11111b',
}

# Дополнительные темы оформления
THEMES = {
    'dark': COLORS,
    'light': {
        'bg': "#f0f0f0",
        'display': '#ffffff',
        'display_text': '#333333',
        'btn_normal': "#e0e0e0",
        'btn_normal_text': '#333333',
        'btn_operator': '#ffab40',
        'btn_operator_text': '#ffffff',
        'btn_equal': '#4caf50',
        'btn_equal_text': '#ffffff',
        'btn_clear': '#f44336',
        'btn_clear_text': '#ffffff',
        'btn_special': '#9c27b0',
        'btn_special_text': '#ffffff',
        'btn_memory': '#00bcd4',
        'btn_memory_text': '#ffffff',
        'btn_finance': '#ff9800',
        'btn_finance_text': '#ffffff',
        'btn_converter': '#2196f3',
        'btn_converter_text': '#ffffff',
        'hover': '#d0d0d0',
        'tab_bg': '#e0e0e0',
        'tab_fg': '#333333',
        'status_bg': '#e0e0e0',
    }
}

class VariableManager:
    """Система переменных для хранения и использования значений"""
    def __init__(self):
        self.variables = {
            'ans': 0,
            'pi': math.pi,
            'e': math.e,
            'phi': (1 + math.sqrt(5)) / 2,  # Золотое сечение
            'c': 299792458,  # Скорость света м/с
            'g': 9.80665,    # Ускорение свободного падения
            'h': 6.62607015e-34,  # Постоянная Планка
        }
    
    def set_var(self, name, value):
        self.variables[name] = value
    
    def get_var(self, name):
        return self.variables.get(name, None)
    
    def list_vars(self):
        return list(self.variables.keys())

class CurrencyConverter:
    """Конвертер валют с кэшированием курсов"""
    def __init__(self):
        self.rates = {}
        self.last_update = None
        self.load_default_rates()
    
    def load_default_rates(self):
        """Загрузка курсов по умолчанию"""
        self.rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'RUB': 90.5,
            'GBP': 0.79,
            'JPY': 149.5,
            'CNY': 7.24,
            'CHF': 0.88,
            'CAD': 1.36,
            'AUD': 1.53,
            'KZT': 450.0,
        }
        self.last_update = datetime.now()
    
    def convert(self, amount, from_currency, to_currency):
        """Конвертация валют"""
        if from_currency not in self.rates or to_currency not in self.rates:
            return None
        
        # Конвертация через USD
        usd_amount = amount / self.rates[from_currency]
        result = usd_amount * self.rates[to_currency]
        return round(result, 2)

class UnitConverter:
    """Конвертер единиц измерения"""
    def __init__(self):
        self.length = {
            'метр': 1, 'км': 1000, 'см': 0.01, 'мм': 0.001,
            'миля': 1609.34, 'ярд': 0.9144, 'фут': 0.3048,
            'дюйм': 0.0254, 'морская миля': 1852
        }
        self.mass = {
            'кг': 1, 'г': 0.001, 'мг': 1e-6, 'тонна': 1000,
            'фунт': 0.453592, 'унция': 0.0283495,
            'карат': 0.0002, 'стоун': 6.35029
        }
        self.temperature_formulas = {
            ('Цельсий', 'Фаренгейт'): lambda c: c * 9/5 + 32,
            ('Фаренгейт', 'Цельсий'): lambda f: (f - 32) * 5/9,
            ('Цельсий', 'Кельвин'): lambda c: c + 273.15,
            ('Кельвин', 'Цельсий'): lambda k: k - 273.15,
            ('Фаренгейт', 'Кельвин'): lambda f: (f + 459.67) * 5/9,
            ('Кельвин', 'Фаренгейт'): lambda k: k * 9/5 - 459.67,
        }
        self.area = {
            'м²': 1, 'км²': 1e6, 'см²': 0.0001,
            'га': 10000, 'акр': 4046.86, 'сотка': 100
        }
        self.volume = {
            'м³': 1, 'литр': 0.001, 'мл': 1e-6,
            'галлон': 0.00378541, 'баррель': 0.158987
        }
        self.speed = {
            'м/с': 1, 'км/ч': 0.277778, 'миль/ч': 0.44704,
            'узел': 0.514444, 'мах': 340.3
        }
    
    def convert(self, value, from_unit, to_unit, category):
        """Конвертация единиц измерения"""
        if category == 'температура':
            key = (from_unit, to_unit)
            if key in self.temperature_formulas:
                return self.temperature_formulas[key](value)
            return value
        
        units = getattr(self, category, {})
        if from_unit in units and to_unit in units:
            # Конвертация через базовую единицу
            base_value = value * units[from_unit]
            result = base_value / units[to_unit]
            return round(result, 10)
        return None

class FractionCalculator:
    """Калькулятор для работы с дробями"""
    def __init__(self):
        self.mode = 'fraction'  # fraction или decimal
    
    def calculate(self, expr):
        """Вычисление выражения с дробями"""
        try:
            # Заменяем ÷ на / для совместимости
            expr = expr.replace('÷', '/')
            result = eval(expr)
            if self.mode == 'fraction':
                frac = Fraction(result).limit_denominator(1000)
                if frac.denominator == 1:
                    return str(frac.numerator)
                return f"{frac.numerator}/{frac.denominator}"
            else:
                return str(round(float(result), 10))
        except:
            return "Ошибка"
    
    def simplify(self, numerator, denominator):
        """Упрощение дроби"""
        frac = Fraction(numerator, denominator)
        return f"{frac.numerator}/{frac.denominator}"

class DateCalculator:
    """Калькулятор для работы с датами"""
    def __init__(self):
        self.months_ru = [
            '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        self.days_ru = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    
    def days_between(self, date1, date2):
        """Количество дней между датами"""
        delta = date2 - date1
        return delta.days
    
    def add_days(self, date, days):
        """Добавление дней к дате"""
        return date + timedelta(days=days)
    
    def add_months(self, date, months):
        """Добавление месяцев к дате"""
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, calendar.monthrange(year, month)[1])
        return date.replace(year=year, month=month, day=day)
    
    def day_of_week(self, date):
        """День недели"""
        return self.days_ru[date.weekday()]
    
    def format_date(self, date):
        """Форматирование даты"""
        return f"{date.day} {self.months_ru[date.month]} {date.year} г."
    
    def is_leap_year(self, year):
        """Проверка на високосный год"""
        return calendar.isleap(year)

class FinancialCalculator:
    """Финансовый калькулятор"""
    def __init__(self):
        pass
    
    def compound_interest(self, principal, rate, time, n=12):
        """Сложный процент
        
        Args:
            principal: начальная сумма
            rate: годовая ставка (в долях, например 0.05 для 5%)
            time: срок в годах
            n: количество начислений в год
        """
        return principal * (1 + rate/n)**(n*time)
    
    def simple_interest(self, principal, rate, time):
        """Простые проценты"""
        return principal * (1 + rate * time)
    
    def loan_payment(self, principal, rate, months):
        """Ежемесячный платеж по кредиту (аннуитетный)
        
        Args:
            principal: сумма кредита
            rate: годовая ставка (в долях)
            months: срок в месяцах
        """
        monthly_rate = rate / 12
        if monthly_rate == 0:
            return principal / months
        payment = principal * (monthly_rate * (1 + monthly_rate)**months) / \
                  ((1 + monthly_rate)**months - 1)
        return round(payment, 2)
    
    def total_loan_cost(self, principal, rate, months):
        """Общая стоимость кредита"""
        payment = self.loan_payment(principal, rate, months)
        return round(payment * months, 2)
    
    def npv(self, rate, cashflows):
        """Чистая приведенная стоимость (NPV)
        
        Args:
            rate: ставка дисконтирования
            cashflows: список денежных потоков
        """
        return sum(cf / (1 + rate)**t for t, cf in enumerate(cashflows))
    
    def future_value(self, payment, rate, periods):
        """Будущая стоимость аннуитета"""
        if rate == 0:
            return payment * periods
        return payment * ((1 + rate)**periods - 1) / rate
    
    def present_value(self, payment, rate, periods):
        """Приведенная стоимость аннуитета"""
        if rate == 0:
            return payment * periods
        return payment * (1 - (1 + rate)**(-periods)) / rate
    
    def roi(self, profit, investment):
        """Рентабельность инвестиций (ROI) в процентах"""
        return round((profit / investment - 1) * 100, 2)
    
    def inflation_adjust(self, amount, rate, years):
        """Корректировка на инфляцию"""
        return amount / (1 + rate)**years

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
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.configure(highlightthickness=0)
    
    def get_bg_color(self):
        return {
            'normal': COLORS['btn_normal'],
            'operator': COLORS['btn_operator'],
            'equal': COLORS['btn_equal'],
            'clear': COLORS['btn_clear'],
            'special': COLORS['btn_special'],
            'memory': COLORS['btn_memory'],
            'finance': COLORS['btn_finance'],
            'converter': COLORS['btn_converter']
        }.get(self.color_type, COLORS['btn_normal'])
    
    def get_fg_color(self):
        return {
            'normal': COLORS['btn_normal_text'],
            'operator': COLORS['btn_operator_text'],
            'equal': COLORS['btn_equal_text'],
            'clear': COLORS['btn_clear_text'],
            'special': COLORS['btn_special_text'],
            'memory': COLORS['btn_memory_text'],
            'finance': COLORS['btn_finance_text'],
            'converter': COLORS['btn_converter_text']
        }.get(self.color_type, COLORS['btn_normal_text'])
    
    def get_hover_color(self):
        hover_map = {
            'normal': "#505dd2",
            'operator': '#b4befe',
            'equal': "#c873c9",
            'clear': '#f9e2af',
            'special': '#f5c2e7',
            'memory': "#999ec2",
            'finance': "#f5e0dc",
            'converter': "#b7bdf8"
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
        self.configure(highlightbackground=COLORS['bg'], highlightthickness=2)


class SimpleCalculator:
    """Обычный калькулятор с красивым интерфейсом"""
    def __init__(self, parent, shared_memory, add_to_history, variables):
        self.parent = parent
        self.shared_memory = shared_memory
        self.add_to_history = add_to_history
        self.variables = variables
        self.expression = ""
        
        parent.configure(bg=COLORS['bg'])
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
        buttons_frame = tk.Frame(parent, bg=COLORS['bg'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
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
        
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
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
            # Подстановка переменных
            for var_name, var_value in self.variables.variables.items():
                expr = expr.replace(var_name, str(var_value))
            
            result = eval(expr)
            result = round(result, 10)
            self.variables.set_var('ans', result)
            self.add_to_history(f"{self.display_var.get()} = {result}")
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
            result = round(math.sqrt(current), 10)
            self.add_to_history(f"√({current}) = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def square(self):
        try:
            current = float(self.display_var.get())
            result = round(current ** 2, 10)
            self.add_to_history(f"{current}² = {result}")
            self.display_var.set(str(result))
        except:
            pass
    
    def reciprocal(self):
        try:
            current = float(self.display_var.get())
            result = round(1 / current, 10)
            self.add_to_history(f"1/{current} = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")


class ScientificCalculator:
    """Научный калькулятор с красивым интерфейсом"""
    def __init__(self, parent, shared_memory, add_to_history, variables):
        self.parent = parent
        self.shared_memory = shared_memory
        self.add_to_history = add_to_history
        self.variables = variables
        
        parent.configure(bg=COLORS['bg'])
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
        buttons_frame = tk.Frame(parent, bg=COLORS['bg'])
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        row1 = [('sin', 0, 0, 'special'), ('cos', 0, 1, 'special'), ('tan', 0, 2, 'special'),
                ('log', 0, 3, 'special'), ('ln', 0, 4, 'special'), ('C', 0, 5, 'clear')]
        row2 = [('7', 1, 0, 'normal'), ('8', 1, 1, 'normal'), ('9', 1, 2, 'normal'),
                ('^', 1, 3, 'operator'), ('√', 1, 4, 'special'), ('(', 1, 5, 'operator')]
        row3 = [('4', 2, 0, 'normal'), ('5', 2, 1, 'normal'), ('6', 2, 2, 'normal'),
                ('*', 2, 3, 'operator'), ('/', 2, 4, 'operator'), (')', 2, 5, 'operator')]
        row4 = [('1', 3, 0, 'normal'), ('2', 3, 1, 'normal'), ('3', 3, 2, 'normal'),
                ('+', 3, 3, 'operator'), ('-', 3, 4, 'operator'), ('=', 3, 5, 'equal')]
        row5 = [('0', 4, 0, 'normal'), ('.', 4, 1, 'normal'), ('±', 4, 2, 'special'),
                ('π', 4, 3, 'special'), ('e', 4, 4, 'special'), ('!', 4, 5, 'special')]
        row6 = [('sinh', 5, 0, 'special'), ('cosh', 5, 1, 'special'), ('tanh', 5, 2, 'special'),
                ('|x|', 5, 3, 'special'), ('10^x', 5, 4, 'special'), ('mod', 5, 5, 'special')]
        
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
        elif key == '!':
            self.factorial()
        elif key == '|x|':
            self.absolute()
        elif key == 'mod':
            self.modulo()
        elif key == '10^x':
            self.power_of_10()
        elif key in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'log', 'ln']:
            self.scientific_func(key)
        elif key == '(' or key == ')':
            self.add_paren(key)
    
    def number_click(self, num):
        current = self.display_var.get()
        if current == "0" or current == "Ошибка":
            self.display_var.set(num)
        else:
            self.display_var.set(current + num)
    
    def operator_click(self, op):
        current = self.display_var.get()
        if current and not current.endswith('.'):
            self.display_var.set(current + op)
    
    def add_paren(self, paren):
        current = self.display_var.get()
        if current == "0":
            self.display_var.set(paren)
        else:
            self.display_var.set(current + paren)
    
    def scientific_func(self, func_name):
        try:
            current = float(self.display_var.get())
            func_map = {
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
                'sinh': math.sinh,
                'cosh': math.cosh,
                'tanh': math.tanh,
                'log': math.log10,
                'ln': math.log,
            }
            result = round(func_map[func_name](current), 10)
            self.add_to_history(f"{func_name}({current}) = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def factorial(self):
        try:
            current = int(float(self.display_var.get()))
            if current < 0:
                raise ValueError
            result = math.factorial(current)
            self.add_to_history(f"{current}! = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def absolute(self):
        try:
            current = float(self.display_var.get())
            result = abs(current)
            self.add_to_history(f"|{current}| = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def modulo(self):
        current = self.display_var.get()
        if current and not current.endswith(' mod '):
            self.display_var.set(current + ' % ')
    
    def power_of_10(self):
        try:
            current = float(self.display_var.get())
            result = round(10 ** current, 10)
            self.add_to_history(f"10^{current} = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def calculate(self):
        try:
            expr = self.display_var.get()
            expr = expr.replace('^', '**')
            
            # Подстановка переменных
            for var_name, var_value in self.variables.variables.items():
                expr = expr.replace(var_name, str(var_value))
            
            result = eval(expr)
            result = round(result, 10)
            self.variables.set_var('ans', result)
            self.add_to_history(f"{self.display_var.get()} = {result}")
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
            result = round(math.sqrt(current), 10)
            self.add_to_history(f"√({current}) = {result}")
            self.display_var.set(str(result))
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
        self.pending_operation = None
        self.stored_value = 0
        
        parent.configure(bg=COLORS['bg'])
        
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
        
        self.oct_btn = ModernButton(base_frame, text="OCT", color_type='normal',
                                    command=lambda: self.set_base("OCT"))
        self.oct_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
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
                ('M-', 4, 3, 'memory'), ('ROL', 4, 4, 'special'), ('ROR', 4, 5, 'special')]
        
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
        for btn, base in [(self.dec_btn, "DEC"), (self.hex_btn, "HEX"), 
                         (self.bin_btn, "BIN"), (self.oct_btn, "OCT")]:
            if base == self.current_base:
                btn.config(bg=COLORS['btn_special'], fg=COLORS['btn_special_text'])
            else:
                btn.config(bg=COLORS['btn_normal'], fg=COLORS['btn_normal_text'])
    
    def update_display(self):
        if self.current_base == "DEC":
            self.display_var.set(str(self.current_value & 0xFFFFFFFF))
        elif self.current_base == "HEX":
            self.display_var.set(hex(self.current_value & 0xFFFFFFFF)[2:].upper())
        elif self.current_base == "BIN":
            self.display_var.set(bin(self.current_value & 0xFFFFFFFF)[2:])
        elif self.current_base == "OCT":
            self.display_var.set(oct(self.current_value & 0xFFFFFFFF)[2:])
    
    def get_input_value(self):
        text = self.display_var.get()
        try:
            if self.current_base == "DEC":
                return int(text) if text else 0
            elif self.current_base == "HEX":
                return int(text, 16) if text else 0
            elif self.current_base == "BIN":
                return int(text, 2) if text else 0
            elif self.current_base == "OCT":
                return int(text, 8) if text else 0
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
            self.calculate()
        elif key == 'C':
            self.current_value = 0
            self.pending_operation = None
            self.stored_value = 0
            self.update_display()
        elif key == '<<':
            self.current_value = (self.current_value << 1) & 0xFFFFFFFF
            self.update_display()
            self.add_to_history(f"Сдвиг влево: {self.display_var.get()}")
        elif key == '>>':
            self.current_value = (self.current_value >> 1) & 0xFFFFFFFF
            self.update_display()
            self.add_to_history(f"Сдвиг вправо: {self.display_var.get()}")
        elif key == 'ROL':
            # Циклический сдвиг влево
            msb = (self.current_value >> 31) & 1
            self.current_value = ((self.current_value << 1) | msb) & 0xFFFFFFFF
            self.update_display()
        elif key == 'ROR':
            # Циклический сдвиг вправо
            lsb = self.current_value & 1
            self.current_value = (self.current_value >> 1) | (lsb << 31)
            self.update_display()
        elif key in ['AND', 'OR', 'XOR']:
            self.pending_operation = key
            self.stored_value = self.get_input_value()
            self.current_value = 0
            self.display_var.set("0")
        elif key == 'NOT':
            self.current_value = ~self.current_value & 0xFFFFFFFF
            self.update_display()
        elif key == 'MC':
            self.shared_memory[0] = 0
        elif key == 'MR':
            self.current_value = self.shared_memory[0] & 0xFFFFFFFF
            self.update_display()
        elif key == 'M+':
            self.shared_memory[0] = (self.shared_memory[0] + self.current_value) & 0xFFFFFFFF
        elif key == 'M-':
            self.shared_memory[0] = (self.shared_memory[0] - self.current_value) & 0xFFFFFFFF
    
    def calculate(self):
        if self.pending_operation:
            current_val = self.get_input_value()
            if self.pending_operation == 'AND':
                self.current_value = self.stored_value & current_val
            elif self.pending_operation == 'OR':
                self.current_value = self.stored_value | current_val
            elif self.pending_operation == 'XOR':
                self.current_value = self.stored_value ^ current_val
            
            self.current_value &= 0xFFFFFFFF
            self.pending_operation = None
            self.stored_value = 0
            self.update_display()
    
    def number_click(self, num):
        current = self.display_var.get()
        if current == "0" or current == "Ошибка":
            self.display_var.set(num)
        else:
            self.display_var.set(current + num)
        self.current_value = self.get_input_value()


class GraphCalculator:
    """Графический калькулятор для построения графиков функций"""
    def __init__(self, parent, add_to_history, variables):
        self.parent = parent
        self.add_to_history = add_to_history
        self.variables = variables
        
        parent.configure(bg=COLORS['bg'])
        
        if not MATPLOTLIB_AVAILABLE:
            label = tk.Label(parent, text="⚠️ Для работы графика установите:\nmatplotlib и numpy\n\npip install matplotlib numpy",
                           font=('Segoe UI', 12), bg=COLORS['bg'], fg=COLORS['display_text'],
                           justify=tk.CENTER)
            label.pack(expand=True)
            return
        
        # Верхняя панель с вводом функции
        input_frame = tk.Frame(parent, bg=COLORS['bg'])
        input_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(input_frame, text="f(x) =", font=('Segoe UI', 12, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=(0, 10))
        
        self.func_var = tk.StringVar()
        self.func_var.set("sin(x)")
        
        self.func_entry = tk.Entry(input_frame, textvariable=self.func_var,
                                   font=('Consolas', 12), bg=COLORS['display'],
                                   fg=COLORS['display_text'], relief=tk.FLAT,
                                   insertbackground=COLORS['display_text'])
        self.func_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        plot_btn = ModernButton(input_frame, text="Построить", color_type='equal',
                                command=self.plot_function)
        plot_btn.pack(side=tk.RIGHT)
        
        # Параметры графика
        params_frame = tk.Frame(parent, bg=COLORS['bg'])
        params_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(params_frame, text="X min:", font=('Segoe UI', 10),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.xmin_var = tk.StringVar(value="-10")
        xmin_entry = tk.Entry(params_frame, textvariable=self.xmin_var, width=6,
                              font=('Consolas', 10), bg=COLORS['display'],
                              fg=COLORS['display_text'], relief=tk.FLAT)
        xmin_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(params_frame, text="X max:", font=('Segoe UI', 10),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.xmax_var = tk.StringVar(value="10")
        xmax_entry = tk.Entry(params_frame, textvariable=self.xmax_var, width=6,
                              font=('Consolas', 10), bg=COLORS['display'],
                              fg=COLORS['display_text'], relief=tk.FLAT)
        xmax_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(params_frame, text="Точек:", font=('Segoe UI', 10),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=(0, 5))
        
        self.points_var = tk.StringVar(value="500")
        points_entry = tk.Entry(params_frame, textvariable=self.points_var, width=6,
                                font=('Consolas', 10), bg=COLORS['display'],
                                fg=COLORS['display_text'], relief=tk.FLAT)
        points_entry.pack(side=tk.LEFT)
        
        # Кнопки быстрых функций
        quick_frame = tk.Frame(parent, bg=COLORS['bg'])
        quick_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        quick_funcs = [
            ('sin(x)', 'sin(x)'), ('cos(x)', 'cos(x)'), ('tan(x)', 'tan(x)'),
            ('x²', 'x**2'), ('√x', 'sqrt(x)'), ('1/x', '1/x'),
            ('e^x', 'exp(x)'), ('ln(x)', 'log(x)'), ('|x|', 'abs(x)')
        ]
        
        for text, func in quick_funcs:
            btn = ModernButton(quick_frame, text=text, color_type='special',
                              command=lambda f=func: self.set_function(f))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Область для графика
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor=COLORS['display'])
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor(COLORS['display'])
        self.ax.tick_params(colors=COLORS['display_text'])
        self.ax.spines['bottom'].set_color(COLORS['display_text'])
        self.ax.spines['top'].set_color(COLORS['display_text'])
        self.ax.spines['left'].set_color(COLORS['display_text'])
        self.ax.spines['right'].set_color(COLORS['display_text'])
        self.ax.xaxis.label.set_color(COLORS['display_text'])
        self.ax.yaxis.label.set_color(COLORS['display_text'])
        self.ax.title.set_color(COLORS['display_text'])
        
        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.func_entry.bind('<Return>', lambda e: self.plot_function())
        
        self.plot_function()
    
    def set_function(self, func):
        self.func_var.set(func)
        self.plot_function()
    
    def plot_function(self):
        try:
            x_min = float(self.xmin_var.get())
            x_max = float(self.xmax_var.get())
            points = int(self.points_var.get())
            
            if x_min >= x_max:
                raise ValueError("X min должен быть меньше X max")
            
            x = np.linspace(x_min, x_max, points)
            y = []
            func_str = self.func_var.get()
            
            safe_dict = {
                'x': 0, 'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                'sqrt': np.sqrt, 'exp': np.exp, 'log': np.log, 'log10': np.log10,
                'abs': np.abs, 'pi': np.pi, 'e': np.e, 'sinh': np.sinh,
                'cosh': np.cosh, 'tanh': np.tanh, 'arcsin': np.arcsin,
                'arccos': np.arccos, 'arctan': np.arctan
            }
            
            # Добавляем пользовательские переменные
            for var_name, var_value in self.variables.variables.items():
                safe_dict[var_name] = var_value
            
            for xi in x:
                try:
                    safe_dict['x'] = xi
                    yi = eval(func_str, {"__builtins__": {}}, safe_dict)
                    if abs(yi) > 1e6:
                        yi = np.nan
                    y.append(yi)
                except:
                    y.append(np.nan)
            
            y = np.array(y)
            
            self.ax.clear()
            self.ax.plot(x, y, color=COLORS['btn_special'], linewidth=2)
            self.ax.axhline(y=0, color=COLORS['display_text'], linewidth=0.5, alpha=0.5)
            self.ax.axvline(x=0, color=COLORS['display_text'], linewidth=0.5, alpha=0.5)
            self.ax.grid(True, alpha=0.3, color=COLORS['display_text'])
            self.ax.set_xlabel('x', fontsize=10)
            self.ax.set_ylabel('f(x)', fontsize=10)
            self.ax.set_title(f'f(x) = {func_str}', fontsize=12, fontweight='bold')
            self.ax.set_facecolor(COLORS['display'])
            self.ax.tick_params(colors=COLORS['display_text'])
            
            for spine in self.ax.spines.values():
                spine.set_color(COLORS['display_text'])
            
            self.canvas.draw()
            self.add_to_history(f"📈 Построен график: f(x) = {func_str}, x ∈ [{x_min}, {x_max}]")
            
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f'Ошибка: {str(e)}', 
                        transform=self.ax.transAxes, ha='center', va='center',
                        color='red', fontsize=12)
            self.canvas.draw()


class FractionCalculatorTab:
    """Вкладка калькулятора дробей"""
    def __init__(self, parent, add_to_history):
        self.parent = parent
        self.add_to_history = add_to_history
        self.fraction_calc = FractionCalculator()
        
        parent.configure(bg=COLORS['bg'])
        
        # Заголовок
        title_frame = tk.Frame(parent, bg=COLORS['bg'])
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="🧮 Калькулятор дробей", font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack()
        
        # Дисплей
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        display_frame = tk.Frame(parent, bg=COLORS['bg'])
        display_frame.pack(fill=tk.X, padx=15, pady=5)
        
        self.display = ModernDisplay(display_frame, self.display_var)
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Ввод дроби
        fraction_input_frame = tk.Frame(parent, bg=COLORS['bg'])
        fraction_input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(fraction_input_frame, text="Числитель:", bg=COLORS['bg'], 
                fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        self.num_var = tk.StringVar(value="1")
        num_entry = tk.Entry(fraction_input_frame, textvariable=self.num_var, width=10,
                            font=('Consolas', 12), bg=COLORS['display'],
                            fg=COLORS['display_text'])
        num_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(fraction_input_frame, text="/", font=('Segoe UI', 16, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        
        tk.Label(fraction_input_frame, text="Знаменатель:", bg=COLORS['bg'], 
                fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        self.den_var = tk.StringVar(value="1")
        den_entry = tk.Entry(fraction_input_frame, textvariable=self.den_var, width=10,
                            font=('Consolas', 12), bg=COLORS['display'],
                            fg=COLORS['display_text'])
        den_entry.pack(side=tk.LEFT, padx=5)
        
        simplify_btn = ModernButton(fraction_input_frame, text="Упростить", 
                                   color_type='special', command=self.simplify_fraction)
        simplify_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопки операций
        ops_frame = tk.Frame(parent, bg=COLORS['bg'])
        ops_frame.pack(fill=tk.X, padx=15, pady=10)
        
        operations = [
            ('+', ' + '), ('-', ' - '), ('×', ' * '), ('÷', ' / '),
        ]
        
        for text, op in operations:
            btn = ModernButton(ops_frame, text=text, color_type='operator',
                              command=lambda o=op: self.add_operation(o))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Кнопки действий
        actions_frame = tk.Frame(parent, bg=COLORS['bg'])
        actions_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        clear_btn = ModernButton(actions_frame, text="C", color_type='clear',
                                command=self.clear)
        clear_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        backspace_btn = ModernButton(actions_frame, text="⌫", color_type='clear',
                                    command=self.backspace)
        backspace_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        equal_btn = ModernButton(actions_frame, text="=", color_type='equal',
                                command=self.calculate)
        equal_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
    
    def add_operation(self, op):
        current = self.display_var.get()
        if current != "0" and current != "Ошибка":
            self.display_var.set(current + op)
    
    def calculate(self):
        try:
            expr = self.display_var.get()
            result = self.fraction_calc.calculate(expr)
            self.add_to_history(f"{expr} = {result}")
            self.display_var.set(str(result))
        except:
            self.display_var.set("Ошибка")
    
    def simplify_fraction(self):
        try:
            num = int(self.num_var.get())
            den = int(self.den_var.get())
            if den == 0:
                self.display_var.set("Ошибка: деление на 0")
                return
            
            result = self.fraction_calc.simplify(num, den)
            self.display_var.set(result)
            self.add_to_history(f"Упрощение: {num}/{den} = {result}")
        except:
            self.display_var.set("Ошибка")
    
    def clear(self):
        self.display_var.set("0")
    
    def backspace(self):
        current = self.display_var.get()
        if len(current) > 1:
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")


class DateCalculatorTab:
    """Вкладка калькулятора дат"""
    def __init__(self, parent, add_to_history):
        self.parent = parent
        self.add_to_history = add_to_history
        self.date_calc = DateCalculator()
        
        parent.configure(bg=COLORS['bg'])
        
        # Заголовок
        title_frame = tk.Frame(parent, bg=COLORS['bg'])
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="📅 Калькулятор дат", font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack()
        
        # Ввод дат
        date_frame = tk.Frame(parent, bg=COLORS['bg'])
        date_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Дата 1
        tk.Label(date_frame, text="Дата 1 (ГГГГ-ММ-ДД):", bg=COLORS['bg'], 
                fg=COLORS['display_text']).grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.date1_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date1_entry = tk.Entry(date_frame, textvariable=self.date1_var, width=15,
                              font=('Consolas', 12), bg=COLORS['display'],
                              fg=COLORS['display_text'])
        date1_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Дата 2
        tk.Label(date_frame, text="Дата 2 (ГГГГ-ММ-ДД):", bg=COLORS['bg'], 
                fg=COLORS['display_text']).grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.date2_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date2_entry = tk.Entry(date_frame, textvariable=self.date2_var, width=15,
                              font=('Consolas', 12), bg=COLORS['display'],
                              fg=COLORS['display_text'])
        date2_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Кнопки операций
        ops_frame = tk.Frame(parent, bg=COLORS['bg'])
        ops_frame.pack(fill=tk.X, padx=15, pady=10)
        
        diff_btn = ModernButton(ops_frame, text="Разница в днях", color_type='special',
                               command=self.days_between)
        diff_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Добавление дней
        add_frame = tk.Frame(parent, bg=COLORS['bg'])
        add_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(add_frame, text="Добавить дней:", bg=COLORS['bg'], 
                fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        self.days_var = tk.StringVar(value="0")
        days_entry = tk.Entry(add_frame, textvariable=self.days_var, width=10,
                             font=('Consolas', 12), bg=COLORS['display'],
                             fg=COLORS['display_text'])
        days_entry.pack(side=tk.LEFT, padx=5)
        
        add_days_btn = ModernButton(add_frame, text="Вычислить", color_type='equal',
                                   command=self.add_days)
        add_days_btn.pack(side=tk.LEFT, padx=5)
        
        # Добавление месяцев
        month_frame = tk.Frame(parent, bg=COLORS['bg'])
        month_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(month_frame, text="Добавить месяцев:", bg=COLORS['bg'], 
                fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        self.months_var = tk.StringVar(value="0")
        months_entry = tk.Entry(month_frame, textvariable=self.months_var, width=10,
                               font=('Consolas', 12), bg=COLORS['display'],
                               fg=COLORS['display_text'])
        months_entry.pack(side=tk.LEFT, padx=5)
        
        add_months_btn = ModernButton(month_frame, text="Вычислить", color_type='equal',
                                     command=self.add_months)
        add_months_btn.pack(side=tk.LEFT, padx=5)
        
        # Дополнительные функции
        extra_frame = tk.Frame(parent, bg=COLORS['bg'])
        extra_frame.pack(fill=tk.X, padx=15, pady=10)
        
        leap_btn = ModernButton(extra_frame, text="Високосный год?", color_type='special',
                               command=self.check_leap_year)
        leap_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        dow_btn = ModernButton(extra_frame, text="День недели", color_type='special',
                              command=self.day_of_week)
        dow_btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Результат
        self.result_var = tk.StringVar()
        self.result_var.set("Результат появится здесь")
        
        result_label = tk.Label(parent, textvariable=self.result_var,
                               font=('Segoe UI', 12, 'bold'),
                               bg=COLORS['display'], fg=COLORS['display_text'],
                               padx=15, pady=15)
        result_label.pack(fill=tk.X, padx=15, pady=(10, 15))
    
    def parse_date(self, date_str):
        """Парсинг даты из строки"""
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return None
    
    def days_between(self):
        date1 = self.parse_date(self.date1_var.get())
        date2 = self.parse_date(self.date2_var.get())
        
        if date1 and date2:
            days = self.date_calc.days_between(date1, date2)
            self.result_var.set(f"Разница: {abs(days)} дней")
            self.add_to_history(f"Дней между {date1.date()} и {date2.date()}: {abs(days)}")
        else:
            self.result_var.set("Ошибка: неверный формат даты")
    
    def add_days(self):
        date = self.parse_date(self.date1_var.get())
        try:
            days = int(self.days_var.get())
            if date:
                new_date = self.date_calc.add_days(date, days)
                self.result_var.set(f"Результат: {self.date_calc.format_date(new_date)}")
                self.add_to_history(f"{date.date()} + {days} дней = {new_date.date()}")
        except:
            self.result_var.set("Ошибка: введите корректное число дней")
    
    def add_months(self):
        date = self.parse_date(self.date1_var.get())
        try:
            months = int(self.months_var.get())
            if date:
                new_date = self.date_calc.add_months(date, months)
                self.result_var.set(f"Результат: {self.date_calc.format_date(new_date)}")
                self.add_to_history(f"{date.date()} + {months} месяцев = {new_date.date()}")
        except:
            self.result_var.set("Ошибка: введите корректное число месяцев")
    
    def check_leap_year(self):
        date = self.parse_date(self.date1_var.get())
        if date:
            is_leap = self.date_calc.is_leap_year(date.year)
            self.result_var.set(f"{date.year} год {'високосный' if is_leap else 'не високосный'}")
    
    def day_of_week(self):
        date = self.parse_date(self.date1_var.get())
        if date:
            dow = self.date_calc.day_of_week(date)
            self.result_var.set(f"День недели: {dow}")


class FinancialCalculatorTab:
    """Вкладка финансового калькулятора"""
    def __init__(self, parent, add_to_history):
        self.parent = parent
        self.add_to_history = add_to_history
        self.finance_calc = FinancialCalculator()
        
        parent.configure(bg=COLORS['bg'])
        
        # Заголовок
        title_frame = tk.Frame(parent, bg=COLORS['bg'])
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="💰 Финансовый калькулятор", font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack()
        
        # Создаем прокручиваемую область
        canvas = tk.Canvas(parent, bg=COLORS['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLORS['bg'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Сложный процент
        self.create_compound_interest_section(scrollable_frame)
        
        # Кредитный калькулятор
        self.create_loan_section(scrollable_frame)
        
        # Инвестиции
        self.create_investment_section(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True, padx=15)
        scrollbar.pack(side="right", fill="y")
    
    def create_compound_interest_section(self, parent):
        """Секция сложного процента"""
        frame = tk.LabelFrame(parent, text="Сложный процент", bg=COLORS['bg'],
                             fg=COLORS['display_text'], font=('Segoe UI', 11, 'bold'))
        frame.pack(fill=tk.X, pady=10)
        
        fields = [
            ("Начальная сумма:", "100000"),
            ("Годовая ставка (%):", "5"),
            ("Срок (лет):", "10"),
            ("Начислений в год:", "12"),
        ]
        
        self.ci_vars = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(frame, text=label, bg=COLORS['bg'], fg=COLORS['display_text']).grid(
                row=i, column=0, sticky='w', padx=10, pady=5)
            var = tk.StringVar(value=default)
            entry = tk.Entry(frame, textvariable=var, width=15,
                           font=('Consolas', 10), bg=COLORS['display'],
                           fg=COLORS['display_text'])
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.ci_vars[label] = var
        
        self.ci_result_var = tk.StringVar(value="Результат: ")
        result_label = tk.Label(frame, textvariable=self.ci_result_var,
                               font=('Segoe UI', 11, 'bold'),
                               bg=COLORS['display'], fg=COLORS['display_text'],
                               padx=10, pady=10)
        result_label.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
        calc_btn = ModernButton(frame, text="Рассчитать", color_type='finance',
                               command=self.calc_compound_interest)
        calc_btn.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
    
    def create_loan_section(self, parent):
        """Секция кредитного калькулятора"""
        frame = tk.LabelFrame(parent, text="Кредитный калькулятор", bg=COLORS['bg'],
                             fg=COLORS['display_text'], font=('Segoe UI', 11, 'bold'))
        frame.pack(fill=tk.X, pady=10)
        
        fields = [
            ("Сумма кредита:", "1000000"),
            ("Годовая ставка (%):", "12"),
            ("Срок (месяцев):", "60"),
        ]
        
        self.loan_vars = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(frame, text=label, bg=COLORS['bg'], fg=COLORS['display_text']).grid(
                row=i, column=0, sticky='w', padx=10, pady=5)
            var = tk.StringVar(value=default)
            entry = tk.Entry(frame, textvariable=var, width=15,
                           font=('Consolas', 10), bg=COLORS['display'],
                           fg=COLORS['display_text'])
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.loan_vars[label] = var
        
        self.loan_result_var = tk.StringVar(value="Результат: ")
        result_label = tk.Label(frame, textvariable=self.loan_result_var,
                               font=('Segoe UI', 11, 'bold'),
                               bg=COLORS['display'], fg=COLORS['display_text'],
                               padx=10, pady=10)
        result_label.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
        calc_btn = ModernButton(frame, text="Рассчитать", color_type='finance',
                               command=self.calc_loan)
        calc_btn.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
    
    def create_investment_section(self, parent):
        """Секция инвестиций"""
        frame = tk.LabelFrame(parent, text="Инвестиции (ROI)", bg=COLORS['bg'],
                             fg=COLORS['display_text'], font=('Segoe UI', 11, 'bold'))
        frame.pack(fill=tk.X, pady=10)
        
        fields = [
            ("Вложенная сумма:", "100000"),
            ("Полученная сумма:", "150000"),
        ]
        
        self.inv_vars = {}
        for i, (label, default) in enumerate(fields):
            tk.Label(frame, text=label, bg=COLORS['bg'], fg=COLORS['display_text']).grid(
                row=i, column=0, sticky='w', padx=10, pady=5)
            var = tk.StringVar(value=default)
            entry = tk.Entry(frame, textvariable=var, width=15,
                           font=('Consolas', 10), bg=COLORS['display'],
                           fg=COLORS['display_text'])
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.inv_vars[label] = var
        
        self.inv_result_var = tk.StringVar(value="Результат: ")
        result_label = tk.Label(frame, textvariable=self.inv_result_var,
                               font=('Segoe UI', 11, 'bold'),
                               bg=COLORS['display'], fg=COLORS['display_text'],
                               padx=10, pady=10)
        result_label.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=10, sticky='ew')
        
        calc_btn = ModernButton(frame, text="Рассчитать", color_type='finance',
                               command=self.calc_roi)
        calc_btn.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=5, sticky='ew')
    
    def calc_compound_interest(self):
        try:
            principal = float(self.ci_vars["Начальная сумма:"].get())
            rate = float(self.ci_vars["Годовая ставка (%):"].get()) / 100
            time = float(self.ci_vars["Срок (лет):"].get())
            n = int(self.ci_vars["Начислений в год:"].get())
            
            result = self.finance_calc.compound_interest(principal, rate, time, n)
            profit = result - principal
            
            self.ci_result_var.set(
                f"Итоговая сумма: {result:,.2f} | Доход: {profit:,.2f}"
            )
            self.add_to_history(f"Сложный процент: {principal} под {rate*100}% на {time} лет = {result:,.2f}")
        except:
            self.ci_result_var.set("Ошибка: проверьте введенные данные")
    
    def calc_loan(self):
        try:
            principal = float(self.loan_vars["Сумма кредита:"].get())
            rate = float(self.loan_vars["Годовая ставка (%):"].get()) / 100
            months = int(self.loan_vars["Срок (месяцев):"].get())
            
            payment = self.finance_calc.loan_payment(principal, rate, months)
            total = self.finance_calc.total_loan_cost(principal, rate, months)
            overpayment = total - principal
            
            self.loan_result_var.set(
                f"Ежемесячный платеж: {payment:,.2f} | Переплата: {overpayment:,.2f} | Всего: {total:,.2f}"
            )
            self.add_to_history(f"Кредит: {principal} на {months} мес. под {rate*100}%, платеж: {payment:,.2f}")
        except:
            self.loan_result_var.set("Ошибка: проверьте введенные данные")
    
    def calc_roi(self):
        try:
            investment = float(self.inv_vars["Вложенная сумма:"].get())
            profit = float(self.inv_vars["Полученная сумма:"].get())
            
            roi = self.finance_calc.roi(profit, investment)
            
            self.inv_result_var.set(f"ROI: {roi}% | Доход: {profit - investment:,.2f}")
            self.add_to_history(f"ROI: вложено {investment}, получено {profit} = {roi}%")
        except:
            self.inv_result_var.set("Ошибка: проверьте введенные данные")


class UnitConverterTab:
    """Вкладка конвертера единиц"""
    def __init__(self, parent, add_to_history):
        self.parent = parent
        self.add_to_history = add_to_history
        self.converter = UnitConverter()
        self.currency_converter = CurrencyConverter()
        
        parent.configure(bg=COLORS['bg'])
        
        # Заголовок
        title_frame = tk.Frame(parent, bg=COLORS['bg'])
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        tk.Label(title_frame, text="🔄 Конвертер единиц", font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack()
        
        # Выбор типа конвертации
        type_frame = tk.Frame(parent, bg=COLORS['bg'])
        type_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.conversion_type = tk.StringVar(value="длина")
        types = ["длина", "масса", "температура", "площадь", "объем", "скорость", "валюта"]
        
        for t in types:
            btn = ModernButton(type_frame, text=t.capitalize(), color_type='converter',
                              command=lambda x=t: self.set_conversion_type(x))
            btn.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Область ввода
        input_frame = tk.Frame(parent, bg=COLORS['bg'])
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.value_var = tk.StringVar(value="1")
        value_entry = tk.Entry(input_frame, textvariable=self.value_var, width=15,
                              font=('Consolas', 14), bg=COLORS['display'],
                              fg=COLORS['display_text'])
        value_entry.pack(pady=5)
        
        # Выбор единиц
        units_frame = tk.Frame(parent, bg=COLORS['bg'])
        units_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(units_frame, text="Из:", bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        
        self.from_unit_var = tk.StringVar()
        self.from_menu = ttk.Combobox(units_frame, textvariable=self.from_unit_var, width=15)
        self.from_menu.pack(side=tk.LEFT, padx=5)
        
        tk.Label(units_frame, text="→", font=('Segoe UI', 16, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=10)
        
        tk.Label(units_frame, text="В:", bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT, padx=5)
        
        self.to_unit_var = tk.StringVar()
        self.to_menu = ttk.Combobox(units_frame, textvariable=self.to_unit_var, width=15)
        self.to_menu.pack(side=tk.LEFT, padx=5)
        
        convert_btn = ModernButton(units_frame, text="Конвертировать", color_type='converter',
                                  command=self.convert)
        convert_btn.pack(side=tk.LEFT, padx=10)
        
        # Результат
        self.result_var = tk.StringVar()
        self.result_var.set("Результат появится здесь")
        
        result_label = tk.Label(parent, textvariable=self.result_var,
                               font=('Segoe UI', 12, 'bold'),
                               bg=COLORS['display'], fg=COLORS['display_text'],
                               padx=15, pady=15)
        result_label.pack(fill=tk.X, padx=15, pady=(10, 15))
        
        self.set_conversion_type("длина")
    
    def set_conversion_type(self, conv_type):
        self.conversion_type.set(conv_type)
        
        if conv_type == "валюта":
            units = list(self.currency_converter.rates.keys())
        elif conv_type == "температура":
            units = ["Цельсий", "Фаренгейт", "Кельвин"]
        else:
            units = list(getattr(self.converter, conv_type, {}).keys())
        
        self.from_menu['values'] = units
        self.to_menu['values'] = units
        
        if units:
            self.from_unit_var.set(units[0])
            self.to_unit_var.set(units[-1])
    
    def convert(self):
        try:
            value = float(self.value_var.get())
            from_unit = self.from_unit_var.get()
            to_unit = self.to_unit_var.get()
            conv_type = self.conversion_type.get()
            
            if conv_type == "валюта":
                result = self.currency_converter.convert(value, from_unit, to_unit)
            else:
                result = self.converter.convert(value, from_unit, to_unit, conv_type)
            
            if result is not None:
                self.result_var.set(f"{value} {from_unit} = {result} {to_unit}")
                self.add_to_history(f"Конвертация: {value} {from_unit} → {result} {to_unit}")
            else:
                self.result_var.set("Ошибка конвертации")
        except:
            self.result_var.set("Ошибка: проверьте введенные данные")


class HistoryTab:
    """Вкладка истории с красивым оформлением"""
    def __init__(self, parent):
        self.parent = parent
        parent.configure(bg=COLORS['bg'])
        
        # Заголовок
        title_frame = tk.Frame(parent, bg=COLORS['bg'])
        title_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        tk.Label(title_frame, text="📜 История вычислений", font=('Segoe UI', 14, 'bold'),
                bg=COLORS['bg'], fg=COLORS['display_text']).pack(side=tk.LEFT)
        
        # Кнопки управления историей
        controls_frame = tk.Frame(parent, bg=COLORS['bg'])
        controls_frame.pack(fill=tk.X, padx=15, pady=5)
        
        export_btn = ModernButton(controls_frame, text="Экспорт CSV", color_type='special',
                                 command=self.export_to_csv)
        export_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = ModernButton(controls_frame, text="Сохранить", color_type='special',
                               command=self.save_history)
        save_btn.pack(side=tk.LEFT, padx=2)
        
        load_btn = ModernButton(controls_frame, text="Загрузить", color_type='special',
                               command=self.load_history)
        load_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ModernButton(controls_frame, text="Очистить", color_type='clear',
                                command=self.clear_history)
        clear_btn.pack(side=tk.RIGHT, padx=2)
        
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
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(5, 10))
        
        scrollbar = tk.Scrollbar(self.history_text, bg=COLORS['bg'])
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
    
    def add_entry(self, entry):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_text.insert(tk.END, f"[{timestamp}] {entry}\n")
        self.history_text.see(tk.END)
    
    def clear_history(self):
        if messagebox.askyesno("Очистка истории", "Вы уверены?"):
            self.history_text.delete(1.0, tk.END)
    
    def export_to_csv(self):
        """Экспорт истории в CSV файл"""
        try:
            history_content = self.history_text.get(1.0, tk.END).strip()
            if not history_content:
                messagebox.showwarning("Экспорт", "История пуста")
                return
            
            lines = history_content.split('\n')
            with open('calculator_history.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Entry'])
                for line in lines:
                    if '] ' in line:
                        timestamp, entry = line.split('] ', 1)
                        timestamp = timestamp[1:]  # убираем '['
                        writer.writerow([timestamp, entry])
            
            messagebox.showinfo("Успех", f"История экспортирована в calculator_history.csv ({len(lines)} записей)")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")
    
    def save_history(self):
        """Сохранение истории в JSON файл"""
        try:
            history_content = self.history_text.get(1.0, tk.END).strip()
            lines = history_content.split('\n') if history_content else []
            
            history_data = []
            for line in lines:
                if '] ' in line:
                    timestamp, entry = line.split('] ', 1)
                    timestamp = timestamp[1:]
                    history_data.append({
                        'timestamp': timestamp,
                        'entry': entry
                    })
            
            with open('calculator_history.json', 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo("Успех", f"История сохранена в calculator_history.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")
    
    def load_history(self):
        """Загрузка истории из JSON файла"""
        try:
            with open('calculator_history.json', 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            self.history_text.delete(1.0, tk.END)
            for item in history_data:
                self.history_text.insert(tk.END, f"[{item['timestamp']}] {item['entry']}\n")
            
            messagebox.showinfo("Успех", f"Загружено {len(history_data)} записей из истории")
        except FileNotFoundError:
            messagebox.showwarning("Загрузка", "Файл истории не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {str(e)}")


class MultiCalculator:
    """Главное окно с красивым интерфейсом"""
    def __init__(self, root):
        self.root = root
        self.root.title("✨ MultiCalc Pro — Многофункциональный калькулятор")
        self.root.geometry("850x900")
        self.root.configure(bg=COLORS['bg'])
        
        try:
            self.root.iconbitmap('calc.ico')
        except:
            pass
        
        self.shared_memory = [0]
        self.history = []
        self.variables = VariableManager()
        
        # Меню
        menubar = tk.Menu(root, bg=COLORS['bg'], fg=COLORS['display_text'])
        root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg'], fg=COLORS['display_text'])
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить историю", command=self.save_history)
        file_menu.add_command(label="Загрузить историю", command=self.load_history)
        file_menu.add_command(label="Экспорт в CSV", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=root.quit)
        
        view_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg'], fg=COLORS['display_text'])
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Тёмная тема", command=lambda: self.change_theme('dark'))
        view_menu.add_command(label="Светлая тема", command=lambda: self.change_theme('light'))
        
        help_menu = tk.Menu(menubar, tearoff=0, bg=COLORS['bg'], fg=COLORS['display_text'])
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=COLORS['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=COLORS['btn_normal'], 
                       foreground=COLORS['display_text'], padding=[15, 5],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', COLORS['btn_special'])])
        
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.simple_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.scientific_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.programmer_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.graph_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.fraction_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.date_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.finance_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.converter_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        self.history_frame = tk.Frame(self.notebook, bg=COLORS['bg'])
        
        self.notebook.add(self.simple_frame, text="🧮 Обычный")
        self.notebook.add(self.scientific_frame, text="🔬 Научный")
        self.notebook.add(self.programmer_frame, text="💻 Программист")
        self.notebook.add(self.graph_frame, text="📈 Графики")
        self.notebook.add(self.fraction_frame, text="🧮 Дроби")
        self.notebook.add(self.date_frame, text="📅 Даты")
        self.notebook.add(self.finance_frame, text="💰 Финансы")
        self.notebook.add(self.converter_frame, text="🔄 Конвертер")
        self.notebook.add(self.history_frame, text="📜 История")
        
        self.simple_calc = SimpleCalculator(self.simple_frame, self.shared_memory, 
                                           self.add_to_history, self.variables)
        self.scientific_calc = ScientificCalculator(self.scientific_frame, self.shared_memory, 
                                                   self.add_to_history, self.variables)
        self.programmer_calc = ProgrammerCalculator(self.programmer_frame, self.shared_memory, 
                                                   self.add_to_history)
        self.graph_calc = GraphCalculator(self.graph_frame, self.add_to_history, self.variables)
        self.fraction_calc_tab = FractionCalculatorTab(self.fraction_frame, self.add_to_history)
        self.date_calc_tab = DateCalculatorTab(self.date_frame, self.add_to_history)
        self.finance_calc_tab = FinancialCalculatorTab(self.finance_frame, self.add_to_history)
        self.converter_tab = UnitConverterTab(self.converter_frame, self.add_to_history)
        self.history_tab = HistoryTab(self.history_frame)
        
        self.status_var = tk.StringVar()
        self.status_var.set(f"💾 Память: {self.shared_memory[0]} | Переменных: {len(self.variables.variables)}")
        status_bar = tk.Label(
            root, textvariable=self.status_var,
            bg=COLORS['status_bg'], fg=COLORS['display_text'],
            font=('Segoe UI', 9), anchor='w', padx=10, pady=5
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.update_status()
    
    def add_to_history(self, entry):
        self.history.append(entry)
        self.history_tab.add_entry(entry)
    
    def update_status(self):
        self.status_var.set(
            f"💾 Память: {self.shared_memory[0]} | "
            f"Переменных: {len(self.variables.variables)} | "
            f"Записей в истории: {len(self.history)}"
        )
        self.root.after(1000, self.update_status)
    
    def change_theme(self, theme_name):
        """Смена темы оформления"""
        global COLORS
        if theme_name in THEMES:
            COLORS.update(THEMES[theme_name])
            messagebox.showinfo("Тема", f"Тема '{theme_name}' применена. Перезапустите для полного эффекта.")
    
    def save_history(self):
        self.history_tab.save_history()
    
    def load_history(self):
        self.history_tab.load_history()
    
    def export_history(self):
        self.history_tab.export_to_csv()
    
    def show_about(self):
        about_text = """
✨ MultiCalc Pro v2.0

Многофункциональный калькулятор с поддержкой:
• Обычных и научных вычислений
• Программистского режима
• Построения графиков функций
• Работы с дробями
• Финансовых расчетов
• Конвертации единиц измерения
• Работы с датами
• Системы переменных

Горячие клавиши:
Enter - вычислить
Цифры и операторы - ввод с клавиатуры

Автор: ИИ-ассистент
        """
        messagebox.showinfo("О программе", about_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiCalculator(root)
    root.mainloop()
