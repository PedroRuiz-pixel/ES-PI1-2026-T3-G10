# Grupo 10 - ES-PI1-2026-T3
GRUPO 10 - SALA 3 

##Descrição do projeto:
Projeto desenvolvido para a disciplina de Projeto Integrador I - Engenharia de Software da PUC-Campinas.

O sistema simula um processo de votação digital em ambiente terminal, com foco em organização, segurança dos dados e integração entre Python e MySQL



##Integrantes:

- Eduardo de Campos Ferreira Filho

- Pedro Henrique Bassetto Ruiz

- Matheus Augusto Alves

- Kauan Paixão Benedito

- Bruno Rosa dos Anjos

##Objetivos:
-Desenvolver o backend de um sistema de votação digital fictício, utilizando python, mysql e organização do projeto com github.


##Tecnologias utilizadas:
-Python3
-MySQL
-Github
-Github Project


##Funcionalidades já implementadas:
- Reposiório github criado
- Read.me inical
- Ligação de Python com o Banco de Dados
- Banco de Dados Criado
- Validação de Cpf
- Validação de Título de Eleitor
- Fluxo de Votos Implementado
- Autêntificação de Mesário
- Encerramento de Votação
- Zerézima
- Menu Principal
- Menu Gerenciamento
- Menu de Eleitor
- Menu Candidatos
- Menu Votação
- Menu Abertura de Votação
- Menu Auditoria
- Menu Resultados
- Listagem de Eleitores
- Criptografia e Descriptografia
- Cifra de Hill
- Busca de Eleitor
- Cadastro de Eleitor
- Logs Implementados
- Estatísticas de Comparecimento
- Boletim de Urna
- Validação de Integridade

##Como executar o sistema:
py menu_principal.py

##Estrutura do projeto:
- `menu_principal.py`: arquivo principal para iniciar o sistema.
- `menus/`: menus de navegação do sistema.
- `database/`: conexão com o banco de dados.
- `auditoria/`: logs, auditoria e protocolos.
- `votacao/`: funções de votação que não são menus, como a zerésima.
- `Criptografia/`: arquivos relacionados à criptografia.

###Pré requisitos:
-Pyhton3 instalado
-MySQL instalado e em execução
-Biblioteca 'mysql-connector-python' instalada

###Instalação da biblioteca:
''' bash 
pip install mysql-connector-python
