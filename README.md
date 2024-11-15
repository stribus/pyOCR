# pyOCR

captura uma area da tela e converte em texto
precisa do tesseract-ocr instalado

## ocr.py

para usar no pronpt de comando

## ocr.pyw

para usar como aplicativo windows.
gerando um arquivo executavel com o pyinstaller

```cmd
pyinstaller --windowed --noconsole --name "pyOCR" --add-data "Tesseract-OCR/*;Tesseract-OCR"  ocr.pyw
```
