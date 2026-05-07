import tkinter as tk
from tkinter import messagebox
import time
import threading
from plyer import notification

def disparar_alerta(mensagem, minutos, root):
    # O "motor" continua rodando aqui, mesmo com a janela invisível
    time.sleep(minutos * 60)
    
    try:
        notification.notify(
            title='Lembrete Importante',
            message=mensagem,
            app_name='NudgeLocal',
            timeout=10
        )
    except:
        pass # Garante que o messagebox apareça mesmo se a notificação falhar
        
    # O messagebox precisa que o 'root' exista (mesmo oculto) para funcionar
    messagebox.showinfo("Lembrete", mensagem)
    
    # Agora sim, encerramos o processo completamente após o "OK"
    root.quit()

def configurar_lembrete():
    def iniciar():
        msg = entry_msg.get()
        try:
            tempo = float(entry_tempo.get())
            
            # Mudança 1: daemon=False. Isso diz ao Python: 
            # "Não feche o programa enquanto esta thread estiver ativa".
            threading.Thread(
                target=disparar_alerta, 
                args=(msg, tempo, root), 
                daemon=False 
            ).start()
            
            # Mudança 2: withdraw(). A janela desaparece da vista do usuário,
            # mas o processo continua vivo em RAM aguardando o timer.
            root.withdraw() 
            
        except ValueError:
            messagebox.showerror("Erro", "Insira um número válido.")

    root = tk.Tk()
    root.title("Nudge")
    root.geometry("300x160")
    
    # Centraliza a janela na tela
    root.eval('tk::PlaceWindow . center')
    
    tk.Label(root, text="O que devo lembrar?", font=("Arial", 10)).pack(pady=5)
    entry_msg = tk.Entry(root, width=35)
    entry_msg.pack(padx=10)
    entry_msg.focus_set()

    tk.Label(root, text="Em quantos minutos?", font=("Arial", 10)).pack(pady=5)
    entry_tempo = tk.Entry(root, width=10)
    entry_tempo.pack()

    # UX: Atalho para o Enter disparar o lembrete
    root.bind('<Return>', lambda event: iniciar())
    
    tk.Button(root, text="Me avise (Enter)", command=iniciar, bg="#e1e1e1").pack(pady=15)
    
    root.mainloop()

if __name__ == "__main__":
    configurar_lembrete()