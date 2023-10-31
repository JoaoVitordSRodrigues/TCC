#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
#importando da pasta 'telas_py' a tela de login em python
from telas_py.telaLogin import Ui_MainWindow
from classes.Funcionario import Funcionario
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

        self.classeFuncionario = Funcionario()
        
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
        if (state == 2):#state 2 representa a caixa de seleção marcada
            self.ui.etySenha.setEchoMode(QtWidgets.QLineEdit.Normal)
        #ira esconder a senha ao desmarcar a checkbox        
        else:
            self.ui.etySenha.setEchoMode(QtWidgets.QLineEdit.Password)

    #FUNCAO QUE IRA FAZER O LOGIN
    def fazerLogin(self):
        usuario = self.ui.etyUsuario.text() 
        senha = self.ui.etySenha.text()  

        #ira fazer a validação dos campos não preechidos
        if(usuario == '' or senha == ''):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")
            #campos nao preechidos, ira setar os campos que nao foram preechidos
            if(usuario == ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            if(senha == ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            #campos preechidos, ira setar os campos que foram preechidos        
            if(usuario != ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
            if(senha != ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
        #se os campos estiverem preechidos
        else: 
            resultado, nome_funcionario  = self.classeFuncionario.funcionario(usuario, senha)
            if resultado == "Credenciais incorretas ou usuário não encontrado":
                QMessageBox.warning(self, 'Aviso', resultado)
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            else:
                QMessageBox.warning(self, 'Aviso', 'Credenciais corretas! Acesso permitido.')
                #se a consulta obter os dados
                if resultado == "Diretor":  
                    from func_telas.func_TelasDiretor import Config_TelasDiretor
                    self.telas_diretor = Config_TelasDiretor(nome_funcionario)#passando como parametro o nome do diretor
                    self.telas_diretor.show()     
                    self.close()  #fecha a tela de login
                elif resultado == "Segurança":
                    from func_telas.func_TelasSeguranca import Config_TelasSeguranca
                    self.telas_seguranca = Config_TelasSeguranca(nome_funcionario)#passando como parametro o nome do segurança
                    self.telas_seguranca.show()
                    self.close()
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

