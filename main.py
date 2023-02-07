from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import customtkinter
import math
import sqlite3
#import datetime
from datetime import datetime,date
import pygame

banco=sqlite3.connect('barber.db', check_same_thread=False)
cursor=banco.cursor()
#cursor.execute("CREATE TABLE horarios_concluidos(nome text,barbeiro text,trabalho text,hora text,data text)")
data_atual=date.today()
data= data_atual.strftime("%d/%m/%Y")




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
    dados=cursor.execute(f"""SELECT nome,barbeiro,trabalho,hora FROM horarios WHERE data LIKE '%{data}%'""").fetchall()
    for h in dados:
        tree_agenda_hoje.insert("","end",values=h)


def agenda_geral():            ################## PREENCHE A AGENDA GERAL
    tree_agenda_geral.delete(*tree_agenda_geral.get_children())
    dados=cursor.execute(f"""SELECT * FROM horarios""")
    for h in dados:
        tree_agenda_geral.insert("","end",values=h)


def realizados_hoje():
    tree_agenda_hoje.delete(*tree_agenda_hoje.get_children())
    tree_realizados_hoje.delete(*tree_realizados_hoje.get_children())
    dado=cursor.execute(f"""SELECT * FROM horarios_concluidos WHERE data LIKE '%{data}%'""").fetchall()
    for r in dado:
        tree_realizados_hoje.insert("","end",values=r)


def pesquisa():
    tree_agenda_geral.delete(*tree_agenda_geral.get_children())
    buscar=busca.get()
    results=cursor.execute(f"""SELECT * FROM horarios WHERE nome LIKE '%{buscar}%'""").fetchall()
    for b in results:
        tree_agenda_geral.insert("","end",values=b)



def concluido():    #### FUNÇÃO DO BOTAO CONCLUIDO DO FRAME_UM,DELETA DO BD E DELETA DO TREE VIEW
    off()
    concluido=tree_agenda_hoje.selection()[0]
    selecionado=tree_agenda_hoje.item(concluido,'values')
    del_nome=selecionado[0]
    del_barbeiro=selecionado[1]
    del_trabalho=selecionado[2]
    del_hora=selecionado[3]
    
    
    cursor.execute(f"""INSERT INTO horarios_concluidos VALUES('{del_nome}','{del_barbeiro}','{del_trabalho}','{del_hora}','{data}')""")
    banco.commit()


    cursor.execute(f"""DELETE FROM horarios WHERE  nome=('{del_nome}') AND barbeiro=('{del_barbeiro}') AND trabalho=('{del_trabalho}') AND hora=('{del_hora}')""")
    banco.commit()
    tree_agenda_hoje.delete(concluido)
    agenda_geral()
    realizados_hoje()
    quant()

def salvar():     #### SALVA O NOVO HORARIO NO BANCO DE DADOS
    nome_save=nome.get()
    barber_save=barber.get()
    trabalho_save=trabalho.get()
    hour_save=hour.get()
    day_save=day.get()
    disponivel=cursor.execute(f"""SELECT * FROM horarios WHERE barbeiro=('{barber_save}') AND hora=('{hour_save}') AND data=('{day_save}')""").fetchall()
    if nome_save=="" or barber_save=="" or trabalho_save=="" or hour_save=="" or day_save=="":
        messagebox.showerror(title="Erro",message="Um ou mais campos estão vazios!")
    
    #disponivel=cursor.execute(f"""SELECT * FROM horarios WHERE barbeiro=('{barber_save}') AND hora=('{hour_save}') AND data=('{day_save}')""").fetchall()
    
    elif len(disponivel)>=1:
        messagebox.showerror(title="Indisponivel",message=f"O barbeiro {barber_save} ja tem horario marcado dia {day_save} as {hour_save}")

    else:
        cursor.execute(f"""INSERT INTO horarios VALUES('{nome_save}','{barber_save}','{trabalho_save}','{hour_save}','{day_save}')""")
        banco.commit()

        nome.delete(0,"end")
        barber.delete(0,"end")
        hour.delete(0,"end")
        day.delete(0,"end")

    agenda_geral()
    agendados_hoje()
    print("Hello")


def feito():
    nome=nome_dois.get()
    barber=barber_dois.get()
    hora=hour_dois.get()
    job=trabalho_dois.get()
    cursor.execute(f"""INSERT INTO horarios_concluidos VALUES('{nome}','{barber}','{job}','{hora}','{data}')""")
    banco.commit()
    agenda_geral()
    agendados_hoje()
    off()
    quant()

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
    off()


app= Tk()

lista=("Cabelo","Barba")   ######## lista de trabalhos disponivel

height=app.winfo_screenheight()   ##IDENTIFICA O TAMANHO DA TELA##
width=app.winfo_screenwidth()    
width_four=math.floor(width/5)
width_five=math.floor(width/6.25)

                #########################################################################



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
title_hoje=customtkinter.CTkLabel(frame_um,text="Trabalhos de hoje",font=("Arial",18),fg_color="#32CD32",corner_radius=10)
title_hoje.place(x=730,y=10,width=200)

style=ttk.Style()
style.configure("Treeview",background="white")
style.map("Treeview",background=[("selected","gray")])

tree_agenda_hoje=ttk.Treeview(frame_um,columns=('Nome','Barbeiro','Trabalho','Hora'),show="headings")
tree_agenda_hoje.column('Nome',minwidth=0,width=width_four)
tree_agenda_hoje.column('Barbeiro',minwidth=0,width=width_four)
tree_agenda_hoje.column('Trabalho',minwidth=0,width=width_four)
tree_agenda_hoje.column('Hora',minwidth=0,width=width_four)
tree_agenda_hoje.heading("Nome",text="Nome")
tree_agenda_hoje.heading("Barbeiro",text="Barbeiro")
tree_agenda_hoje.heading("Trabalho",text="Trabalho")
tree_agenda_hoje.heading("Hora",text="Hora")
tree_agenda_hoje.place(x=20,y=70)
agendados_hoje()

concluido=customtkinter.CTkButton(frame_um,text='Concluido',text_color="White",fg_color="Blue",command=concluido)
concluido.place(x=width-350,y=75)

cancelar=customtkinter.CTkButton(frame_um,text="Cancelar",text_color="White",fg_color="Blue")
cancelar.place(x=width-350,y=125)





################################## AGENDA GERAL ##################################################
title_geral=customtkinter.CTkLabel(frame_um,text="Trabalhos Gerais",font=("Arial",18),fg_color="#00BFFF",corner_radius=10)
title_geral.place(x=730,y=360,width=200)

tree_agenda_geral=ttk.Treeview(frame_um,columns=('Nome','Barbeiro','Trabalho','Hora','Data'),show="headings")
tree_agenda_geral.column('Nome',minwidth=0,width=width_five)
tree_agenda_geral.column('Barbeiro',minwidth=0,width=width_five)
tree_agenda_geral.column('Trabalho',minwidth=0,width=width_five)
tree_agenda_geral.column('Hora',minwidth=0,width=width_five)
tree_agenda_geral.column('Data',minwidth=0,width=width_five)
tree_agenda_geral.heading("Nome",text="Nome")
tree_agenda_geral.heading("Barbeiro",text="Barbeiro")
tree_agenda_geral.heading("Trabalho",text="Trabalho")
tree_agenda_geral.heading("Hora",text="Hora")
tree_agenda_geral.heading("Data",text="Data")
tree_agenda_geral.place(x=20,y=400,height=500)
agenda_geral()


busca=customtkinter.CTkEntry(frame_um,placeholder_text="Busca")
busca.place(x=width-350,y=400)
busca_button=customtkinter.CTkButton(frame_um,text="Buscar",fg_color="Blue",command=pesquisa)
busca_button.place(x=width-200,y=400,width=60)




geral_desmarcar=customtkinter.CTkButton(frame_um,text="Desmarcar",text_color="White",fg_color="Blue",command=desmarcar)
geral_desmarcar.place(x=width-350,y=500)





def off():
    #dia=datetime.now()
    hour_dois.delete(0,999)
    atual = datetime.now()
    dia = atual.strftime("%H:%M")  
    hour_dois.insert(0,f"{dia}")
    realizados_hoje()


#################################### NOVO ######################

def quant():    #### ALTERA A QUANTIDADE DE TRABALHO REALIZADOS NO DIA
    quant=cursor.execute(f"""SELECT * FROM horarios_concluidos WHERE data=('{data}')""").fetchall()
    v=len(quant)
    trabalho_hoje_q['text']=v

############## AGENDAMENTO ################

agendamento=LabelFrame(frame_dois,borderwidth=5,relief='sunken',background="gray")
agendamento.place(x=10,y=10,width=400,height=800)

nome_tittle=customtkinter.CTkLabel(agendamento,text="Nome:")
nome_tittle.place(x=100,y=8)
nome=customtkinter.CTkEntry(agendamento,placeholder_text="Nome do Cliente")
nome.place(x=100,y=30)

barber=customtkinter.CTkEntry(agendamento,placeholder_text="Barbeiro")
barber.place(x=100,y=60)

hour=customtkinter.CTkEntry(agendamento,placeholder_text="Hora:")
hour.place(x=100,y=90)

day_button=customtkinter.CTkButton(agendamento,text="📅",font=("Arial",20),fg_color="transparent",command=calendar)
day_button.place(x=250,y=118,width=50)
day=customtkinter.CTkEntry(agendamento,placeholder_text="Dia/Mes/Ano:")
day.place(x=100,y=120)

trabalho=customtkinter.CTkComboBox(agendamento,values=lista,button_hover_color="#32CD32",dropdown_hover_color="#D3D3D3")
trabalho.place(x=100,y=150)


button_agendar=customtkinter.CTkButton(frame_dois,text="Agendar",command=salvar)
button_agendar.place(x=110,y=300)


################ REALIZADO #############

realizado=LabelFrame(frame_dois,borderwidth=5,relief="sunken",background="gray")
realizado.place(x=600,y=10,width=400,height=800)


nome_dois=customtkinter.CTkEntry(realizado,placeholder_text="Nome")
nome_dois.place(x=100,y=30)

barber_dois=customtkinter.CTkEntry(realizado,placeholder_text="Barbeiro")
barber_dois.place(x=100,y=60)

hour_dois=customtkinter.CTkEntry(realizado,placeholder_text="Barbeiro")
hour_dois.place(x=100,y=90)

trabalho_dois=customtkinter.CTkComboBox(realizado,values=lista,button_hover_color="#32CD32",dropdown_hover_color="#D3D3D3")
trabalho_dois.place(x=100,y=120)


agendar_chegada=customtkinter.CTkButton(realizado,text="Feito",command=feito)
agendar_chegada.place(x=110,y=300)



######################### REALIZADOS HOJE ############################

quantos_hoje=LabelFrame(frame_tres,borderwidth=5, relief='sunken')
quantos_hoje.place(x=10,y=10,width=300,height=100)

trabalho_hoje=customtkinter.CTkLabel(quantos_hoje,text="Quantidade de traballhos hoje:",font=("Arial",20))
trabalho_hoje.place(x=10,y=20)

#trabalho_hoje_q=customtkinter.CTkLabel(quantos_hoje,text="34",font=("arial",20))
trabalho_hoje_q=Label(quantos_hoje,text="34",font=("arial",20))
trabalho_hoje_q.place(x=10,y=50)


tree_realizados_hoje=ttk.Treeview(frame_tres,columns=('Nome','Barbeiro','Trabalho','Hora','Data'),show="headings")
tree_realizados_hoje.column('Nome',minwidth=0,width=width_five)
tree_realizados_hoje.column('Barbeiro',minwidth=0,width=width_five)
tree_realizados_hoje.column('Trabalho',minwidth=0,width=width_five)
tree_realizados_hoje.column('Data',minwidth=0,width=width_five)
tree_realizados_hoje.column('Hora',minwidth=0,width=width_five)
tree_realizados_hoje.heading("Nome",text="Nome")
tree_realizados_hoje.heading("Barbeiro",text="Barbeiro")
tree_realizados_hoje.heading("Trabalho",text="Trabalho")
tree_realizados_hoje.heading("Data",text="Data")
tree_realizados_hoje.heading("Hora",text="Hora")
tree_realizados_hoje.place(x=20,y=300,height=500)

realizados_hoje()

off()
quant()
agenda_geral()
agendados_hoje()



app.mainloop()