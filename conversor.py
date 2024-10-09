import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image

# Nome do arquivo para armazenar o último número usado
arquivo_sequencia = "sequencia_nome.txt"

# Variável global para a cor de fundo
cor_de_fundo = None

# Função para carregar o último número de sequência do arquivo
def carregar_sequencia():
    if os.path.exists(arquivo_sequencia):
        with open(arquivo_sequencia, "r") as file:
            return int(file.read().strip())
    return 1  # Começa com 1 caso o arquivo não exista

# Função para salvar o último número de sequência no arquivo
def salvar_sequencia(numero):
    with open(arquivo_sequencia, "w") as file:
        file.write(str(numero))

# Função para selecionar o diretório de origem
def selecionar_pasta_origem():
    pasta_origem = filedialog.askdirectory(title="Selecione a pasta de imagens")
    if pasta_origem:
        entrada_origem.delete(0, tk.END)
        entrada_origem.insert(0, pasta_origem)

# Função para selecionar o diretório de destino
def selecionar_pasta_destino():
    pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino")
    if pasta_destino:
        entrada_destino.delete(0, tk.END)
        entrada_destino.insert(0, pasta_destino)

# Função para escolher a cor de fundo
def escolher_cor_fundo():
    global cor_de_fundo
    cor = colorchooser.askcolor(title="Escolha a cor de fundo")[1]
    if cor:
        cor_de_fundo = cor
        botao_cor_fundo.config(bg=cor)  # Altera a cor do botão para indicar a escolha

# Função para converter as imagens
def converter_imagens():
    origem = entrada_origem.get()
    destino = entrada_destino.get()
    formato = formato_var.get()

    if not origem or not destino:
        messagebox.showerror("Erro", "Por favor, selecione as pastas de origem e destino.")
        return

    # Carregar a sequência inicial
    sequencia = carregar_sequencia()

    # Listar as imagens para contar e configurar a barra de progresso
    imagens = [f for f in os.listdir(origem) if f.endswith((".jpg", ".jpeg", ".bmp", ".png"))]
    total_imagens = len(imagens)
    if total_imagens == 0:
        messagebox.showwarning("Atenção", "Nenhuma imagem encontrada na pasta de origem.")
        return

    barra_progresso["maximum"] = total_imagens
    barra_progresso["value"] = 0

    # Loop pelas imagens na pasta de origem
    for i, filename in enumerate(imagens):
        img_path = os.path.join(origem, filename)
        img = Image.open(img_path)
        
        # Aplicar cor de fundo se estiver definida e a imagem tiver transparência
        if cor_de_fundo and img.mode in ("RGBA", "LA", "P"):
            # Converter imagem com fundo transparente para o modo "RGBA"
            img = img.convert("RGBA")
            
            # Criar um novo fundo na cor selecionada
            background = Image.new("RGBA", img.size, cor_de_fundo)
            
            # Compor a imagem com o fundo
            img = Image.alpha_composite(background, img)
        
        # Converter a imagem final para "RGB" antes de salvar, caso necessário
        if formato in ["jpeg", "bmp"]:  # JPEG e BMP não suportam transparência
            img = img.convert("RGB")
        
        # Gerar um novo nome com base na sequência
        new_filename = f"imagem_{sequencia}.{formato}"
        img.save(os.path.join(destino, new_filename))

        # Incrementar a sequência e atualizar a barra de progresso
        sequencia += 1
        barra_progresso["value"] += 1
        janela.update_idletasks()  # Atualiza a barra de progresso em tempo real

    # Salvar a nova sequência no arquivo
    salvar_sequencia(sequencia)
    
    messagebox.showinfo("Sucesso", "Conversão concluída.")
    barra_progresso["value"] = 0

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Conversor de Imagens")
janela.geometry("700x500")

# Diretório de origem
tk.Label(janela, text="Pasta de Imagens:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entrada_origem = tk.Entry(janela, width=40)
entrada_origem.grid(row=0, column=1, padx=10, pady=10)
botao_origem = tk.Button(janela, text="Selecionar", command=selecionar_pasta_origem)
botao_origem.grid(row=0, column=2, padx=10, pady=10)

# Diretório de destino
tk.Label(janela, text="Pasta de Destino:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_destino = tk.Entry(janela, width=40)
entrada_destino.grid(row=1, column=1, padx=10, pady=10)
botao_destino = tk.Button(janela, text="Selecionar", command=selecionar_pasta_destino)
botao_destino.grid(row=1, column=2, padx=10, pady=10)

# Opções de formato
tk.Label(janela, text="Formato de Saída:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
formato_var = tk.StringVar(value="png")
formato_opcoes = ["png", "jpeg", "bmp"]
formato_menu = tk.OptionMenu(janela, formato_var, *formato_opcoes)
formato_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Botão para escolher a cor de fundo
botao_cor_fundo = tk.Button(janela, text="Escolher Cor de Fundo", command=escolher_cor_fundo)
botao_cor_fundo.grid(row=3, column=1, padx=10, pady=10)

# Barra de Progresso
barra_progresso = ttk.Progressbar(janela, orient="horizontal", length=300, mode="determinate")
barra_progresso.grid(row=4, column=1, padx=10, pady=20)

# Botão de conversão
botao_converter = tk.Button(janela, text="Converter Imagens", command=converter_imagens)
botao_converter.grid(row=5, column=1, padx=10, pady=20)

janela.mainloop()
