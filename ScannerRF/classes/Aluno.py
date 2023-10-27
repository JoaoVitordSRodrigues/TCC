#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QMessageBox, QComboBox, QFileDialog, QStackedWidget, QTableWidgetItem
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import pyqtSlot, QTextStream
#importando da pasta 'telas_py' as telas do diretor em python
from telas_py.telas_Diretor import Ui_MainWindow as Ui_Telas_Diretor
from PyQt5.QtCore import Qt
import re

class Aluno:

    #=================================================================================================
    #===========FUNCAO PAG CADASTRAR ALUNO============================================================
    #=================================================================================================
    #funcao que ira cadastrar aluno
    def cadastrarAluno(self, nomeAluno, rmAluno, periodoAluno, cursoAluno, serie_turmaAluno, face_aluno):
        #obtendo os valores contidos nos campos
        nome = nomeAluno
        rm = rmAluno
        periodo = periodoAluno
        curso = cursoAluno
        serie_turma = serie_turmaAluno
        self.face_aluno = face_aluno

        #ira fazer a validação dos campos não preechidos
        if(nome == '' or rm == '' or periodo == 'Selecione o período do aluno' or curso == 'Selecione o curso do aluno' or 
           serie_turma == 'Selecione a turma do aluno'):
            return "Preencha todos os campos!"
        #verifica se o nome é uma string não vazia e contém apenas letras e espaços
        elif not re.match(r'^[A-Za-z\s]+$', nome):
            return "O nome deve conter apenas letras e espaços." # Saia da função se o nome for inválido
        #verifica se o RM contém apenas dígitos
        elif not re.match(r'^\d+$', rm):
            return "O RM deve conter apenas números." # Saia da função se o RM for inválido)
        elif self.face_aluno == None:
            return "Selecione alguma imagem do aluno. O aluno não contém imagem para cadastrar."
        #se os campos estiverem preechidos
        else:
            return "foi"
            '''
            id_periodo = 0
            id_curso = 0

            #setando o id do periodo
            if(periodo == 'Manhã'):
                id_periodo = id_periodo + 1    
            elif(periodo == 'Tarde'):
                id_periodo = id_periodo + 2       
            else:#periodo da noite
                id_periodo = id_periodo + 3

            #setando o id do curso
            if(curso == 'Administração'):
                id_curso = id_curso + 1      
            elif(curso == 'Contabilidade'):
                id_curso = id_curso + 2        
            elif(curso == 'Desenvolvimento de Sistemas'):
                id_curso = id_curso + 3    
            elif(curso == 'Logística'):
                id_curso = id_curso + 4   
            elif(curso == 'Recursos Humanos'):
                id_curso = id_curso + 5   
            else:#servicos juridicos
                id_curso = id_curso + 6
            
            #se obter a imagem da face do aluno
            if self.face_aluno is not None:
                #consulta a tabela 'turma' para encontrar o ID da turma correspondente
                BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
                result = BancoTcc.cursor.fetchone()
                #se obter o id da turma
                if result:
                    id_turma = result[0]  #setando o id da turma em uma variavel
                    #inserindo o aluno na tabela 'alunos' associando-o à turma correta
                    BancoTcc.cursor.execute("INSERT INTO aluno (id_turma, rm_aluno, nome_aluno, face_aluno) VALUES (?, ?, ?, ?)", (id_turma, rm, nome, self.face_aluno))
                    BancoTcc.conn.commit()
                    QMessageBox.information(self, "Cadastro Concluido", "Cadastro Realizado com Sucesso!!")#mensagem de cadastro concluido
                    #limpando todos os campos apos o cadastro
                    self.limparCampos()
                #se nao obter o id da turma           
                else:
                    QMessageBox.information(self, "Turma não encontrada", "Turma não encontrada. O aluno não foi cadastrado.!")             
            #se nao obter a imagem da face do aluno
            else:
                QMessageBox.information(self, "Imagem não encontrada", "Selecione alguma imagem do aluno. O aluno não contém imagem para cadastrar.")  '''



    #=================================================================================================
    #===========FUNCAO PAG ATUALIZAR ALUNO============================================================
    #=================================================================================================
    #funcao que ira atualizar aluno
    def atualizarAluno(self):
        #id do aluno que sera atualizado
        id_aluno_atualizar = self.id_aluno
        #se obter o id do aluno
        if id_aluno_atualizar is not None:
            #obtendo os valores dos campos 
            nome = self.ui.etyNome_PgAtualizar.text()
            rm = self.ui.etyRM_PgAtualizar.text()
            periodo = self.ui.cboxPeriodo_PgAtualizar.currentText()
            curso = self.ui.cboxCurso_PgAtualizar.currentText()
            serie_turma = self.ui.cboxTurma_PgAtualizar.currentText()
         
            dialogo = QMessageBox()  #caixa de mensagem          
            dialogo.setWindowTitle("Atualização do cadastro do aluno")  #titulo da caixa de mensagem         
            dialogo.setText("Deseja atualizar os dados do cadastro do aluno?:")  #texto da caixa de mensagem      
            dialogo.setIcon(QMessageBox.Information)  #define o ícone da caixa de diálogo
            dialogo.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)  #define os botões padrão como "Ok" e "Cancelar"
            resultado = dialogo.exec_()

            #se o usuario clicar em 'ok' ira atualizar o aluno
            if resultado == QMessageBox.Ok:
                #se obter o id do aluno
                if id_aluno_atualizar is not None:
                    id_periodo = 0
                    id_curso = 0

                    #setando o id do periodo
                    if(periodo == 'Manhã'):
                        id_periodo = id_periodo + 1
                    elif(periodo == 'Tarde'):
                        id_periodo = id_periodo + 2
                    else:#periodo da noite
                        id_periodo = id_periodo + 3

                    #setando o id do curso
                    if(curso == 'Administração'):
                        id_curso = id_curso + 1
                    elif(curso == 'Contabilidade'):
                        id_curso = id_curso + 2
                    elif(curso == 'Desenvolvimento de Sistemas'):
                        id_curso = id_curso + 3
                    elif(curso == 'Logística'):
                        id_curso = id_curso + 4
                    elif(curso == 'Recursos Humanos'):
                        id_curso = id_curso + 5
                    else:#servicos juridicos
                        id_curso = id_curso + 6
                    
                    #consulta a tabela 'turma' para encontrar o ID da turma correspondente
                    BancoTcc.cursor.execute("SELECT id_turma FROM turma WHERE id_periodo = ? AND id_curso = ? AND serie_turma = ?", (id_periodo, id_curso, serie_turma))
                    result = BancoTcc.cursor.fetchone()
                    #se obter o id da turma
                    if result:
                        id_turma = result[0]  #setando o id da turma em uma variavel
                        #atualizando os dados do aluno com base no id do aluno selecionado, associando-o à turma correta
                        BancoTcc.cursor.execute("UPDATE aluno SET id_turma=?, rm_aluno=?, nome_aluno=?, face_aluno=? WHERE id_aluno = ?", (id_turma, rm, nome, self.face_aluno, id_aluno_atualizar))
                        BancoTcc.conn.commit()
                        QMessageBox.information(self, "Atualização do aluno concluída", "Dados do cadastro do aluno atualizado com sucesso!")
                        #redirecionando para pagina de dados do alunos
                        self.ui.stackedWidget.setCurrentIndex(7)

                        #EXCUTANDO SQL NOVAMENTE PARA OBTER OS NOVOS DADOS CADASTRADOS E ASSIM EXIBIR NA PAG DE DADOS DO ALUNO
                        consulta_sql = "SELECT * FROM aluno WHERE id_aluno = ?"  #consulta sql que selcionar os dados do aluno de acordo com o id dele
                        BancoTcc.cursor.execute(consulta_sql, (self.id_aluno,))
                        dados_aluno = BancoTcc.cursor.fetchone()  #armazenando os dados do aluno
                        #se obter os dados do aluno
                        if dados_aluno:
                            self.id_aluno = dados_aluno[0]  #variavel que recebe o id do aluno, o '0' é a coluna em que o id do aluno esta
                            id_turma = dados_aluno[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                            rm_aluno = dados_aluno[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                            nome_aluno = dados_aluno[3]  #variavel que recebe o nome do aluno, o '3' é a coluna em que o nome do aluno esta
                            self.face_alunoAtt = dados_aluno[4]  #variavel que recebe a face do aluno, o '4' é a coluna em que a face do aluno esta

                            consulta_turma = "SELECT * FROM turma WHERE id_turma = ?"  #consulta SQL para selecionar os dados da turma com base no id
                            BancoTcc.cursor.execute(consulta_turma, (id_turma,))
                            dados_turma = BancoTcc.cursor.fetchone()  #armazenando os dados da turma 
                            #se obter os dados da turma
                            if dados_turma is not None:
                                id_curso = dados_turma[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
                                id_periodo = dados_turma[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
                                serie_turma = dados_turma[3] #variavel que recebe o id da serie, '3' é coluna em que o id da serie esta 

                                #consulta SQL para selecionar os dados do curso com base no id do curso
                                consulta_curso = "SELECT * FROM curso WHERE id_curso = ?"
                                BancoTcc.cursor.execute(consulta_curso, (id_curso,))
                                dados_curso = BancoTcc.cursor.fetchone()  #armazenando os dados do curso

                                #consulta SQL para selecionar os dados do período com base no id do período
                                consulta_periodo = "SELECT * FROM periodo WHERE id_periodo = ?"
                                BancoTcc.cursor.execute(consulta_periodo, (id_periodo,))
                                dados_periodo = BancoTcc.cursor.fetchone()  #armazenando os dados do periodo

                                #se obter os dados do curso e do periodo
                                if dados_curso is not None and dados_periodo is not None:
                                    nome_curso = dados_curso[1]  #variavel que recebe o nome do curso, '1' é coluna em que o nome do curso esta 
                                    turno_periodo = dados_periodo[1]  #variavel que recebe o turno do curso, '1' é coluna em que o turno do curso esta 

                                    #setando os dados na pag Dados Turma para a visualização
                                    self.ui.lbl_Nome_PgDadosAluno.setText(nome_aluno)
                                    self.ui.lbl_Rm_PgDadosAluno.setText(str(rm_aluno))
                                    self.ui.lbl_Periodo_PgDadosAluno.setText(turno_periodo)
                                    self.ui.lbl_NomeCurso_PgDadosAluno.setText(nome_curso)
                                    self.ui.lbl_Turma_PgDadosAluno.setText(serie_turma + ' ' + nome_curso + ' ' + turno_periodo)                 
                                    # Crie um QPixmap a partir dos dados da imagem
                                    pixmap = QPixmap()
                                    pixmap.loadFromData(self.face_alunoAtt)
                                    # Defina o QPixmap na label
                                    self.ui.lbl_ImgAluno_PgDadosAluno.setPixmap(pixmap)
                                    self.ui.lbl_ImgAluno_PgDadosAluno.setScaledContents(True)

                                    #setando os dados nas variaveis que foram iniciadas no 'def __init__', nas configs iniciais
                                    self.turno_periodoAtt = turno_periodo
                                    self.nome_cursoAtt = nome_curso
                                    self.serie_turmaAtt = serie_turma
                                #se nao obter os dados do curso e do periodo
                                else:
                                    QMessageBox.information(self, "Sem resultados!", "Nenhum resultado encontrado para o ID do curso ou do período.")   
                            #se nao obter os dados da turma
                            else:
                                QMessageBox.information(self, "Informação", "Nenhuma turma encontrada com o id informado.")
                        #se nao obter os dados do aluno    
                        else:
                            QMessageBox.information(self, "Informação", "Nenhum aluno encontrado com o RM informado.")
                    #se nao obter o id da turma
                    else:
                        QMessageBox.information(self, "Turma não encontrada", "Turma não encontrada. O aluno não foi atualizado.!")
                #se obter o id do aluno
                else:
                    QMessageBox.warning(self, "Exclusão do aluno", "ID do aluno não definido ou encontrado.")
            #se clicar em 'cancel' ira interromper a atualização
            elif resultado == QMessageBox.Cancel:
                QMessageBox.warning(self, "Atualização do aluno interrompida", "Atualização interrompida com sucesso!")
        #se nao obter o id do aluno
        else:
            QMessageBox.warning(self, "Atualização do aluno falhou", "ID do aluno não definido ou encontrado.")

    #botao que ira deletar o aluno de acordo com o id
    def deletarAluno(self):       
        dialogo = QMessageBox()#caixa de mensagem    
        dialogo.setWindowTitle("Exclusão do aluno")#titulo da caixa de mensagem    
        dialogo.setText("Deseja deletar o cadastro do aluno?:")#texto da caixa de mensagem
        dialogo.setIcon(QMessageBox.Information)#define o ícone da caixa de diálogo
        dialogo.setStandardButtons( QMessageBox.Ok | QMessageBox.Cancel)#define os botões padrão como "Ok" e "Cancelar"
        opcao_Selecionada = dialogo.exec_()

        #se o usuario clicar em 'ok' ira deletar o aluno
        if opcao_Selecionada == QMessageBox.Ok:
            #se obter o id do aluno
            if self.id_aluno is not None:
                id_aluno_excluir = self.id_aluno  #id do aluno que ira ser excluido
                #instrução sql que ira deletar o aluno com base no id do aluno
                BancoTcc.cursor.execute("DELETE FROM aluno WHERE id_aluno = ?", (id_aluno_excluir,))
                BancoTcc.conn.commit()
                #mensagem que o aluno foi excluido
                QMessageBox.information(self, "Exclusão do aluno concluída", "Cadastro do aluno deletado com sucesso!")
                self.ui.stackedWidget.setCurrentIndex(5)#redirecionando para a pag pesquisar
            #se nao obter o id do aluno
            else:
                QMessageBox.warning(self, "Exclusão do aluno", "ID do aluno não definido. Selecione um aluno para excluir.")
        #se clicar em 'cancel' ira interromper a exclusão
        elif opcao_Selecionada == QMessageBox.Cancel:
            QMessageBox.warning(self, "Exclusão do aluno interrompida", "Exclusão interrompida com sucesso!")