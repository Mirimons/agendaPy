import mysql.connector
from PyQt5 import uic, QtWidgets

banco = mysql.connector.connect( 
    host = "localhost",
    user = "root",
    password = "",
    database = "agenda"
)

idEdicao = None

def main():
    campoNome = agenda.leNome.text()
    print("Nome: ", campoNome)
    campoEmail = agenda.leEmail.text()
    print("Email: ", campoEmail)
    campoTelefone = agenda.leTelefone.text()
    print("Telefone: ", campoTelefone)

    tipoTelefone = ""

    if agenda.rbResidencial.isChecked():
        print("Tipo de telefone é residencial")
        tipoTelefone = "Residencial"
    elif agenda.rbCelular.isChecked():
        print("Tipo de telefone é celular")
        tipoTelefone = "Celular"
    else:
        print("Informe o tipo de telefone!")
        tipoTelefone = "Não informado"
        
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO contatos (nome, email, telefone, tipoTelefone) VALUES (%s, %s, %s, %s)"
    dados = (str(campoNome), str(campoEmail), str(campoTelefone), tipoTelefone)
    cursor.execute(comando_SQL, dados)
    banco.commit()
    
    #Limpa os campos quando aperta no "Cadastrar"
    agenda.leNome.setText("");
    agenda.leEmail.setText("");
    agenda.leTelefone.setText("");

    print("Contato cadastrado com sucesso!")

def telaConsulta():
    agendaConsultar.show()
    
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    #print(contatos_lidos)
    
    agendaConsultar.tabela.setRowCount(len(contatos_lidos))
    agendaConsultar.tabela.setColumnCount(5)
    
    for i in range(0,len(contatos_lidos)):
        for j in range(0, 5):
            agendaConsultar.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(contatos_lidos[i][j])))


def telaAlterar():
    global idEdicao
    
    linha = agendaConsultar.tabela.currentRow()
    if linha == -1:
       QtWidgets.QMessageBox.warning(agendaConsultar, "Atenção", "Selecione um contato para alterar!")
       return
    
    idEdicao = agendaConsultar.tabela.item(linha, 0).text()
    nome = agendaConsultar.tabela.item(linha, 1).text()
    email = agendaConsultar.tabela.item(linha, 2).text()
    telefone = agendaConsultar.tabela.item(linha, 3).text()
    tipoTelefone = agendaConsultar.tabela.item(linha, 4).text()
   
    agendaAlterar.leNome.setText(nome)
    agendaAlterar.leEmail.setText(email)
    agendaAlterar.leTelefone.setText(telefone)
   
    if tipoTelefone == "Residencial":
       agendaAlterar.rbResidencial.setChecked(True)
    elif tipoTelefone == "Celular":
       agendaAlterar.rbCelular.setChecked(True)       
   
    agendaAlterar.show()


def alterarContato():
    global idEdicao
    
    linhaContato = agendaConsultar.tabela.currentRow()
    if linhaContato == -1:
        QtWidgets.QMessageBox.warning(agendaConsultar, "Atenção", "Selecione um contato para alterar!")
        return

    novoNome = agendaAlterar.leNome.text()
    novoEmail = agendaAlterar.leEmail.text()
    novoTelefone = agendaAlterar.leTelefone.text()

    if agendaAlterar.rbResidencial.isChecked():
        novoTipoTelefone = "Residencial"
    elif agendaAlterar.rbCelular.isChecked():
        novoTipoTelefone = "Celular"
    else:
        novoTipoTelefone = "Não informado"
    
    try:
        cursor = banco.cursor()
        
        comando_SQL_update = """
            UPDATE contatos
            SET nome = %s, email = %s, telefone = %s, tipoTelefone = %s
            WHERE id = %s
        """
        dados = (novoNome, novoEmail, novoTelefone, novoTipoTelefone, idEdicao)
            
        cursor.execute(comando_SQL_update, dados)
        banco.commit()
        
        cursor.close()
    
        agendaAlterar.close()
    
        telaConsulta()
        
    except Exception as e:
        QtWidgets.QMessageBox.critical(agendaAlterar, "Erro", f"Erro ao alterar contato: {str(e)}")
    
    
def excluirContato():
    linhaContato = agendaConsultar.tabela.currentRow()
    agendaConsultar.tabela.removeRow(linhaContato)

    cursor = banco.cursor()
    comando_SQL = "SELECT id FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    valorId = contatos_lidos[linhaContato][0]
    cursor.execute("DELETE FROM contatos WHERE id=" + str(valorId))
    banco.commit()

    
app = QtWidgets.QApplication([])
agenda = uic.loadUi("agenda.ui")
agendaConsultar = uic.loadUi("listaContatos.ui")
agendaAlterar = uic.loadUi("alterar.ui")

agenda.btnCadastro.clicked.connect(main)
agenda.btnConsulta.clicked.connect(telaConsulta)
agendaConsultar.btnExcluir.clicked.connect(excluirContato)
agendaConsultar.btnAlterar.clicked.connect(telaAlterar)
agendaAlterar.btnAlterar.clicked.connect(alterarContato)

agenda.show()
app.exec()
