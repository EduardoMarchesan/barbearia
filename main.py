from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import customtkinter
import math
import sqlite3
import datetime
from time import sleep


banco=sqlite3.connect('barber.db', check_same_thread=False)
cursor=banco.cursor()
#cursor.execute("CREATE TABLE horarios(nome text,barbeiro text,trabalho text,hora text,data text)")
date_cap=datetime.date.today()
date=date_cap.strftime("%d/%m/%Y")



def calendar():      ########## FUNÇÃO QUE GERA O CALENDARIO
    day.delete(0,999)
    new_gui = Tk()
    new_gui.title("CALENDER")

 
    

    def data():
        data_day=calend.get_date()
        day.insert(END,data_day)
        new_gui.destroy()
    

 
    calend=Calendar(new_gui,locale="pt_br")
    calend.pack()

    butao=customtkinter.CTkButton(new_gui,text="Inserir",command=data)
    butao.pack()
    


def agendados_hoje():                ############### PREENCHE A AGENDA DE TRABALHOS DO DIA
    tree_agenda_hoje.delete(*tree_agenda_hoje.get_children())
    dados=cursor.execute(f"""SELECT nome,barbeiro,trabalho,hora FROM horarios WHERE data LIKE '%{date}%'""").fetchall()
    for h in dados:
        tree_agenda_hoje.insert("","end",values=h)


def agenda_geral():            ################## PREENCHE A AGENDA GERAL
    tree_agenda_geral.delete(*tree_agenda_geral.get_children())
    dados=cursor.execute(f"""SELECT * FROM horarios""")
    for h in dados:
        tree_agenda_geral.insert("","end",values=h)


def concluido():    #### FUNÇÃO DO BOTAO CONCLUIDO DO FRAME_UM,DELETA DO BD E DELETA DO TREE VIEW
    concluido=tree_agenda_hoje.selection()[0]
    selecionado=tree_agenda_hoje.item(concluido,'values')
    del_nome=selecionado[0]
    del_barbeiro=selecionado[1]
    del_trabalho=selecionado[2]
    del_hora=selecionado[3]
    cursor.execute(f"""DELETE FROM horarios WHERE  nome=('{del_nome}') AND barbeiro=('{del_barbeiro}') AND trabalho=('{del_trabalho}') AND hora=('{del_hora}')""")
    banco.commit()
    tree_agenda_hoje.delete(concluido)
    agenda_geral()


def salvar():     #### SALVA O NOVO HORARIO NO BANCO DE DADOS
    nome_save=nome.get()
    barber_save=barber.get()
    trabalho_save=trabalho.get()
    hour_save=hour.get()
    day_save=day.get()
    if nome_save=="" or barber_save=="" or trabalho_save=="" or hour_save=="" or day_save=="":
        messagebox.showerror(title="Erro",message="Um ou mais campos estão vazios!")
    cursor.execute(f"""INSERT INTO horarios VALUES('{nome_save}','{barber_save}','{trabalho_save}','{hour_save}','{day_save}')""")
    banco.commit()

    nome.delete(0,"end")
    barber.delete(0,"end")
    hour.delete(0,"end")
    day.delete(0,"end")
    trabalho.delete(0,"end")

    agenda_geral()
    agendados_hoje()

def desmarcar():
    desmarcado=tree_agenda_geral.selection()[0]
    select=tree_agenda_geral.item(desmarcado,"values")
    des_nome=select[0]
    des_barber=select[1]
    des_trabalho=select[2]
    des_hour=select[3]
    des_date=select[4]
    cursor.execute(f"""DELETE FROM horarios WHERE  nome=('{des_nome}') AND barbeiro=('{des_barber}') AND trabalho=('{des_trabalho}') AND hora=('{des_hour}') AND data=('{des_date}')""")
    banco.commit()
    tree_agenda_geral.delete(desmarcado)
    
    agenda_geral()
    agendados_hoje()



app= Tk()


height=app.winfo_screenheight()   ##IDENTIFICA O TAMANHO DA TELA
width=app.winfo_screenwidth()       ########
width_four=math.floor(width/5)
width_five=math.floor(width/6.25)



app.state("zoomed")


aba=ttk.Notebook(app,width=width-15,height=height-100)
aba.place(x=5,y=5)
######################
frame_um=customtkinter.CTkFrame(aba,fg_color="gray")
aba.add(frame_um,text="Geral")
#####################
frame_dois=customtkinter.CTkFrame(aba,fg_color="#708090")
aba.add(frame_dois,text="Agenda")
#################
frame_tres=customtkinter.CTkFrame(aba)
aba.add(frame_tres,text="Realizados-Hoje")

#################################### AGENDADOS - HOJE ######################
tree_agenda_hoje=ttk.Treeview(frame_um,columns=('Nome','Barbeiro','Trabalho','Hora'),show="headings")
tree_agenda_hoje.column('Nome',minwidth=0,width=width_four)
tree_agenda_hoje.column('Barbeiro',minwidth=0,width=width_four)
tree_agenda_hoje.column('Trabalho',minwidth=0,width=width_four)
tree_agenda_hoje.column('Hora',minwidth=0,width=width_four)
tree_agenda_hoje.heading("Nome",text="Nome")
tree_agenda_hoje.heading("Barbeiro",text="Barbeiro")
tree_agenda_hoje.heading("Trabalho",text="Trabalho")
tree_agenda_hoje.heading("Hora",text="Hora")
tree_agenda_hoje.place(x=20,y=20)
agendados_hoje()

concluido=customtkinter.CTkButton(frame_um,text='Concluido',text_color="White",fg_color="Blue",command=concluido)
concluido.place(x=width-350,y=20)

cancelar=customtkinter.CTkButton(frame_um,text="Cancelar",text_color="White",fg_color="Blue")
cancelar.place(x=width-350,y=70)





################################## AGENDA GERAL ##################################################
tree_agenda_geral=ttk.Treeview(frame_um,columns=('Nome','Barbeiro','Trabalho','Data','Hora'),show="headings")
tree_agenda_geral.column('Nome',minwidth=0,width=width_five)
tree_agenda_geral.column('Barbeiro',minwidth=0,width=width_five)
tree_agenda_geral.column('Trabalho',minwidth=0,width=width_five)
tree_agenda_geral.column('Data',minwidth=0,width=width_five)
tree_agenda_geral.column('Hora',minwidth=0,width=width_five)
tree_agenda_geral.heading("Nome",text="Nome")
tree_agenda_geral.heading("Barbeiro",text="Barbeiro")
tree_agenda_geral.heading("Trabalho",text="Trabalho")
tree_agenda_geral.heading("Data",text="Data")
tree_agenda_geral.heading("Hora",text="Hora")
tree_agenda_geral.place(x=20,y=300,height=500)
agenda_geral()


geral_desmarcar=customtkinter.CTkButton(frame_um,text="Desmarcar",text_color="White",fg_color="Blue",command=desmarcar)
geral_desmarcar.place(x=width-350,y=300)






#################################### NOVO ######################

nome_tittle=customtkinter.CTkLabel(frame_dois,text="Nome:")
nome_tittle.place(x=10,y=8)
nome=customtkinter.CTkEntry(frame_dois,placeholder_text="Nome do Cliente")
nome.place(x=10,y=30)

barber=customtkinter.CTkEntry(frame_dois,placeholder_text="Barbeiro")
barber.place(x=10,y=60)

hour=customtkinter.CTkEntry(frame_dois,placeholder_text="Hora:")
hour.place(x=10,y=90)

day_button=customtkinter.CTkButton(frame_dois,text="📅",font=("Arial",20),fg_color="transparent",command=calendar)
day_button.place(x=150,y=118,width=50)
day=customtkinter.CTkEntry(frame_dois,placeholder_text="Dia/Mes/Ano:")
day.place(x=10,y=120)
trabalho=customtkinter.CTkEntry(frame_dois,placeholder_text="Trabalho")
trabalho.place(x=10,y=150)





button_agendar=customtkinter.CTkButton(frame_dois,text="Agendar",command=salvar)
button_agendar.place(x=10,y=300)



#####################################################################





app.mainloop()