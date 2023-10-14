#IMPORTANDO AS BIBLIOTECAS
import sys
import cv2
import io
import BancoTcc
import messagebox
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
from telaLogin import Ui_MainWindow
from telas_Diretor import Ui_MainWindow as Ui_Telas_Diretor
from telas_Seguranca import Ui_MainWindow as Ui_Telas_Seguranca
from PyQt5.QtCore import Qt
# Importa a Biblioteca OPENCV --> Usada para o Reconhecimento em si 
import cv2



#=========================================================================#
#                                                                         #
#                 CLASSE P/ A TELA PRINCIPAL PARA O DIRETOR               #
#                                                                         #
#=========================================================================#
class TelasDiretor(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA DIRETOR
    def __init__(self):
        super(TelasDiretor, self).__init__()
        self.ui = Ui_Telas_Diretor()
        self.ui.setupUi(self)

        #ESCONDER ICONES DO MENU E CONFIGURAR INDICE DA PAG INICIAL
        self.ui.menu_icons.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btnIconMenu.setChecked(True)
        
        #=======================BOTOES DE NAVEGACAO LATERAIS===========================
        #FUNÇAO DOS BOTOES VOLTAR
        self.ui.btnVoltarLAberto.clicked.connect(self.on_btnVoltarLateral_clicked)

        #FUNÇOES DOS BOTOES DESCONECTAR
        self.ui.btnDesconectar_PgHome.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLateral.clicked.connect(self.abrirTelaLogin)
        self.ui.btnDesconectarLAberto.clicked.connect(self.abrirTelaLogin)

        #===========BOTOES DE NAVEGACAO DENTRO DAS PAG(FUNCIONALIDADES)================
        
        #==================================================================
        #======================CONFIG PAG PESQUISAR========================
        #==================================================================
        #botao que ira redirecionar p/ pag turma
        self.ui.btnBuscarTurma_PgPesquisar.clicked.connect(self.btnBuscarTurma)
        #botao que ira redirecionar p/ pag alunoRm
        self.ui.btnBuscarRM_PgPesquisar_2.clicked.connect(self.btnBuscarRm)
        #==================================================================


        #==================================================================
        #======================CONFIG PAG DADOS ALUNO======================
        #==================================================================
        #botao que ira redirecionar p/ pag atualizar aluno
        self.ui.btnAtualizarAluno_PgAtualizar_2.clicked.connect(self.btnAtualizarAluno_PgDadosAluno)
        #==================================================================

        
        #==================================================================
        #===================CONFIG PAG CADASTRAR ALUNO=====================
        #==================================================================
        #botao que ira carregar a imagem do aluno      
        self.ui.btnCarregarFT_PgCadastro.clicked.connect(self.carregar_imagem)
        #botao que ira cadastrar aluno
        self.ui.btnCadastrarAluno_PgCadastro.clicked.connect(self.cadastrarAluno)
        #==================================================================



        #==================================================================
        #===================CONFIG PARA DELETAR ALUNO======================
        #==================================================================
        self.ui.btnDeletarAluno_PgAtualizar_2.clicked.connect(self.deletarAluno)


        #setando os valores da combobox 'periodo' 
        self.ui.cboxPeriodo_PgCadastro.addItem("Selecione o período do aluno")
        self.ui.cboxPeriodo_PgCadastro.addItem("Manhã")
        self.ui.cboxPeriodo_PgCadastro.addItem("Tarde")
        self.ui.cboxPeriodo_PgCadastro.addItem("Noite")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxPeriodo_PgCadastro.model().item(0).setFlags(Qt.ItemIsEnabled)
        
        #setando os valores da combobox 'turma'
        self.ui.cboxTurma_PgCadastro.addItem("Selecione a turma do aluno")
        self.ui.cboxTurma_PgCadastro.addItem("1°")
        self.ui.cboxTurma_PgCadastro.addItem("2°")
        self.ui.cboxTurma_PgCadastro.addItem("3°"),
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxTurma_PgCadastro.model().item(0).setFlags(Qt.ItemIsEnabled)

        #botao que ira limpar todos os campos
        self.ui.btnLimparCampos_PgCadastro.clicked.connect(self.limparCampos)

        self.ui.cboxPeriodo_PgCadastro.currentIndexChanged.connect(self.exibirCursosPorPeriodo)
        self.exibirCursosPorPeriodo()  # Inicialmente, exibe todos os cursos
        #==================================================================


        #==================================================================
        #===================CONFIG PAG ATUALIZAR ALUNO=====================
        #==================================================================
        #botao que ira carregar a imagem do aluno      
        self.ui.btnCarregarFT_PgAtualizar.clicked.connect(self.carregar_imagemPgAtualizar)       

        #setando os valores da combobox 'periodo' 
        self.ui.cboxPeriodo_PgAtualizar.addItem("Selecione o período do aluno")
        self.ui.cboxPeriodo_PgAtualizar.addItem("Manhã")
        self.ui.cboxPeriodo_PgAtualizar.addItem("Tarde")
        self.ui.cboxPeriodo_PgAtualizar.addItem("Noite")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxPeriodo_PgAtualizar.model().item(0).setFlags(Qt.ItemIsEnabled)
        
        #setando na combobox 'curso' para ajudar na seleção(placeholder)
        self.ui.cboxCurso_PgAtualizar.addItem("Selecione o curso do aluno")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxCurso_PgAtualizar.model().item(0).setFlags(Qt.ItemIsEnabled)

        #setando os valores da combobox 'turma'
        self.ui.cboxTurma_PgAtualizar.addItem("Selecione a turma do aluno")
        self.ui.cboxTurma_PgAtualizar.addItem("1°")
        self.ui.cboxTurma_PgAtualizar.addItem("2°")
        self.ui.cboxTurma_PgAtualizar.addItem("3°"),
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxTurma_PgAtualizar.model().item(0).setFlags(Qt.ItemIsEnabled)

        self.ui.cboxPeriodo_PgAtualizar.currentIndexChanged.connect(self.exibirCursosPorPeriodo_PgAtualizar)
        self.exibirCursosPorPeriodo()  # Inicialmente, exibe todos os cursos
        #==================================================================


        #==================================================================
        #===================CONFIG PAG PESQUISAR ALUNO=====================
        #==================================================================
        #setando os valores da combobox 'periodo' 
        self.ui.cboxPeriodo_PgPesquisar.addItem("Selecione o período do aluno")
        self.ui.cboxPeriodo_PgPesquisar.addItem("Manhã")
        self.ui.cboxPeriodo_PgPesquisar.addItem("Tarde")
        self.ui.cboxPeriodo_PgPesquisar.addItem("Noite")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxPeriodo_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)
        
        #setando na combobox 'curso' para ajudar na seleção(placeholder)
        self.ui.cboxCurso_PgPesquisar.addItem("Selecione o curso do aluno")
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxCurso_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)

        #setando os valores da combobox 'turma'
        self.ui.cboxTurma_PgPesquisar.addItem("Selecione a turma do aluno")
        self.ui.cboxTurma_PgPesquisar.addItem("1°")
        self.ui.cboxTurma_PgPesquisar.addItem("2°")
        self.ui.cboxTurma_PgPesquisar.addItem("3°"),
        #desabilitando a primeira opção 'selecione...'
        self.ui.cboxTurma_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)

        self.ui.cboxPeriodo_PgPesquisar.currentIndexChanged.connect(self.exibirCursosPorPeriodo_PgPesquisar)
        self.exibirCursosPorPeriodo_PgPesquisar()  # Inicialmente, exibe todos os cursos
        #==================================================================


    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #                    FUNÇOES DA CLASSE DIRETOR                        -
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------    
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
    #botao que ira redirecionar p/ pag alunos
    def on_btnAlunos_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    #botao que ira redirecionar p/ pag entradas
    def on_btnEntradas_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #================BOTOES DO MENU LATERAL================
    #botoes que ira redirecionar p/ pag home
    def on_btnHomeLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def on_btnHomeLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    #botoes que ira redirecionar p/ pag alunos
    def on_btnAlunosLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def on_btnAlunosLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    #botoes que ira redirecionar p/ pag entradas
    def on_btnEntradasLateral_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def on_btnEntradasLAberto_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    #funcao para verificar a pagina atual e funcionar o botão voltar
    def on_btnVoltarLateral_clicked(self):
        #0 = pag home
        #1 = pag alunos
        #2 = pag entradas
        #3 = pag cadastro
        #4 = pag atualizar
        #5 = pag pesquisar
        #6 = pag dados turma
        #7 = pag dados aluno

        telaAtual = self.ui.stackedWidget.currentIndex()

        #se tiver na tela home, irá voltar para tela home
        if telaAtual == 0:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela alunos, irá voltar para tela home
        elif telaAtual == 1:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela entradas, irá voltar para tela home
        elif telaAtual == 2:
            self.ui.stackedWidget.setCurrentIndex(0)
        #se tiver na tela cadastro, irá voltar para tela home
        elif telaAtual == 3:
            telaAtual = 3
            self.ui.stackedWidget.setCurrentIndex(1)

    #===============funcao de abrir tela de login, que ira ser exibida ao desconectar===============
    def abrirTelaLogin(self):
        #criando uma instancia da tela de login
        self.telaLogin = MainWindow()  
        #exibindo a tela
        self.telaLogin.show()
        #fecha a tela anterior
        self.close()  



    #=================================================
    #================FUNCAO PAG ALUNOS================
    #================================================
    #botões pagina alunos, funcoes para trocar de pagina
    def on_btnPgCadastrarAlunos_PgAlunos_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    def on_btnPgProcurarAlunos_PgAlunos_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(5)
    #=================================================
    #=================================================

    
    #=================================================
    #==============FUNCAO PAG PESQUISAR===============
    #=================================================
    #botao que ira redirecionar p/ pag turma
    def btnBuscarTurma(self):
        self.ui.stackedWidget.setCurrentIndex(6)
    
    #botao que ira redirecionar p/ pag alunoRm
    def btnBuscarRm(self):
        self.ui.stackedWidget.setCurrentIndex(7)
    #=================================================
    #=================================================


    #=================================================
    #=============FUNCAO PAG DADOS ALUNO==============
    #=================================================
    #botao que ira redirecionar p/ pag dados alunos
    def btnAtualizarAluno_PgDadosAluno(self):
        self.ui.stackedWidget.setCurrentIndex(4)
    #=================================================
    #=================================================

    #=================================================
    #===========FUNCAO PAG CADASTRAR ALUNO============
    #=================================================
    #funcao que ira cadastrar aluno

    def cadastrarAluno(self):
        nome = self.ui.etyNome_PgCadastro.text()
        rm = self.ui.etyRM_PgCadastro.text()
        checbox_periodo = self.ui.cboxPeriodo_PgCadastro.currentText()
        checkbox_curso = self.ui.cboxCurso_PgCadastro.currentText()
        checkbox_turma = self.ui.cboxTurma_PgCadastro.currentText()
        fotoAlu = self.ui.btnCarregarFT_PgCadastro.isChecked()

        #ira fazer a validação dos campos não preechidos
        if(nome == '' or rm == '' or checbox_periodo == 'Selecione o período do aluno' or checkbox_curso == 'Selecione o curso do aluno' or 
           checkbox_turma == 'Selecione a turma do aluno'):
            #mensagem de campos nao preenchidos
            QMessageBox.warning(self, "Aviso", "Preencha todos os campos!")

            #validações de nao preechimento dos campos, setando os campos nao preenchidos com cor vermelha
            if(nome == ''):
                self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(rm == ''):
                self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')

            if(checbox_periodo == 'Selecione o período do aluno'):
                self.ui.cboxPeriodo_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(checkbox_curso == 'Selecione o curso do aluno'):
                self.ui.cboxCurso_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')
            
            if(checkbox_turma == 'Selecione a turma do aluno'):
                self.ui.cboxTurma_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid red; color:#ffffff')

            #validações de preechimento corretos dos campos, setando os campos preenchidos com cor verde
            if(nome != ''):
                self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(rm != ''):
                self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(checbox_periodo != 'Selecione o período do aluno'):
                self.ui.cboxPeriodo_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(checkbox_curso != 'Selecione o curso do aluno'):
                self.ui.cboxCurso_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
            if(checkbox_turma != 'Selecione a turma do aluno'):
                self.ui.cboxTurma_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid green; color:#ffffff')
            
        #se os campos estiverem preechidos
        else:
            BancoTcc.cursor.execute("""
            INSERT INTO cadastroAlu (nome, rm, checbox_periodo, checkbox_curso, checkbox_turma, fotoAlu) VALUES(?, ?, ?, ?, ?, ?)
            """, (nome, rm, checbox_periodo, checkbox_curso, checkbox_turma, fotoAlu))
            BancoTcc.conn.commit()
            QMessageBox.information(self, "Cadastro Concluido", "Cadastro Realizado com Sucesso!!")

            #limpando todos os campos apos o cadastro
            self.limparCampos()
                 

    #funcao que ira limpar os campos
    def limparCampos(self):
        #limpando as caixas de texto
        self.ui.etyNome_PgCadastro.setText('')
        self.ui.etyRM_PgCadastro.setText('')
        #limpando a seleção da combobox
        self.ui.cboxPeriodo_PgCadastro.setCurrentIndex(0)
        self.ui.cboxCurso_PgCadastro.setCurrentIndex(0)
        self.ui.cboxTurma_PgCadastro.setCurrentIndex(0)

        #retornando as cores iniciais dos campos
        self.ui.etyNome_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid #000000; color:#ffffff')
        self.ui.etyRM_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border: 2px solid #000000; color:#ffffff')
        self.ui.cboxPeriodo_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
        self.ui.cboxCurso_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')
        self.ui.cboxTurma_PgCadastro.setStyleSheet('background-color: #069E6E; border-radius:5px; border-color:#069E6E; color:#ffffff')

        #retirando a imagem do aluno
        width, height = 200, 210
        fundoImagem = QImage(width, height, QImage.Format_RGB32)
        fundoImagem.fill(QColor(241, 241, 241))  # Preenche com branco
        self.pixmap = QPixmap.fromImage(fundoImagem)
        self.ui.lbl_ImgAluno.setPixmap(self.pixmap)

    #funcao que ira exibir os cursos de acordo com o periodo selecionado
    def exibirCursosPorPeriodo(self):
        #varivel contendo os curso existentes por periodo
        cursos_PorPeriodo = {
            "Manhã": ["Administração", "Desenvolvimento de Sistemas", "Recursos Humanos"],
            "Tarde": ["Administração", "Desenvolvimento de Sistemas", "Logística"],
            "Noite": ["Contabilidade", "Recursos Humanos", "Serviços Jurídicos"]
        }

        #variavel que recebe o periodo que o usuario selecionou
        periodo_selecionado = self.ui.cboxPeriodo_PgCadastro.currentText()
        #variavel que exibi os cursos disponiveis de acordo com o periodo selecionado
        cursos_disponiveis = cursos_PorPeriodo.get(periodo_selecionado, [])
        
        self.ui.cboxCurso_PgCadastro.clear()
        #opcao do combobox para ser utilizada como ajuda(placeholder)
        self.ui.cboxCurso_PgCadastro.addItem("Selecione o curso do aluno")
        #adicionando opções de curso na combobox de acordo com o perido selecionado
        self.ui.cboxCurso_PgCadastro.addItems(cursos_disponiveis)
        #desabilitando a opção 'selecione...'
        self.ui.cboxCurso_PgCadastro.model().item(0).setFlags(Qt.ItemIsEnabled)

    #funcao que ira carregar a foto do aluno
    def carregar_imagem(self):
        #cria um objeto de opções para a caixa de dialogo
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg)", options=options)
        
        #verifica se o caminho do arquivo (filename) não está vazio
        if filename:
            #cria um objeto QPixmap a partir do arquivo de imagem selecionado
            pixmap = QPixmap(filename)
            #tamanho da imagem
            pixmap = pixmap.scaled(200, 210)
            #setando imagem na label da imagem
            self.ui.lbl_ImgAluno.setPixmap(pixmap)
    #=================================================
    #=================================================


    #=================================================
    #===========FUNCAO PAG ATUALIZAR ALUNO============
    #=================================================
    #funcao que ira atualizar aluno
    def atualizarAluno(self):
        nome = self.ui.etyNome_PgCadastro.text()
        rm = self.ui.etyRM_PgCadastro.text()
        checbox_periodo = self.ui.cboxPeriodo_PgCadastro.currentText()
        checkbox_curso = self.ui.cboxCurso_PgCadastro.currentText()
        checkbox_turma = self.ui.cboxTurma_PgCadastro.currentText()
        fotoAlu = self.ui.btnCarregarFT_PgCadastro.isChecked()

        BancoTcc.cursor.execute("""
        UPDATE cadastroAlu SET nome=?, rm=?, checbox_periodo=?, checkbox_curso=?, checkbox_turma=?, fotoAlu=?
        WHERE """, (nome, rm, checbox_periodo, checkbox_curso, checkbox_turma, fotoAlu,))
        BancoTcc.conn.commit()
        messagebox.showinfo(title="Atualização do Aluno", message="Aluno atualizado com Sucesso!!")


    #=================================================
    #===========FUNCAO PARA DELETAR ALUNO=============
    #=================================================  
    def deletarAluno(self):
        nome = self.ui.etyNome_PgCadastro.text()
        rm = self.ui.etyRM_PgCadastro.text()
        checbox_periodo = self.ui.cboxPeriodo_PgCadastro.currentText()
        checkbox_curso = self.ui.cboxCurso_PgCadastro.currentText()
        checkbox_turma = self.ui.cboxTurma_PgCadastro.currentText()
        fotoAlu = self.ui.btnCarregarFT_PgCadastro.isChecked()

        BancoTcc.cursor.execute("""
        DELETE FROM cadastroAlu WHERE nome=?, rm=?, checbox_periodo=?, checkbox_curso=?, checkbox_turma=?, fotoAlu=?
        """, (nome, rm, checbox_periodo, checkbox_curso, checkbox_turma, fotoAlu,))
        BancoTcc.conn.commit()
        messagebox.showinfo(title="Exclusão do Aluno", message="Aluno excluido com Sucesso!!")

    #funcao que ira exibir os cursos de acordo com o periodo selecionado
    def exibirCursosPorPeriodo_PgAtualizar(self):
        #varivel contendo os curso existentes por periodo
        cursos_PorPeriodo = {
            "Manhã": ["Administração", "Desenvolvimento de Sistemas", "Recursos Humanos"],
            "Tarde": ["Administração", "Desenvolvimento de Sistemas", "Logística"],
            "Noite": ["Contabilidade", "Recursos Humanos", "Serviços Jurídicos"]
        }

        #variavel que recebe o periodo que o usuario selecionou
        periodo_selecionado = self.ui.cboxPeriodo_PgAtualizar.currentText()
        #variavel que exibi os cursos disponiveis de acordo com o periodo selecionado
        cursos_disponiveis = cursos_PorPeriodo.get(periodo_selecionado, [])
        
        self.ui.cboxCurso_PgAtualizar.clear()
        #opcao do combobox para ser utilizada como ajuda(placeholder)
        self.ui.cboxCurso_PgAtualizar.addItem("Selecione o curso do aluno")
        #adicionando opções de curso na combobox de acordo com o perido selecionado
        self.ui.cboxCurso_PgAtualizar.addItems(cursos_disponiveis)
        #desabilitando a opção 'selecione...'
        self.ui.cboxCurso_PgAtualizar.model().item(0).setFlags(Qt.ItemIsEnabled)

    #funcao que ira carregar a foto do aluno
    def carregar_imagemPgAtualizar(self):
        #cria um objeto de opções para a caixa de dialogo
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Selecionar Imagem", "", "Imagens (*.png *.jpg *.jpeg)", options=options)
        
        #verifica se o caminho do arquivo (filename) não está vazio
        if filename:
            #cria um objeto QPixmap a partir do arquivo de imagem selecionado
            pixmap = QPixmap(filename)
            #tamanho da imagem
            pixmap = pixmap.scaled(200, 210)
            #setando imagem na label da imagem
            self.ui.lbl_ImgAluno_PgAtualizar.setPixmap(pixmap)
    #=================================================
    #=================================================


    #=================================================
    #===========FUNCAO PAG PESQUISAR ALUNO============
    #=================================================
    #funcao que ira exibir os cursos de acordo com o periodo selecionado
    def exibirCursosPorPeriodo_PgPesquisar(self):
        #varivel contendo os curso existentes por periodo
        cursos_PorPeriodo = {
            "Manhã": ["Administração", "Desenvolvimento de Sistemas", "Recursos Humanos"],
            "Tarde": ["Administração", "Desenvolvimento de Sistemas", "Logística"],
            "Noite": ["Contabilidade", "Recursos Humanos", "Serviços Jurídicos"]
        }

        #variavel que recebe o periodo que o usuario selecionou
        periodo_selecionado = self.ui.cboxPeriodo_PgPesquisar.currentText()
        #variavel que exibi os cursos disponiveis de acordo com o periodo selecionado
        cursos_disponiveis = cursos_PorPeriodo.get(periodo_selecionado, [])
        
        self.ui.cboxCurso_PgPesquisar.clear()
        #opcao do combobox para ser utilizada como ajuda(placeholder)
        self.ui.cboxCurso_PgPesquisar.addItem("Selecione o curso do aluno")
        #adicionando opções de curso na combobox de acordo com o perido selecionado
        self.ui.cboxCurso_PgPesquisar.addItems(cursos_disponiveis)
        #desabilitando a opção 'selecione...'
        self.ui.cboxCurso_PgPesquisar.model().item(0).setFlags(Qt.ItemIsEnabled)
    #=================================================
    #=================================================

#=========================================================================#
#                                                                         #
#                CLASSE P/ A TELA PRINCIPAL PARA O SEGURANÇA              #
#                                                                         #
#=========================================================================#
class TelasSeguranca(QMainWindow):
    #CONFIG INICIAIS P/ SER EXECUTADAS AO ABRIR A TELA SEGURANÇA
    def __init__(self):
        super(TelasSeguranca, self).__init__()
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
        xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'  

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
        self.telaLogin = MainWindow()  
        #exibindo a tela
        self.telaLogin.show()
        #fecha a tela anterior
        self.close()  



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
        
        #=======================BOTOES DAS FUNCIONALIDADES===========================
        #botao de exibir a senha
        self.ui.chkboxExibirSenha.stateChanged.connect(self.exibirSenha)
        #botao de fazer o login
        self.ui.btnLogin.clicked.connect(self.fazerLogin)

    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #                      FUNÇOES DA CLASSE LOGIN                        -
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------   
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
                self.telas_diretor = TelasDiretor() #crie uma instância da segunda tela
                self.telas_diretor.show()
                self.close() #fecha a tela de login 

            #se for as credenciais do segurança, ira abrir a tela do segurança
            else:
                self.telas_seguranca = TelasSeguranca() #crie uma instância da segunda tela
                self.telas_seguranca.show()
                self.close() #fecha a tela de login

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
