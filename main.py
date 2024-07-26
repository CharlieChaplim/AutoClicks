import threading
import time
from pynput.keyboard import Controller as KeyboardController, Listener, Key
from pynput.mouse import Controller as MouseController, Button
import tkinter as tk
from tkinter import messagebox

# Inicializa o controlador de teclado e mouse
keyboard = KeyboardController()
mouse = MouseController()

# Variáveis de controle das macros
running = False
mouse_running = False

# Configurações padrão
config = {
    'key1': None,
    'key2': None,
    'key3': None,
    'hold1': False,
    'hold2': False,
    'hold3': False,
    'interval': 0.025,
    'stop_key': None,
    'mouse_button': None,
    'mouse_hold': False,
    'mouse_interval': 0.025,
    'mouse_stop_key': None
}

def press_key_repeatedly():
    global running
    while running:
        if config['key1']:
            if config['hold1']:
                keyboard.press(config['key1'])
            else:
                keyboard.press(config['key1'])
                keyboard.release(config['key1'])

        if config['key2']:
            if config['hold2']:
                keyboard.press(config['key2'])
            else:
                keyboard.press(config['key2'])
                keyboard.release(config['key2'])

        if config['key3']:
            if config['hold3']:
                keyboard.press(config['key3'])
            else:
                keyboard.press(config['key3'])
                keyboard.release(config['key3'])

        time.sleep(config['interval'])

def click_mouse_repeatedly():
    global mouse_running
    while mouse_running:
        if config['mouse_button']:
            if config['mouse_hold']:
                mouse.press(config['mouse_button'])
            else:
                mouse.click(config['mouse_button'])
            if config['mouse_hold']:
                mouse.release(config['mouse_button'])
        time.sleep(config['mouse_interval'])

def release_held_keys():
    if config['key1'] and config['hold1']:
        keyboard.release(config['key1'])
    if config['key2'] and config['hold2']:
        keyboard.release(config['key2'])
    if config['key3'] and config['hold3']:
        keyboard.release(config['key3'])

def toggle_macro():
    def on_press(key):
        global running
        try:
            if key.char == config['stop_key']:
                running = not running
                if running:
                    print("Macro de teclado iniciada.")
                    threading.Thread(target=press_key_repeatedly).start()
                else:
                    print("Macro de teclado parada.")
                    release_held_keys()
        except AttributeError:
            if key == config['stop_key']:
                running = not running
                if running:
                    print("Macro de teclado iniciada.")
                    threading.Thread(target=press_key_repeatedly).start()
                else:
                    print("Macro de teclado parada.")
                    release_held_keys()

    listener = Listener(on_press=on_press)
    listener.start()

def toggle_mouse_macro():
    def on_press(key):
        global mouse_running
        try:
            if key.char == config['mouse_stop_key']:
                mouse_running = not mouse_running
                if mouse_running:
                    print("Macro de mouse iniciada.")
                    threading.Thread(target=click_mouse_repeatedly).start()
                else:
                    print("Macro de mouse parada.")
                    mouse.release(config['mouse_button'])
        except AttributeError:
            if key == config['mouse_stop_key']:
                mouse_running = not mouse_running
                if mouse_running:
                    print("Macro de mouse iniciada.")
                    threading.Thread(target=click_mouse_repeatedly).start()
                else:
                    print("Macro de mouse parada.")
                    mouse.release(config['mouse_button'])

    listener = Listener(on_press=on_press)
    listener.start()

def update_keyboard_config():
    global config
    key1 = entry_key1.get().lower()
    key2 = entry_key2.get().lower() or None
    key3 = entry_key3.get().lower() or None
    stop_key_str = entry_stop_key.get().lower()

    if not key1 or not stop_key_str:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios.")
        return

    config['key1'] = key1
    config['key2'] = key2
    config['key3'] = key3
    config['hold1'] = hold_var1.get()
    config['hold2'] = hold_var2.get()
    config['hold3'] = hold_var3.get()
    config['stop_key'] = stop_key_str if len(stop_key_str) == 1 else getattr(Key, stop_key_str, stop_key_str)

    print("Configuração do teclado atualizada:", config)

def update_mouse_config():
    global config
    mouse_button = mouse_button_var.get()
    mouse_stop_key_str = entry_mouse_stop_key.get().lower()

    if mouse_button == 'none' or not mouse_stop_key_str:
        messagebox.showwarning("Atenção", "Por favor, preencha todos os campos obrigatórios.")
        return

    config['mouse_button'] = Button.left if mouse_button == 'left' else Button.right
    config['mouse_hold'] = mouse_hold_var.get()
    config['mouse_stop_key'] = mouse_stop_key_str if len(mouse_stop_key_str) == 1 else getattr(Key, mouse_stop_key_str, mouse_stop_key_str)

    print("Configuração do mouse atualizada:", config)

def open_keyboard_config_window():
    keyboard_window = tk.Toplevel()
    keyboard_window.title("Configuração do Teclado")

    # Tecla 1
    tk.Label(keyboard_window, text="Tecla 1 (obrigatória):").grid(row=0, column=0)
    global entry_key1
    entry_key1 = tk.Entry(keyboard_window)
    entry_key1.grid(row=0, column=1)

    global hold_var1
    hold_var1 = tk.BooleanVar()
    hold_checkbox1 = tk.Checkbutton(keyboard_window, text="Segurar", variable=hold_var1)
    hold_checkbox1.grid(row=0, column=2)

    # Tecla 2
    tk.Label(keyboard_window, text="Tecla 2 (opcional):").grid(row=1, column=0)
    global entry_key2
    entry_key2 = tk.Entry(keyboard_window)
    entry_key2.grid(row=1, column=1)

    global hold_var2
    hold_var2 = tk.BooleanVar()
    hold_checkbox2 = tk.Checkbutton(keyboard_window, text="Segurar", variable=hold_var2)
    hold_checkbox2.grid(row=1, column=2)

    # Tecla 3
    tk.Label(keyboard_window, text="Tecla 3 (opcional):").grid(row=2, column=0)
    global entry_key3
    entry_key3 = tk.Entry(keyboard_window)
    entry_key3.grid(row=2, column=1)

    global hold_var3
    hold_checkbox3 = tk.Checkbutton(keyboard_window, text="Segurar", variable=hold_var3)
    hold_checkbox3.grid(row=2, column=2)

    # Tecla de parada/início do teclado
    tk.Label(keyboard_window, text="Tecla de parada/início (teclado):").grid(row=3, column=0)
    global entry_stop_key
    entry_stop_key = tk.Entry(keyboard_window)
    entry_stop_key.grid(row=3, column=1)

    # Botão de atualização
    tk.Button(keyboard_window, text="Atualizar Configuração", command=update_keyboard_config).grid(row=4, columnspan=3)

def open_mouse_config_window():
    mouse_window = tk.Toplevel()
    mouse_window.title("Configuração do Mouse")

    # Seção do Mouse
    tk.Label(mouse_window, text="Botão do Mouse:").grid(row=0, column=0)
    global mouse_button_var
    mouse_button_var = tk.StringVar(value='none')
    tk.Radiobutton(mouse_window, text="Esquerdo", variable=mouse_button_var, value='left').grid(row=0, column=1)
    tk.Radiobutton(mouse_window, text="Direito", variable=mouse_button_var, value='right').grid(row=0, column=2)

    global mouse_hold_var
    mouse_hold_var = tk.BooleanVar()
    tk.Checkbutton(mouse_window, text="Segurar", variable=mouse_hold_var).grid(row=1, column=1)

    # Tecla de parada/início do mouse
    tk.Label(mouse_window, text="Tecla de parada/início (mouse):").grid(row=2, column=0)
    global entry_mouse_stop_key
    entry_mouse_stop_key = tk.Entry(mouse_window)
    entry_mouse_stop_key.grid(row=2, column=1)

    # Botão de atualização
    tk.Button(mouse_window, text="Atualizar Configuração", command=update_mouse_config).grid(row=3, columnspan=3)

def create_main_gui():
    window = tk.Tk()
    window.title("Macro de Teclado e Mouse")

    tk.Button(window, text="Configurar Teclado", command=open_keyboard_config_window).pack(pady=10)
    tk.Button(window, text="Configurar Mouse", command=open_mouse_config_window).pack(pady=10)
    tk.Button(window, text="Iniciar Macro", command=lambda: [toggle_macro(), toggle_mouse_macro()]).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_main_gui()
