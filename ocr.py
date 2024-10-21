# capitura uma area da tela e salva em um arquivo temporario
# depois usa o pytesseract para fazer a leitura do texto
# e copia o texto para a area de transferencia
from datetime import datetime
import tkinter as tk
from PIL import ImageGrab
import pytesseract
import os
import pyperclip




class ScreenCaptureOCR:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3) # Transparência da janela
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='grey')

        # Variáveis para armazenar as coordenadas
        self.start_x = None
        self.start_y = None
        self.current_x = None
        self.current_y = None

        # Criar canvas
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill='both', expand=True)

        # Binding dos eventos do mouse
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Tecla de escape para sair
        self.root.bind("<Escape>", lambda e: self.root.quit())

    def on_press(self, event):
        # Salvar posição inicial
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        # Atualizar posição atual
        self.current_x = event.x
        self.current_y = event.y
        
        # Redesenhar retângulo
        self.canvas.delete("selection")
        self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.current_x, self.current_y,
            outline='red', tags="selection"
        )
        
    def copy_to_clipboard(self, text):
        # Copiar texto para a área de transferência
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException:
            print("Erro ao copiar texto para a área de transferência.")
            
        
    def on_release(self, event):
        # Capturar a área selecionada
        if self.start_x and self.start_y and self.current_x and self.current_y:
            x1 = min(self.start_x, self.current_x)
            y1 = min(self.start_y, self.current_y)
            x2 = max(self.start_x, self.current_x)
            y2 = max(self.start_y, self.current_y)

            # Fecha a janela
            self.root.withdraw()
            
            # Pequena pausa para garantir que a janela sumiu
            self.root.after(100, lambda: self.capture_screen(x1, y1, x2, y2))

    def capture_screen(self, x1, y1, x2, y2):
        try :
            # Captura a área selecionada
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            
            datahora = datetime.now().strftime("%Y%m%d%H%M%S")
            nomefarquivo = f"captura\\captura_{datahora}.png"
            # Salva a imagem
            screenshot.save(nomefarquivo)
            
            # Realiza OCR
            text = pytesseract.image_to_string(screenshot, lang='por')
            
            # Salva o texto em um arquivo
            with open(f"transcricao\\texto_extraido{datahora}.txt", "w", encoding='utf-8') as f:
                f.write(text)
            
            print("Imagem salva como 'captura.png'")
            print("Texto extraído salvo em 'texto_extraido{datahora}.txt'")
            print("\nTexto extraído:")
            print(text)
            
            print("\nTexto copiado para a área de transferência.")
            self.copy_to_clipboard(text)
        finally:
            self.root.quit()

def main():
    # Verifica se o Tesseract está instalado
    if not os.path.exists(r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'):
        print("Por favor, instale o Tesseract-OCR primeiro!")
        print("Download: https://github.com/UB-Mannheim/tesseract/wiki")
        return

    # Define o caminho do Tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    
    print("Selecione a área da tela para capturar.")
    print("Pressione ESC para sair.")
    
    app = ScreenCaptureOCR()
    app.root.mainloop()

if __name__ == "__main__":
    main()