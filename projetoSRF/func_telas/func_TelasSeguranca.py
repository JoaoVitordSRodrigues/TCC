#IMPORTANDO AS BIBLIOTECAS
import sys
import io
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from main import MainWindow
from telas_py.telas_Seguranca import Ui_MainWindow as Ui_Telas_Seguranca
from PyQt5.QtCore import Qt
# Importa a Biblioteca OPENCV --> Usada para o Reconhecimento em si 
import cv2


#=========================================================================#
#                                                                         #
#     CLASSE COM FUNCIONALIDADES P/ A TELA PRINCIPAL PARA O SEGURANÇA     #
#                                                                         #
#=========================================================================#
class Config_TelasSeguranca(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA SEGURANÇA
    def __init__(self):
        super(Config_TelasSeguranca, self).__init__()
        self.ui = Ui_Telas_Seguranca()
        self.ui.setupUi(self)

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
        self.ui.btnScannerLateral.clicked.connect(self.cameraReconhecimento)

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #                    FUNÇOES DA CLASSE DIRETOR                        -
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------          
    def cameraReconhecimento(self):
        # variável que passa a xml que usaremos no código
        xml_haar_cascade = 'rec_facial/haarcascade_frontalface_alt2.xml'  

        # Carrega o classificador
        faceClassifier = cv2.CascadeClassifier(xml_haar_cascade)

        # Inicia a Camera
        capture = cv2.VideoCapture(0)

        # Define o Tamanho da largura na captura de acordo com o tamanho da webcam 
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 740)
        # Define o Tamanho da altura na captura de acordo com o tamanho da webcam 
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 580)

        # Deixa a Captura ao vivo em um loop até ser pressionado a letra 'Q' e o sistema ser fechado
        while not cv2.waitKey(20) & 0xFF == ord('q'):
            ret, frame_color = capture.read()

                    # Define que a captura vai ser em imagem colorida 
            gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

                    # Detecta o rosto em si da pessoa 
            faces = faceClassifier.detectMultiScale(gray)

                    # Define altura e largura do que será detectado   
            for x, y, w, h in faces:
                cv2.rectangle(frame_color, (x,y), (x + w, y + h), (0,0,255), 2 )


                    # Deixa em si a imagem colorida 
            cv2.imshow('color', frame_color)  


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
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_btnEntradasLAberto_clicked(self):
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


