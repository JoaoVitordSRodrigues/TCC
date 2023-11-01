#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox
import re

class Entrada:
    def dadosTabelaEntrada(self, nomeTela):
        if nomeTela == 'Diretor':
            # Executar a consulta SQL para buscar todas as informações da tabela "entrada"
            BancoTcc.cursor.execute("SELECT nome_aluno, rm_aluno, periodo, data_entrada, horario_entrada, status_horario, nome_seguranca FROM entrada")
            dados_entrada = BancoTcc.cursor.fetchall()
            #se a consulta obter os dados
            if dados_entrada is not None:
                resultado = "Exibindo dados."
                return dados_entrada                     
            #se a consulta nao obter os dados
            else:
                resultado = "Não há dados para a exibição."   
                return resultado
        if nomeTela == 'Seguranca':
            # Executar a consulta SQL para buscar todas as informações da tabela "entrada"
            BancoTcc.cursor.execute("SELECT nome_aluno, rm_aluno, periodo, data_entrada, horario_entrada, status_horario FROM entrada")
            dados_entrada = BancoTcc.cursor.fetchall()
            #se a consulta obter os dados
            if dados_entrada is not None:
                resultado = "Exibindo dados."
                return dados_entrada                     
            #se a consulta nao obter os dados
            else:
                resultado = "Não há dados para a exibição."   
                return resultado