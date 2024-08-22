# Controle de Ponto Eletrônico

Este projeto é um sistema de controle de ponto eletrônico desenvolvido em Python utilizando a biblioteca `tkinter` para a interface gráfica e `sqlite3` para o banco de dados. Ele permite que professores registrem entradas e saídas, além de realizar backups dos dados de registro e gerenciar o cadastro de professores.

## Funcionalidades

- **Registrar Ponto:** Professores podem registrar entradas e saídas ao longo do dia.
- **Cadastro de Professores:** Permite o cadastro de novos professores no sistema.
- **Cancelar Matrícula:** Opção para cancelar a matrícula de professores.
- **Backup de Dados:** Gera backups dos dados dos professores e seus registros de ponto.

## Estrutura do Projeto

- **`interface.py`**: Arquivo principal que define a interface gráfica da aplicação e a lógica de interação do usuário.
- **`ponto.py`**: Módulo que lida com o registro de entrada e saída dos professores.
- **`cadastro.py`**: Módulo responsável pelo cadastro de professores e manipulação dos dados relacionados.
- **`backup.py`**: Módulo que permite criar backups dos dados dos professores.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/fleabagreact/ponto-ifrn.git
   ```

2. Instale as dependências (caso haja):
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   python interface.py
   ```

## Como Usar

- **Confirmar Presença**: Digite a matrícula do professor e clique em "Bater Entrada" ou "Bater Saída" para registrar a presença.
- **Cadastrar Professor**: No menu "Cadastro de Professores", insira a matrícula e o nome do professor e clique em "Cadastrar Professor".
- **Cancelar Matrícula**: No menu "Cancelar Matrícula", insira a matrícula do professor que deseja cancelar e clique em "Cancelar Matrícula".
- **Backup**: Para criar um backup dos dados, clique no botão "Abrir Backup" e siga as instruções.

## Tecnologias Utilizadas

- Python 3.x
- Tkinter
- SQLite3

## Aviso

Não há uma configuração tão boa do SQL porque na época, eu ainda não tinha aula de banco de dados.
