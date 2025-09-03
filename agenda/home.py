import mysql.connector
from PyQt5 import uic, QtWidgets

banco = mysql.connector.connect( 
    host = "localhost",
    user = "root",
    password = "etecembu@123",
    database = "agenda"
)


def main():
    campoNome = agenda.leNome.text()
    print("Nome; ", campoNome)
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
    
    #Limpa os cmapos quando aperta no "Cadastrar"
    agenda.leNome.setText("");
    agenda.leEmail.setText("");
    agenda.leTelefone.setText("");

    print("Contato cadastrado com sucesso!")

def telaConsulta():
    agendaConsulta.show()
    
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM contatos"
    cursor.execute(comando_SQL)
    contatos_lidos = cursor.fetchall()
    #print(contatos_lidos)
    
    agendaConsulta.tabela.setRowCount(len(contatos_lidos))
    agendaConsulta.tabela.setColumnCount(5)
    
    for i in range(0,len(contatos_lidos)):
        for j in range(0, 5):
            agendaConsulta.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(contatos_lidos[i][j])))
    



app = QtWidgets.QApplication([])
agenda = uic.loadUi("agenda.ui")
agenda.btnCadastro.clicked.connect(main)

agendaConsulta=uic.loadUi("listaContatos.ui")
agenda.btnConsulta.clicked.connect(telaConsulta)

agenda.show()
app.exec()
