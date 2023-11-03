#IMPORTANDO AS BIBLIOTECAS
import sys
import io
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from main import MainWindow
from telas_py.telas_Seguranca import Ui_MainWindow as Ui_Telas_Seguranca
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
#importando da pasta 'classes' a classe entrada em python
from classes.Entrada import Entrada
# Importa a Biblioteca OPENCV --> Usada para o Reconhecimento em si 
import cv2
import pyttsx3
import sqlite3
import numpy as np
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys, os
from datetime import datetime

#=========================================================================#
#                                                                         #
#     CLASSE COM FUNCIONALIDADES P/ A TELA PRINCIPAL PARA O SEGURANÇA     #
#                                                                         #
#=========================================================================#
class Config_TelasSeguranca(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA SEGURANÇA
    def __init__(self, nome_funcionario):
        super(Config_TelasSeguranca, self).__init__()
        self.ui = Ui_Telas_Seguranca()
        self.ui.setupUi(self)

        self.classeEntrada = Entrada()
        
        #variavel que recebe o nome do funcionario
        self.nome_funcionario = nome_funcionario
        #setando o nome do funcionario na label da pagina de inicio
        self.ui.label_2.setText(f'Olá, {self.nome_funcionario}')

        #ESCONDER ICONES DO MENU E CONFIGURAR INDICE DA PAG INICIAL
        self.ui.menu_icons.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnIconMenu.setChecked(True)

        #FUNÇAO DOS BOTOES VOLTAR
        self.ui.btnVoltarLAberto.clicked.connect(self.on_btnVoltarLateral_clicked)
        
        #FUNÇOES DOS BOTOES DESCONECTAR
        self.ui.btnDesconectar_PgHome.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLateral.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLAberto.clicked.connect(self.abrirTelaLogin)

        #=============CONFIG PAG SCANNER=============
        self.ui.btnScanner.clicked.connect(self.exibirDadosValidacao)
        self.ui.btnScannerLateral.clicked.connect(self.exibirDadosValidacao)
        

        self.ui.etyPesquisar_PgEntradas.textChanged.connect(self.filtrarTabela)




    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #                    FUNÇOES DA CLASSE DIRETOR                        -
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------          
    def consultar_aluno(self):
        self.executarAudioValidacao()
        


    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.menu_icons.findChildren(QPushButton) \
                    + self.ui.menu_todo.findChildren(QPushButton)
        
        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)
            
    #================FUNCOES P/ TROCAR DE PAG================
    #================BOTOES DO MENU DE CIMA (HEADER)================
    #botao que ira redirecionar p/ pag scanner
    def on_btnScanner_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #botao que ira redirecionar p/ pag entradas
    def on_btnEntradas_clicked(self):
        self.inserirDadosTabelaEntrada()
        self.ui.stackedWidget.setCurrentIndex(1)

    #================BOTOES DO MENU LATERAL================
    #botoes que ira redirecionar p/ pag home
    def on_btnHomeLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_btnHomeLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    #botoes que ira redirecionar p/ pag scanner
    def on_btnScannerLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def on_btnScannerLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #botoes que ira redirecionar p/ pag entradas
    def on_btnEntradasLateral_clicked(self):
        self.inserirDadosTabelaEntrada()
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_btnEntradasLAberto_clicked(self):
        self.inserirDadosTabelaEntrada()
        self.ui.stackedWidget.setCurrentIndex(1)

    #funcao para verificar a pagina atual e funcionar o botão voltar
    def on_btnVoltarLateral_clicked(self):
        #0 = pag home
        #1 = pag scanner
        #2 = pag entradas

        telaAtual = self.ui.stackedWidget.currentIndex()

        #se tiver na tela home, irá voltar para tela home
        if telaAtual == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela scanner, irá voltar para tela home
        elif telaAtual == 1:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela entradas, irá voltar para tela home
        elif telaAtual == 2:
            self.ui.stackedWidget.setCurrentIndex(0)

    #===============funcao de abrir tela de login, que ira ser exibida ao desconectar===============
    def abrirTelaLogin(self):
        #criando uma instancia da tela de login
        self.main = MainWindow()  
        #exibindo a tela
        self.main.show()
        #fecha a tela anterior
        self.close()  

    def inserirDadosTabelaEntrada(self):#botao que redireciona para a pag de cadastro
        nomeTela = 'Seguranca'
        # Conectar ao banco de dados (substitua 'seu_banco_de_dados.db' pelo nome do seu banco de dados)
        dados_entrada = self.classeEntrada.dadosTabelaEntrada(nomeTela)

        if dados_entrada == "Não há dados para a exibição.":
            QMessageBox.warning(self, "Aviso", "Não foi possível exibir dados da tabela.")
        else:
            # Preencher a tabela com os dados do banco de dados
            self.ui.tbl_historicoEntradas.setRowCount(len(dados_entrada))
            for row, data in enumerate(dados_entrada):
                for col, value in enumerate(data):
                    item = QTableWidgetItem(str(value))
                    self.ui.tbl_historicoEntradas.setItem(row, col, item)
    
    def filtrarTabela(self):
        search_text = self.ui.etyPesquisar_PgEntradas.text().lower()
        for row in range(self.ui.tbl_historicoEntradas.rowCount()):
            row_hidden = True
            for col in range(self.ui.tbl_historicoEntradas.columnCount()):
                item = self.ui.tbl_historicoEntradas.item(row, col)
                if item.text().lower().startswith(search_text):
                    row_hidden = False
                    break
            self.ui.tbl_historicoEntradas.setRowHidden(row, row_hidden)

    #dados que irão ser exibidos apos validar o rosto do aluno
    def exibirDadosValidacao(self):
        dados_dia = datetime.now()  #setando na variavel os dados do dia(dia, mes, ano, hora, etc.)
        data_hoje_formatada = dados_dia.strftime("%d/%m/%Y")  #setando na variavel a data formatada(00/00/0000)
        horario_hoje_formatado = dados_dia.strftime("%H:%M")  #setando na variavel o horario formatado (00:00)

        self.ui.lbl_dataDoDia.setText(data_hoje_formatada)
        self.ui.lbl_horarioDoDia.setText(horario_hoje_formatado)
   

