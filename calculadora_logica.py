import tkinter as tk
from tkinter import messagebox
import itertools
import re


VARIABLES = ['p', 'q', 'r']

def traducir_expresion(expr):
    traducciones = {'¬': ' not ', '∧': ' and ', '∨': ' or '}
    for simbolo, operador in traducciones.items():
        expr = expr.replace(simbolo, operador)
    expr = re.sub(r'(.+?)\s*→\s*(.+)', r'(not (\1) or (\2))', expr)
    expr = re.sub(r'(.+?)\s*↔\s*(.+)', r'(\1 == \2)', expr)
    return expr

def generar_combinaciones():
    return list(itertools.product([True, False], repeat=3))

def evaluar(expr, valores):
    p, q, r = valores
    try: return eval(expr)
    except: return "Error"

def extraer_subexpresiones(expr):
    subexpresiones = set()
    expr = expr.replace(" ", "")
    stack = []
    for i, char in enumerate(expr):
        if char == '(':
            stack.append(i)
        elif char == ')' and stack:
            start = stack.pop()
            sub = expr[start + 1:i]
            if sub: subexpresiones.add(sub)
    matches = re.findall(r'¬[pqr]', expr)
    for m in matches: subexpresiones.add(m)
    subexpresiones = list(subexpresiones)
    subexpresiones.sort(key=lambda x: len(x))
    subexpresiones.append(expr)
    return subexpresiones

def generar_tabla_auto(expr_raw):
    combinaciones = generar_combinaciones()
    subexpresiones = extraer_subexpresiones(expr_raw)
    tabla = []
    for valores in combinaciones:
        fila = list(valores)
        subresultados = []
        for subexpr in subexpresiones:
            traducida = traducir_expresion(subexpr)
            subresultados.append(evaluar(traducida, valores))
        fila.extend(subresultados)
        tabla.append(fila)
    return subexpresiones, tabla

def mostrar_tabla():
    expr_raw = entrada_expr.get()
    if not expr_raw:
        messagebox.showerror("Error", "Debes ingresar una expresión lógica.")
        return
    subexpresiones, tabla = generar_tabla_auto(expr_raw)

    for widget in tabla_frame.winfo_children():
        widget.destroy()

    headers = VARIABLES + subexpresiones
    for i, h in enumerate(headers):
        tk.Label(tabla_frame, text=h, font=('Arial', 10, 'bold'),
                 bg="#283747", fg="white", padx=6, pady=4, relief="ridge").grid(row=0, column=i, sticky="nsew")

    for fila_idx, fila in enumerate(tabla, start=1):
        for col_idx, val in enumerate(fila):
            color = "#FDFEFE" if fila_idx % 2 == 0 else "#EBF5FB"
            tk.Label(tabla_frame, text=str(val), bg=color,
                     font=('Consolas', 10), padx=6, pady=4,
                     relief="ridge").grid(row=fila_idx, column=col_idx, sticky="nsew")

    resultados_finales = [fila[-1] for fila in tabla]
    for widget in resultado_frame.winfo_children():
        widget.destroy()
    if all(r is True for r in resultados_finales):
        tipo = "TAUTOLOGÍA (siempre verdadera)"
        color = "green"
    elif all(r is False for r in resultados_finales):
        tipo = "CONTRADICCIÓN (siempre falsa)"
        color = "red"
    else:
        tipo = "Contingencia (a veces verdadera, a veces falsa)"
        color = "blue"
    tk.Label(resultado_frame, text=f"Resultado: {tipo}",
             font=('Arial', 12, 'bold'), fg=color, bg="#F4F6F7").pack(pady=5)


root = tk.Tk()
root.title("Calculadora Lógica (p, q, r)")
root.geometry("850x600")
root.config(bg="#F4F6F7")

titulo = tk.Label(root, text="🔹 Calculadora Lógica 🔹",
                  font=("Arial", 16, "bold"), bg="#2E4053", fg="white", pady=10)
titulo.pack(fill="x")

tk.Label(root, text="Introduce una proposición lógica usando p, q, r:",
         font=("Arial", 12), bg="#F4F6F7").pack(pady=5)

entrada_expr = tk.Entry(root, width=60, font=('Consolas', 13), relief="solid", bd=2)
entrada_expr.pack(pady=5)

def insertar_simbolo(simbolo):
    entrada_expr.insert(tk.INSERT, simbolo)

botones_frame = tk.Frame(root, bg="#F4F6F7")
botones_frame.pack(pady=5)
for s in ['¬', '∧', '∨', '→', '↔', '(', ')']:
    tk.Button(botones_frame, text=s, width=4, font=("Arial", 12, "bold"),
              command=lambda sim=s: insertar_simbolo(sim),
              bg="#3498DB", fg="white", relief="raised", bd=3,
              activebackground="#2980B9", activeforeground="white").pack(side=tk.LEFT, padx=4)

tk.Button(root, text="Generar Tabla de Verdad", command=mostrar_tabla,
          font=("Arial", 12, "bold"), bg="#27AE60", fg="white",
          relief="raised", bd=4, activebackground="#229954").pack(pady=10)

tabla_frame = tk.Frame(root, bg="#F4F6F7")
tabla_frame.pack(pady=10, fill="both", expand=True)

resultado_frame = tk.Frame(root, bg="#F4F6F7")
resultado_frame.pack(pady=5)

ayuda = """Símbolos permitidos:
¬p   → negación
p ∧ q → conjunción
p ∨ q → disyunción
p → q → implicación
p ↔ q → bicondicional
"""
tk.Label(root, text=ayuda, justify="left", font=('Consolas', 10),
         bg="#F4F6F7", fg="black").pack(pady=5)

root.mainloop()
