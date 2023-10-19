#IMPORTANDO AS BIBLIOTECAS
import sys
import io
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from telas_py.telaLogin import Ui_MainWindow

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
        usuario = self.ui.etyUsuario.text() 
        senha = self.ui.etySenha.text()  

        #ira fazer a validação dos campos não preechidos
        if(usuario == '' or senha == ''):
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")

            if(usuario == ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(senha == ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid red; color:#ffffff')

            if(usuario != ''):
                self.ui.etyUsuario.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(senha != ''):
                self.ui.etySenha.setStyleSheet('background-color: #454648; border-radius:5px; border: 2px solid green; color:#ffffff')
        
        #se os campos estiverem preechidos
        else:
            # Consulta ao banco de dados para verificar o login
            BancoTcc.cursor.execute("""
            SELECT funcao FROM funcionario WHERE usuario = ? AND senha = ?
            """, (usuario, senha))
            # Recupere todos os registros da consulta
            resultados = BancoTcc.cursor.fetchall()     

            if resultados:
                # Pelo menos um registro foi encontrado
                funcao_funcionario = resultados[0][0]  # Obtém o valor da coluna 'funcao' do primeiro registro
                
                if (funcao_funcionario == 'Diretor'):
                    from func_telas.func_TelasDiretor import Config_TelasDiretor 
                    self.telas_diretor = Config_TelasDiretor()
                    self.telas_diretor.show()
                    self.close()  # Fecha a tela de login
                elif (funcao_funcionario == 'Seguranca'):
                    #senao, abra a tela do segurança
                    from func_telas.func_TelasSeguranca import Config_TelasSeguranca   
                    self.telas_seguranca = Config_TelasSeguranca()
                    self.telas_seguranca.show()
                    self.close()  # Fecha #fecha a tela de login
            else:
                QMessageBox.warning(self, "Login Falhou", "Credenciais incorretas ou usuário não encontrado")


            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

