#IMPORTANDO AS BIBLIOTECAS
import sys
import io
from bd import BancoTcc
import messagebox
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from telaLogin import Ui_MainWindow

from PyQt5.QtCore import Qt



#=========================================================================#
#                                                                         #
#                 CLASSE P/ A TELA DE LOGIN (TELA INICIAL)                #
#                                                                         #
#=========================================================================#
class MainWindow(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA LOGIN
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #=============================================BOTOES==================================================
        #botao(checkbox) de exibir a senha
        self.ui.chkboxExibirSenha.stateChanged.connect(self.exibirSenha)
        #botao de fazer o login
        self.ui.btnLogin.clicked.connect(self.fazerLogin)


    #-----------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------
    #                                    FUNÇOES DA CLASSE LOGIN                                   -
    #-----------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------
    #FUNCAO QUE IRA EXIBIR E ESCONDER A SENHA
    def exibirSenha(self, state):
        #ira exibir a senha ao marcar a checkbox
        if (state == 2):# State 2 representa a caixa de seleção marcada
            self.ui.etySenha.setEchoMode(QtWidgets.QLineEdit.Normal)
        #ira esconder a senha ao desmarcar a checkbox        
        else:
            self.ui.etySenha.setEchoMode(QtWidgets.QLineEdit.Password)

    #FUNCAO QUE IRA FAZER O LOGIN
    def fazerLogin(self):
        #ira fazer a validação dos campos não preechidos
        if(self.ui.etyUsuario.text() == '' or self.ui.etySenha.text() == ''):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")

            if(self.ui.etyUsuario.text() == ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(self.ui.etySenha.text() == ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')

            if(self.ui.etyUsuario.text() != ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(self.ui.etyUsuario.text() != ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
        
        #se os campos estiverem preechidos
        else:
            #se for as credenciais do diretor, ira abrir a tela do diretor
            if(self.ui.etySenha.text() == '1'):
                from func_TelasDiretor import Config_TelasDiretor 
                self.telas_diretor = Config_TelasDiretor()
                self.telas_diretor.show()
                self.close()  # Fecha a tela de login
            else:
                #senao, abra a tela do segurança
                from func_TelasSeguranca import Config_TelasSeguranca   
                self.telas_seguranca = Config_TelasSeguranca()
                self.telas_seguranca.show()
                self.close()  # Fecha #fecha a tela de login

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

