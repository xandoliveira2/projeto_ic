# 📊 Projeto IC – Guia de Instalação e Uso

Este documento orienta o processo de instalação, configuração e utilização do sistema desenvolvido no Projeto IC.

---

## ⚙️ Passo 0 — Configuração do Banco de Dados

Antes de iniciar o sistema, é necessário que um responsável técnico configure o banco de dados PostgreSQL.

- Arquivo a ser editado: `App/settings.py`
- Variável a ser configurada: `DATABASES`

> ⚠️ Essa etapa exige conhecimentos técnicos em Django e PostgreSQL.

---

## 📥 Passo 1 — Instalar o Python

- Instale o Python na sua máquina, **preferencialmente na versão 3.12 ou superior**.
- Durante a instalação, marque a opção **"Add Python to PATH"**.
- **Reinicie o computador após a instalação** para garantir que a variável de ambiente seja aplicada corretamente.

---

## 📁 Passo 2 — Obter o Projeto

- Baixe e **descompacte os arquivos** deste projeto, ou
- Faça o clone do repositório usando o Git:

  ```bash
  git clone https://github.com/seu-usuario/projeto_ic.git
  ```

- Salve em um local de fácil acesso no seu computador.

---

## 📦 Passo 3 — Instalar Dependências

1. Abra o terminal (CMD, PowerShell, ou terminal do VS Code).
2. Navegue até a **pasta raiz do projeto**, onde está o arquivo `requirements.txt`.
3. Execute o seguinte comando para instalar as dependências:

   ```bash
   python -m pip install -r requirements.txt
   ```

> Use `python3` no lugar de `python` se estiver em sistemas Unix/Linux ou MacOS.

---

## 🚀 Passo 4 — Iniciar o Servidor

1. Navegue até a pasta `App`, onde está localizado o arquivo `manage.py`.
2. Execute o comando:

   ```bash
   python manage.py runserver
   ```

> 🔁 **Porta padrão:** `8000`  
> Se a porta estiver em uso, você pode especificar outra porta assim:

```bash
python manage.py runserver 4560
```

---

## 🌐 Passo 5 — Acessar o Sistema

Abra seu navegador e acesse:

```
http://127.0.0.1:8000
```

> Caso o sistema esteja rodando em um servidor, peça o **IP e a porta correta** ao responsável técnico.

---

## 📈 Passo 6 — Selecionar Variáveis

- Passe o mouse no **lado esquerdo da tela**.
- Isso abrirá um menu com as **variáveis de interesse** disponíveis para geração de gráficos.

---

## 🎯 Passo 7 — (Opcional) Aplicar Filtros Demográficos

- No centro da tela, selecione os filtros desejados, como:
  - Curso
  - Gênero
  - Cidade

---

## 📊 Passo 8 — Gerar o Gráfico

- Após definir as variáveis e filtros, clique no botão **"Gerar Gráfico"**.

---

## 📝 Passo 9 — (Opcional) Adicionar Texto ao Gráfico

- Caso o banco de dados tenha sido configurado corretamente (Passo 0),
- Você poderá **anexar um texto descritivo** ao gráfico gerado com os filtros selecionados.

---

## 📌 Observações Finais

- Este sistema foi desenvolvido utilizando **Django (Python)**.
- Caso enfrente problemas ou tenha dúvidas, abra um 'issue' neste repositório.
