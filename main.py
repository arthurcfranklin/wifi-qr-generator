# Bibliotecas padrão
import os
import re
import sys
import webbrowser
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

# Bibliotecas de terceiros
import qrcode
from PIL import ImageTk

ESPACO = 10  # Espaçamento geral

# --- Funções --- #
def atualizar_senha():
    if security_var.get() == "nopass":
        senha_entry.config(state="disabled")
        senha_entry.delete(0, tk.END)
    else:
        senha_entry.config(state="normal")

def validar_campos():
    ssid = ssid_entry.get().strip()
    senha = senha_entry.get().strip()
    security = security_var.get()

    if not ssid:
        messagebox.showwarning("Atenção", "Informe o nome da rede (SSID).")
        return False
    if re.search(r"[;,:]", ssid):
        messagebox.showerror("Erro", "O nome da rede (SSID) não pode conter os caracteres ; , ou :")
        return False

    if security != "nopass":
        if not senha:
            messagebox.showwarning("Atenção", "Informe a senha da rede Wi-Fi.")
            return False
        if len(senha) < 8:
            messagebox.showwarning("Atenção", "A senha deve ter pelo menos 8 caracteres.")
            return False
        if re.search(r"[;,:]", senha):
            messagebox.showerror("Erro", "A senha não pode conter os caracteres ; , ou :")
            return False

    return True

def gerar_qr():
    if not validar_campos():
        return

    ssid = ssid_entry.get().strip()
    senha = senha_entry.get().strip()
    security = security_var.get()

    tipo = security_map[security]
    wifi_data = f"WIFI:T:{tipo};S:{ssid};P:{senha};;"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=2,
    )
    qr.add_data(wifi_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_temp = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img_temp)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk
    qr_label.qr_image = img

    salvar_btn.config(state="normal")
    abrir_btn.config(state="normal")

def salvar_qr():
    if not hasattr(qr_label, "qr_image"):
        messagebox.showerror("Erro", "Nenhum QR Code gerado ainda.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("Imagem PNG", "*.png")],
        title="Salvar QR Code como..."
    )

    if file_path:
        try:
            qr_label.qr_image.save(file_path)
            messagebox.showinfo("Sucesso", f"QR Code salvo na pasta escolhida!")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", f"Ocorreu um erro ao salvar o arquivo:\n{e}")

def abrir_qr():
    if not hasattr(qr_label, "qr_image"):
        messagebox.showerror("Erro", "Nenhum QR Code gerado ainda.")
        return

    top = tk.Toplevel(root)
    top.title("QR Code - Pré-visualização")
    top.geometry("400x400")
    top.resizable(False, False)

    img_large = qr_label.qr_image.resize((380, 380))
    img_tk_large = ImageTk.PhotoImage(img_large)

    label = tk.Label(top, image=img_tk_large, bg="#ffffff", relief="solid", bd=1)
    label.image = img_tk_large
    label.pack(pady=10, padx=10)

def abrir_github(event):
    webbrowser.open_new("https://github.com/arthurcfranklin")

# --- Interface --- #
root = tk.Tk()
root.title("Gerador de QR Code de Redes Wi-Fi")
root.geometry("700x600")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

# Caminho completo para os assets
if getattr(sys, 'frozen', False):

    # Caminho base é a pasta temporária onde o PyInstaller extrai o exe
    base_path = sys._MEIPASS
else:
    # Caminho base é a pasta onde está o script
    base_path = os.path.dirname(__file__)

# Ícone da aplicação
icone_path = os.path.join(base_path, "assets", "codeico.ico")
root.iconbitmap(icone_path)

# Título
tk.Label(root, text="Gerador de QR Code de Redes Wi-Fi", font=("Coolvetica", 16, "bold"), bg="#f5f5f5").pack(pady=(20, 15))

# Mapeamento de segurança
security_map = {"WPA":"WPA", "WEP":"WEP", "NS":"nopass"}

main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill="both", expand=True, padx=ESPACO, pady=ESPACO)

# Coluna esquerda (inputs + gerar)
left_frame = tk.Frame(main_frame, bg="#f5f5f5")
left_frame.pack(side="left", fill="y", padx=ESPACO, pady=ESPACO)

tk.Label(left_frame, text="Nome da Rede (SSID):", bg="#f5f5f5").pack(anchor="w", pady=ESPACO)
ssid_entry = ttk.Entry(left_frame, width=30)
ssid_entry.pack(pady=ESPACO)

tk.Label(left_frame, text="Senha:", bg="#f5f5f5").pack(anchor="w", pady=ESPACO)
senha_entry = ttk.Entry(left_frame, width=30, show="*")
senha_entry.pack(pady=ESPACO)

tk.Label(left_frame, text="Tipo de Segurança:", bg="#f5f5f5").pack(anchor="center", pady=ESPACO)
security_var = tk.StringVar(value="WPA")
security_combo = ttk.Combobox(
    left_frame,
    textvariable=security_var,
    values=list(security_map.keys()),
    width=15,
    state="readonly"
)
security_combo.pack(pady=ESPACO)
security_combo.bind("<<ComboboxSelected>>", lambda e: atualizar_senha())

# Botão Gerar QR
ttk.Button(left_frame, text="Gerar QR Code", command=gerar_qr).pack(pady=ESPACO)

# Coluna direita (QR Code + botões)
right_frame = tk.Frame(main_frame, bg="#f5f5f5")
right_frame.pack(side="right", fill="both", expand=True, padx=ESPACO, pady=ESPACO)

qr_label = tk.Label(right_frame, bg="#ffffff", relief="solid", bd=1)
qr_label.pack(pady=ESPACO)

btn_frame = tk.Frame(right_frame, bg="#f5f5f5")
btn_frame.pack(pady=ESPACO)

salvar_btn = ttk.Button(btn_frame, text="Salvar QR Code", command=salvar_qr, state="disabled")
salvar_btn.grid(row=0, column=0, padx=ESPACO, pady=ESPACO)
abrir_btn = ttk.Button(btn_frame, text="Abrir QR Code", command=abrir_qr, state="disabled")
abrir_btn.grid(row=0, column=1, padx=ESPACO, pady=ESPACO)

# Frame inferior para créditos e GitHub
bottom_frame = tk.Frame(root, bg="#f5f5f5")
bottom_frame.pack(side="bottom", pady=ESPACO)

# Frame para o rodapé
bottom_frame = tk.Frame(root, bg="#f5f5f5")
bottom_frame.pack(side="bottom", pady=10)

# Label de crédito
tk.Label(
    bottom_frame,
    text="Criado e Desenvolvido por Arthur Franklin ™",
    bg="#f5f5f5",
    font=("Coolvetica", 10)
).pack()

# Label do GitHub clicável
github_label = tk.Label(
    bottom_frame,
    text="Veja meus projetos no GitHub - @arthurcfranklin",
    fg="blue",
    cursor="hand2",
    bg="#f5f5f5",
    font=("Coolvetica", 10, "underline")
)
github_label.pack()
github_label.bind("<Button-1>", abrir_github)

# Label de privacidade
tk.Label(
    bottom_frame,
    text="⚠️ As informações da rede não são armazenadas. Tudo é excluído ao fechar o programa.",
    bg="#f5f5f5",
    fg="red",
    font=("Coolvetica", 8)
).pack(pady=(12, 0))

root.mainloop()