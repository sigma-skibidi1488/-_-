import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import os
import requests
import datetime
# Путь к папке лежит файл .py чтобы рядышком положить файл с логами
folder = os.path.dirname(os.path.abspath(__file__))
# Склеиваем путь к папке и имя файла
file_path = os.path.join(folder, "exchange_log.txt")


# команда для кнопки валют
def convert_any():
    # введённое кол-во
    user_input = entry_amount.get().strip()
    
    # Проверяем что введено норм число
    try:
        amount = float(user_input.replace(",", "."))
        if amount < 0:
            messagebox.showerror("Ошибка", "Количество не может быть отрицательным!")
            return
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число!")
        return

    # получаем выбранные валюты
    cur_from = combo_from.get()
    cur_to = combo_to.get()

    # Запрос к апи
    try:
        url = "https://open.er-api.com/v6/latest/EUR"
        data = requests.get(url).json()
        rates = data["rates"]
    except Exception as e:
        messagebox.showerror("Ошибка сети", f"Не удалось загрузить курсы: {e}")
        return

    # Считаем результат и курс за единицу
    unit_rate = (1 / rates[cur_from]) * rates[cur_to]
    total_result = amount * unit_rate

    # Строка с выводом и сравнением
    result_text = f"{amount:,.2f} {cur_from} = {total_result:,.2f} {cur_to}\n(1 {cur_from} = {unit_rate:.4f} {cur_to})"
    label_result.config(text=result_text, fg="#1a73e8")

    # Запись в лог
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_now}] {amount:.2f} {cur_from} -> {total_result:.2f} {cur_to} (Курс: {unit_rate:.4f})\n"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(log_line)
        
    label_status.config(text="Записано в currency_log.txt", fg="green")

# ткинтер 
root = tk.Tk()
root.title("Универсальный конвертер валют")
root.geometry("400x340")
root.resizable(False, False)

currencies = ["USD", "EUR", "RUB", "KZT", "JPY", "CNY", "BYN"]

# Поле для ввода суммы
label_amt = tk.Label(root, text="Сумма для перевода:", font=("Segoe UI", 10))
label_amt.pack(pady=(10, 2))

entry_amount = tk.Entry(root, font=("Segoe UI", 11), width=15, justify="center")
entry_amount.insert(0, "100") # Сразу ставим 100 по умолчанию
entry_amount.pack(pady=2)

# Блок выбора валют 
frame_cur = tk.Frame(root)
frame_cur.pack(pady=10)

combo_from = ttk.Combobox(frame_cur, values=currencies, state="readonly", width=7, font=("Segoe UI", 10))
combo_from.set("EUR") # Из Евро
combo_from.pack(side=tk.LEFT, padx=5)

arrow_label = tk.Label(frame_cur, text=" ➔ ", font=("Segoe UI", 11, "bold"))
arrow_label.pack(side=tk.LEFT)

combo_to = ttk.Combobox(frame_cur, values=currencies, state="readonly", width=7, font=("Segoe UI", 10))
combo_to.set("RUB") # В Рубли
combo_to.pack(side=tk.LEFT, padx=5)

# Кнопка конвертации
btn = tk.Button(
    root,
    text="Рассчитать и сохранить",
    command=convert_any,
    bg="#28a745",
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=10,
    pady=4
)
btn.pack(pady=10)

# Результат и статус
label_result = tk.Label(root, text="Выберите валюты и нажмите кнопку", font=("Segoe UI", 10, "bold"))
label_result.pack(pady=5)

label_status = tk.Label(root, text="", font=("Segoe UI", 8))
label_status.pack(pady=5)

root.mainloop()

# Валютки
url = "https://open.er-api.com/v6/latest/EUR"
# Запросик
response = requests.get(url)
# Превращаем ответ в словарь
data = response.json()
# тут лежат все валюты мира🥶
rates = data["rates"]
# выбор валюты для сравнения например рубль
target_currency = "RUB"
rate_for_one = rates[target_currency] 
# сотня евро 
amount_100 = 100 * rate_for_one
# делаем строчку для вывода курса
comparison_text = f"1 EUR = {rate_for_one:.2f} {target_currency}  |  100 EUR = {amount_100:.2f} {target_currency}"
print(comparison_text)

# Сохраняем файлик рядом с .py файлом
def save_to_file(text_to_save):
    # Режим "a" дописывает строчку в конец файла не переписывая файл полностью
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(text_to_save + "\n")

save_to_file(text_to_save=comparison_text)




