#IMPORTANDO AS BIBLIOTECAS
import sys
import io
#importando da pasta 'bd' o banco
from bd import BancoTcc
from PyQt5.QtGui import QPixmap, QImage, QColor
#importando da pasta 'telas_py' as telas do diretor em python
from telas_py.telas_Diretor import Ui_MainWindow as Ui_Telas_Diretor
import re

class Aluno:
    def __init__(self):
        self.id_aluno = None

    #=================================================================================================
    #===========FUNCAO PAG CADASTRAR ALUNO============================================================
    #=================================================================================================
    #funcao que ira cadastrar aluno
    def cadastrarAluno(self, nome, rm, periodo, curso, serie_turma, face_alunoCadastro):
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
            #inserindo o aluno na tabela 'alunos' associando-o à turma correta
            BancoTcc.cursor.execute("INSERT INTO aluno (id_turma, rm_aluno, nome_aluno, face_aluno) VALUES (?, ?, ?, ?)", (id_turma, rm, nome, face_alunoCadastro))
            BancoTcc.conn.commit()
            resultado = "Cadastro Realizado com Sucesso!"  # Valor padrão 
        #se nao obter o id da turma           
        else:
            resultado = "Turma não encontrada. O aluno não foi cadastrado." 

        return resultado        


    def visualizarAluno(self, rm):
        consulta_sql = "SELECT * FROM aluno WHERE rm_aluno = ?"  #consulta sql que selcionar os dados do aluno de acordo com o rm dele
        BancoTcc.cursor.execute(consulta_sql, (rm,))
        dados_aluno = BancoTcc.cursor.fetchone()  #armazenando os dados do aluno
        #se obter os dados do aluno
        if dados_aluno:
            id_aluno = dados_aluno[0]  #variavel que recebe o id do aluno, o '0' é a coluna em que o id do aluno esta
            id_turma = dados_aluno[1]  #variavel que recebe o id do curso, '1' é coluna em que o id do curso esta 
            rm_aluno = dados_aluno[2]  #variavel que recebe o id do periodo, '2' é coluna em que o id do periodo esta 
            nome_aluno = dados_aluno[3]  #variavel que recebe o nome do aluno, o '3' é a coluna em que o nome do aluno esta
            face_aluno = dados_aluno[4]  #variavel que recebe a face do aluno, o '4' é a coluna em que a face do aluno esta

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

                    #setando o nome abreviado do curso para exibição
                    if(id_curso == 1):
                        nomeAbrevi_curso = 'ADM'
                    elif(id_curso == 2):
                        nomeAbrevi_curso = 'CONT'
                    elif(id_curso == 3):
                        nomeAbrevi_curso = 'DS'
                    elif(id_curso == 4):
                        nomeAbrevi_curso = 'LOG'
                    elif(id_curso == 5):
                        nomeAbrevi_curso = 'RH'
                    else:#servicos juridicos
                        nomeAbrevi_curso = 'JUR'

                    return id_aluno, nome_aluno, rm_aluno, turno_periodo, nome_curso, serie_turma, nomeAbrevi_curso, face_aluno

                #se nao obter os dados do curso e do periodo
                else:
                    resultado = "Nenhum resultado encontrado para o ID do curso ou do período."   
                    return resultado 
            #se nao obter os dados da turma
            else:
                resultado = "Nenhuma turma encontrada com o id informado."
                return resultado 
        #se nao obter os dados do aluno    
        else:
            resultado = "Nenhum aluno encontrado com o RM informado."
            return resultado 
    
    def deletarAluno(self, id_aluno_excluir):       
        #se obter o id do aluno
        if id_aluno_excluir is not None:
            #instrução sql que ira deletar o aluno com base no id do aluno
            BancoTcc.cursor.execute("DELETE FROM aluno WHERE id_aluno = ?", (id_aluno_excluir,))
            BancoTcc.conn.commit()
            #mensagem que o aluno foi excluido
            resultado = "Cadastro do aluno deletado com sucesso!"
            return resultado 
        #se nao obter o id do aluno
        else:
            resultado = "ID do aluno não definido. Selecione um aluno para excluir."
            return resultado 

    def atualizarAluno(self, id_aluno_atualizar, nome, rm, periodo, curso, serie_turma, face_alunoAtualizar):
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
            BancoTcc.cursor.execute("UPDATE aluno SET id_turma=?, rm_aluno=?, nome_aluno=?, face_aluno=? WHERE id_aluno = ?", (id_turma, rm, nome, face_alunoAtualizar, id_aluno_atualizar))
            BancoTcc.conn.commit()
            resultado = "Dados do cadastro do aluno atualizado com sucesso!"
        #se nao obter o id da turma
        else:
            resultado = "Turma não encontrada. O aluno não foi atualizado.!"

        return resultado
    
            