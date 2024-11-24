# capitura uma area da tela e salva em um arquivo temporario
# depois usa o pytesseract para fazer a leitura do texto
# e copia o texto para a area de transferencia
from datetime import datetime
import tkinter as tk
from PIL import ImageGrab
import pytesseract
import os
import pyperclip
import logging
import configparser



class ScreenCaptureOCR:
    def __init__(self, linguagem='por'):
        """
        Construtor da classe.

        :param linguagem: Linguagem para o reconhecimento de caracteres
        :type linguagem: str
        """

        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3) # Transparência da janela
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='grey')
        self.linguagem = linguagem

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
        """Salva a posição inicial do clique do mouse."""
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        """Redesenha o retângulo de seleção conforme o mouse é movido.

        :param event: Evento do mouse
        :type event: tk.Event
        """
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
        """Copies the given text to the system clipboard.

        :param text: The text string to be copied to the clipboard.
        :type text: str

        :raises pyperclip.PyperclipException: If an error occurs during the copy process.
        """
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException:
            logging.error("Erro ao copiar texto para a área de transferência.")
            
        
    def on_release(self, event):        
        """Fecha a janela e chama o método capture_screen 
        com as coordenadas do retângulo de seleção.

        :param event: Evento do mouse
        :type event: tk.Event
        """
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
        """Captura aerea da tela e salva em um arquivo temporario.
        
        :param x1: Primeira coordenada do retângulo de seleção
        :type x1: int
        :param y1: Segunda coordenada do retângulo de seleção
        :type y1: int
        :param x2: Terceira coordenada do retângulo de seleção
        :type x2: int
        :param y2: Quarta coordenada do retângulo de seleção
        :type y2: int
        """
        try :
            # Captura a área selecionada
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            
            datahora = datetime.now().strftime("%Y%m%d%H%M%S")
            nomefarquivo = f"captura\\captura_{datahora}.png"
            os.makedirs("captura", exist_ok=True)
            # Salva a imagem
            screenshot.save(nomefarquivo)
            
            # Realiza OCR
            text = pytesseract.image_to_string(screenshot, lang=self.linguagem)
                        
            logging.info(f"Texto extraído: {text}")
            logging.info("\nTexto copiado para a área de transferência.")
            self.copy_to_clipboard(text)
        except Exception as e:
            logging.error(f"Erro ao capturar a tela: {e}")
        finally:
            self.root.quit()

def main():
    
    if os.path.exists("config.ini"):
        config = configparser.ConfigParser()
        config.read('config.ini')
        if 'tesseract' in config:
            pytesseract.pytesseract.tesseract_cmd = config['tesseract']['path']
            
        if 'log' in config:
            logging_level = config['log']['level'] if 'level' in config['log'] else 'INFO'
            # logging_path = config['log']['path'] if 'path' in config['log'] else 'ocr.log'
            logging_name = config['log']['name'] if 'name' in config['log'] else 'ocr.log'
            logging_encoding = config['log']['encoding'] if 'encoding' in config['log'] else 'utf-8' 
            logging.basicConfig(level=logging_level, format='%(asctime)s - %(levelname)s - %(message)s', filename=logging_name,encoding=logging_encoding)

        
        # Verifica a linguagem selecionada. Default: português
        linguagem = config['Idioma'] if 'Idioma' in config else 'por'

    else:
        # Configuração do log
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='ocr.log',encoding='utf-8')
        a_Tesseract_path = [
                        r'.\\Tesseract-OCR\\tesseract.exe'
                        ,r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
                        ,r'.\\_internal\\Tesseract-OCR\\tesseract.exe']
        
        for path in a_Tesseract_path:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
    
    # Verifica se o Tesseract está instalado
    if not os.path.exists(pytesseract.pytesseract.tesseract_cmd):
        logging.error("Por favor, instale o Tesseract-OCR primeiro!")
        logging.error("Download: https://github.com/UB-Mannheim/tesseract/wiki")
        return
    
    app = ScreenCaptureOCR()
    app.root.mainloop()

if __name__ == "__main__":
    main()