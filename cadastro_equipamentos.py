from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas


numero_id = 0

db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='db'
    )


def editar_item():
    global numero_id

    linha = abrir_lista.tableWidget.currentRow()

    cursor = db.cursor()
    cursor.execute("SELECT id FROM EQUIPAMENTOS")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM EQUIPAMENTOS WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    tela_editar.lineEdit_6.setText(str(produto[0][5]))
    numero_id = valor_id


def salvar_valor_editado():
    global numero_id

    marca = tela_editar.lineEdit_2.text()
    modelo = tela_editar.lineEdit_3.text()
    num_serie = tela_editar.lineEdit_4.text()
    valor = tela_editar.lineEdit_5.text()
    categoria = tela_editar.lineEdit_6.text()

    cursor = db.cursor()
    cursor.execute(
        "UPDATE EQUIPAMENTOS SET marca = '{}', modelo = '{}', num_serie = '{}', valor ='{}', categoria ='{}' "
        "WHERE id = {}".format(marca, modelo, num_serie, valor, categoria,numero_id))
    db.commit()

    tela_editar.close()
    abrir_lista.close()
    chama_abrir_lista()


def excluir_item():
    linha = abrir_lista.tableWidget.currentRow()
    abrir_lista.tableWidget.removeRow(linha)

    cursor = db.cursor()
    cursor.execute("SELECT id FROM EQUIPAMENTOS")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM EQUIPAMENTOS WHERE id=" + str(valor_id))
    db.commit()


def gerar_pdf():
    cursor = db.cursor()
    comand_sql = "SELECT * FROM EQUIPAMENTOS"
    cursor.execute(comand_sql)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_equipamentos.pdf")
    pdf.setFont("Times-Bold", 18)
    pdf.drawString(200,800, "Equipamentos Cadastrados:")
    pdf.setFont("Times-Bold", 12)

    pdf.drawString(10,750, "ID")
    pdf.drawString(80,750, "MARCA")
    pdf.drawString(180,750, "MODELO")
    pdf.drawString(280,750, "S/N")
    pdf.drawString(380,750, "VALOR R$")
    pdf.drawString(480,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 25
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(80,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(180,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(280,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(380,750 - y, str(dados_lidos[i][4]))
        pdf.drawString(480,750 - y, str(dados_lidos[i][5]))

    pdf.save()
    print("PDF GERADO")


def funcao_principal():
    linha1 = formulario.line1.text()
    linha2 = formulario.line2.text()
    linha3 = formulario.line3.text()
    linha4 = formulario.line4.text()
    categoria = ""

    if formulario.radioButton_1.isChecked():
        print("Categoria GNSS")
        categoria = "GNSS"
    elif formulario.radioButton_2.isChecked():
        print("Categoria Estação Total")
        categoria = "Estação Total"
    elif formulario.radioButton_3.isChecked():
        print("Categoria Software")
        categoria = "Software"
    else:
        print("Categoria Acessório")
        categoria = "Acessório"

    print("Marca:", linha1)
    print("Modelo:", linha2)
    print("Nº de Série:", linha3)
    print("Valor R$:", linha4)

    cursor = db.cursor()
    comand_sql = "INSERT INTO EQUIPAMENTOS (marca,modelo,num_serie,valor,categoria) VALUES (%s, %s, %s, %s, %s)"
    dados = (str(linha1),str(linha2),int(linha3),float(linha4), categoria)
    cursor.execute(comand_sql, dados)
    db.commit()
    formulario.line1.setText("")
    formulario.line2.setText("")
    formulario.line3.setText("")
    formulario.line4.setText("")

def chama_abrir_lista():
    abrir_lista.show()

    cursor = db.cursor()
    comand_sql = "SELECT * from EQUIPAMENTOS"
    cursor = db.cursor()
    cursor.execute(comand_sql)
    dados_lidos = cursor.fetchall()

    abrir_lista.tableWidget.setRowCount(len(dados_lidos))
    abrir_lista.tableWidget.setColumnCount(6)

    for i in range(0, len(dados_lidos)):
            for j in range(0,6):
             abrir_lista.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

app = QtWidgets.QApplication([])
formulario = uic.loadUi("formulario.ui")
abrir_lista = uic.loadUi("lista.ui")
tela_editar=uic.loadUi("edit.ui")
formulario.pushButton_1.clicked.connect(funcao_principal)
formulario.pushButton_2.clicked.connect(chama_abrir_lista)
abrir_lista.pushButton.clicked.connect(gerar_pdf)
abrir_lista.pushButton_2.clicked.connect(excluir_item)
abrir_lista.pushButton_3.clicked.connect(editar_item)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)

formulario.show()
app.exec()

