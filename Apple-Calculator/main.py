from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext
import re
import math

#-------------------- Caminho Base e Imagens ---------------
BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH / "assets"

# --- Valores dos Botões ---
button_values = ["clear","√","%","/",
                 "7","8","9","*",
                 "4","5","6","-",
                 "1","2","3","+",
                 "del","0",".","result"]

# --- Rendezirar Imagens ---
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#-------------------- Classe Calculadora ------------------
class AppleCalculator:

    # --- Inicia a calculadora ---
    def __init__(self,width,height,bg):
        self.width = width
        self.height = height
        self.bg = bg
        self.createWindow()
        self.placeCalculation()
        self.placeLastHistorys()
        self.placeResult()
        self.insertAllButton()
        self.history = []
        self.window.bind("<Key>", self.keyPressed)
        
    # --- Cria a Janela ---
    def createWindow(self):
        self.window = tk.Tk()
        self.reallocateWindow()
        self.window.geometry(f"{self.width}x{self.height}+{self.posX}+{self.posY}")
        self.window.configure(bg = self.bg)
        self.window.title("Apple Calculator by William")
        self.icone = tk.PhotoImage(file=ASSETS_PATH / "apple.png")
        self.window.iconphoto(False, self.icone)
        self.createCanvas()
    
    # --- Posição da janela ---
    def reallocateWindow(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        self.posX = screen_width - self.width - 15
        self.posY = screen_height - self.height - 85
            
    # --- Cria o Canvas ---
    def createCanvas(self):
        self.canvas = tk.Canvas(
            self.window,
            bg = self.bg,
            height = self.height,
            width = self.width,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        
        # Obtém o tamanho da janela
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()

        # Garante que os tamanhos sejam atualizados
        self.window.update_idletasks()

        # Recalcula após atualização
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()

        # Calcula posição para centralizar o canvas
        x = (window_width - self.width) // 2
        y = (window_height - self.height) // 2

        self.canvas.place(x=x, y=y)
    
    # --- Cria área dos Cálculos ---
    def placeCalculation(self):
        self.calculation = tk.Text(
            bd=0,
            bg=self.bg,
            fg="#BABABA",
            highlightthickness=0,
            font=("Helvetica", int(self.height * 0.06))
        )
        self.calculation.place(
            x=18.0,
            y=104.0,
            width=self.width * 0.91818,
            height=self.height * 0.1537
        )
        self.calculation.tag_configure("right", justify="right")
        self.calculation.insert("1.0", "")
        self.calculation.tag_add("right", "1.0", "end")
    
    # --- Cria área do Resultado ---
    def placeResult(self):
        self.result = tk.Text(
            bd=0,
            bg=self.bg,
            fg="#FFFFFF",
            highlightthickness=0,
            font=("Helvetica", int(self.height * 0.09))
        )
        self.result.place(
            x=18,
            y=70.0 + self.height * 0.1537,
            width=self.width * 0.91818,
            height=self.height * 0.15914
        )
        self.result.tag_configure("right", justify="right")
        self.result.insert("1.0", "")
        self.result.tag_add("right", "1.0", "end")
    
    # --- Histórico de Calculos ---
    def placeLastHistorys(self):
        self.historyImage = tk.PhotoImage(
        file=relative_to_assets("button_1.png"))

        # Redimensiona usando Pillow
        img_path = relative_to_assets("button_1.png")
        img = Image.open(img_path)
        resized_img = img.resize((int(self.width * 0.08522), int(self.height * 0.035303)))
        self.historyImage = ImageTk.PhotoImage(resized_img)

        historyButton = tk.Button(
            image=self.historyImage,
            borderwidth=0,
            highlightthickness=0,
            bg="black",            # <- fundo do botão
            activebackground="black",  # <- fundo quando pressionado
            command=lambda: self.showHistory(),
            relief="flat"
        )
        historyButton.place(
            x=37.875,
            y=30.625118255615234,
            width=self.width * 0.08522,
            height=self.height * 0.035303
        )
    
    # --- Inserir novo caracter ao cálculo ---
    def addToCalculation(self,value):
        current_text = self.calculation.get("1.0", tk.END).strip()
        result = self.result.get("1.0", tk.END).strip()

        if result and value not in ("del", "clear", "result"):
            current_text = result + value
            self.calculation.delete("1.0", tk.END)
            self.calculation.insert(tk.END, current_text)
            self.result.delete("1.0", tk.END)  # limpa o resultado antigo
        elif value == "del":
            current_text = current_text[:-1]
            self.calculation.delete("1.0", tk.END)
            self.calculation.insert(tk.END, current_text)
        elif value == "clear":
            self.calculation.delete("1.0", tk.END)
            self.result.delete("1.0", tk.END)
        elif value == "result":
            try:
                expression = current_text
                expression = re.sub(r'√(\d+(\.\d+)?)', r'math.sqrt(\1)', expression)
                expression = re.sub(r'(\d+)%', r'(\1/100)', expression)
                result = eval(expression)
                self.updateResult(result,current_text)
            except Exception as e:
                self.updateResult("Erro")
        else:
            self.calculation.insert(tk.END, value)
        
        self.calculation.tag_add("right", "1.0", "end")

    # --- Atualizar o resultado ---
    def updateResult(self,result,text):
        self.history.append(f"{text} = {str(result)}")
        self.calculation.delete("1.0", tk.END)
        self.result.delete("1.0", tk.END)
        self.result.insert(tk.END, str(result))
        self.result.tag_add("right", "1.0", "end")

    # --- Inserir Botões ---
    def insertAllButton(self):
        y = self.height * 0.399983
        x = self.width * 0.022727

        for i in range(20):
            self.insertButton(i+2,button_values[i],x,y)

            # Verifica se está na última coluna
            x += self.width * 0.22045 + 5
            if (i+1) % 4 == 0:
                y += self.height * 0.1046 + 9
                x = 10

    # --- Inserir botão ---
    def insertButton(self,n,value,posX,posY):
        
        # Redimensiona usando Pillow
        img_path = relative_to_assets(f"button_{n}.png")
        img = Image.open(img_path)
        resized_img = img.resize((int(self.width * 0.22045), int(self.height * 0.1046)))
        buttonImage = ImageTk.PhotoImage(resized_img)
        setattr(self, f"buttonImage_{n}", buttonImage)

        button = tk.Button(
            image=buttonImage,
            borderwidth=0,
            highlightthickness=0,
            bg="black",            # <- fundo do botão
            activebackground="black",  # <- fundo quando pressionado
            command=lambda: self.addToCalculation(value),
            relief="flat"
        )
        button.place(
            x=posX,
            y=posY,
            width=self.width * 0.22045,
            height=self.height * 0.1046
        )

    # --- Mostrar histórico --
    def showHistory(self):
        # Cria uma nova janela (Toplevel) para o histórico
        history_window = tk.Toplevel()
        history_window.title("Histórico de Cálculos")
        history_window.geometry("400x300") # Define o tamanho da janela

        # Cria um widget ScrolledText (uma caixa de texto com barra de rolagem)
        # É ideal para exibir várias linhas de texto
        history_text_area = scrolledtext.ScrolledText(
            history_window,
            wrap=tk.WORD, # Quebra de linha por palavra
            width=40,
            height=15,
            font=("Arial", 10)
        )
        history_text_area.pack(expand=True, fill="both", padx=10, pady=10)

        # Insere cada item do histórico na área de texto
        for calculo in self.history:
            history_text_area.insert(tk.END, calculo + "\n")
        
        history_text_area.config(state=tk.DISABLED)
    
    # --- Tecla pressionada ---
    def keyPressed(self, event):
        char = event.char

        if char in "0123456789+-*/.%√":
            self.addToCalculation(char)
        elif event.keysym == "Return":
            self.addToCalculation("result")
        elif event.keysym == "BackSpace":
            self.addToCalculation("del")
        elif event.keysym == "Escape":
            self.addToCalculation("clear")

        # Reaplica o alinhamento à direita
        self.calculation.tag_add("right", "1.0", "end")
        

if __name__ == '__main__':
    myCalculator = AppleCalculator(300, 550, "#000000")
    myCalculator.window.mainloop()