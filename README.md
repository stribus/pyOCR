# PyOCR - Captura de Tela com OCR

Uma ferramenta simples e eficiente para capturar áreas da tela e converter em texto usando OCR (Reconhecimento Óptico de Caracteres).

## Funcionalidades

- Captura de área da tela através de seleção com mouse
- Conversão automática da imagem para texto
- Cópia automática do texto para a área de transferência
- Suporte para língua portuguesa
- Interface gráfica transparente para seleção precisa

## Pré-requisitos

- Python 3.6 ou superior
- Tesseract OCR instalado no sistema
  - [Download do Tesseract-OCR](https://github.com/UB-Mannheim/tesseract/wiki)

## Instalação

1. Clone este repositório ou baixe os arquivos
2. Instale as dependências:

```powershell
pip install -r requirements.txt
```

3. Certifique-se de que o Tesseract-OCR está instalado no sistema

## Como Usar

### Versão Command Line (ocr.py)

```powershell
python ocr.py
```

- Execute o script via prompt de comando
- Selecione a área desejada com o mouse
- O texto será automaticamente copiado para a área de transferência

### Versão Windows (ocr.pyw)

- Execute o arquivo `ocr.pyw` diretamente
- Ou crie um executável usando PyInstaller:

```powershell
pyinstaller --windowed --noconsole --name "pyOCR" --add-data "Tesseract-OCR/*;Tesseract-OCR"  ocr.pyw
```

- Pressione ESC para cancelar a captura

## Configuração

O arquivo `config.ini` permite personalizar:

- Caminho do Tesseract
- Configurações de log
- Idioma do OCR

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

## Licença

Este projeto está sob a licença MIT.  Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
