#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import ImageTk, Image
from datetime import datetime
from tempfile import NamedTemporaryFile
import os
import preproc
import cv2
import csv
import shutil

# config['camera_dir'] = diretório das imagens da camera - definido e mantido na abertura da primeira imagem
# config['output_dir'] = diretório de arquivamento (principal, do banco) - definido e verificado no inicio
# config['csv'] = nome do arquivo csv, com caminho completo
# config['id'] = id selecionado
# config['entry_id'] = Entry do id na interface
# config['list_id'] = ttk.Listbox do id na interface
# config['list_id_values'] = lista dos ids
# config['entry_idade'] = ttk.Entry da idade na interface
# config['combo_grupo'] = ttk.Combobox do grupo na interface
# config['obs'] = ScrolledText da observacao na interface
# config['img'] = PhotoImage da interrogação na interface
# config['hands'] = PhotoImage das mãos na interface
# pre['individuo'] = dicionário contendo indexado pelo id e associando a uma lista [ id, idade, grupo ]
# pre['ids'] = conjunto dos ids que estão em pre['individuo']
# pre['idades'] = conjunto das idade que estão em pre['individuo']
# pre['grupos'] = conjunto dos grupos que estão em pre['individuo']
# data['file' + str(number)] = nome da imagem com caminho completo
# data['preproc' + str(number)] = imagem saída pré-processada img_preproc_cv2 
# data['output_day_dir'] = diretório de arquivamento do dia, com caminho completo
# data['output_dir'] = diretório da instancia, com caminho completo
# data['csv'] = nome do arquivo csv da instancia, com caminho completo

      
def atualizar_csv(individuo):
    global config
    global pre
    if( os.path.isfile( config['csv'] ) ):
        try:
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            
            with open(config['csv'], 'r', newline='', encoding='utf-8') as csvfile, tempfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer = csv.writer(tempfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                line_count = 0
                for row in reader:
                    if line_count == 0:
                        colunas = ['id', 'idade', 'grupo'];
                        if( colunas != row ):
                            messagebox.showerror(title='Erro',
                                                 message='O banco de imagens do local indicado está inconsistente.\n')
                            return False
                    else:
                        if len(row) == 3:
                            if row[0] == individuo[0] :
                                row[1] = individuo[1]
                                row[2] = individuo[2]
                                pre['individuo'][row[0]] = row
                            if row[0] not in pre['individuo'] or row != pre['individuo'][row[0]]:
                                messagebox.showerror(title='Erro',
                                                     message='O banco de imagens do local indicado está inconsistente.\n')
                                return False                                
                    writer.writerow(row)                            
                    line_count = line_count + 1
                csvfile.close()
                tempfile.close()
            shutil.move(tempfile.name, config['csv'])
        except:
            messagebox.showerror(title='Erro',
                                 message='Não foi possível atualizar!\n')
            
            return False
        
        copiar_pre_interface()
        return True
    return False
    
def adicionar_csv(individuo):
    global config
    global pre
    if( os.path.isfile( config['csv'] ) ):
        try:
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            
            with open(config['csv'], 'r', newline='', encoding='utf-8') as csvfile, tempfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer = csv.writer(tempfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                line_count = 0
                for row in reader:
                    if line_count == 0:
                        colunas = ['id', 'idade', 'grupo'];
                        if( colunas != row ):
                            messagebox.showerror(title='Erro',
                                                 message='O banco de imagens do local indicado está inconsistente.\n')
                            return False
                    else:
                        if len(row) != 3 or row[0] not in pre['individuo'] or row != pre['individuo'][row[0]]:
                            messagebox.showerror(title='Erro',
                                                 message='O banco de imagens do local indicado está inconsistente.\n')
                            return False
                    writer.writerow(row)                            
                    line_count = line_count + 1
                if individuo[0] in pre['individuo']:
                    messagebox.showerror(title='Erro',
                        message='Não há o que atualizar!\n')
                    return False
                pre['individuo'][individuo[0]] = individuo
                writer.writerow(individuo)
                csvfile.close()
                tempfile.close()
            shutil.move(tempfile.name, config['csv'])
        except:
            messagebox.showerror(title='Erro',
                                 message='Não foi possível atualizar!\n')
            
            return False
        
        copiar_pre_interface()
        return True
    return False 

def copiar_pre_interface():
    global config
    global pre

    ids = []
    grupos = []
    for i in pre['individuo']:
        individuo = pre['individuo'][i]
        ids.append(individuo[0])
        grupos.append(individuo[2])

    config['list_id_values'] = ids
    update(ids)
    config['combo_grupo']['values'] = grupos
   
    
def arquivar_definitivo(individuo):
    global config
    global data

    # criar pasta
    # mover todas as imagens
    
    dia = datetime.now().strftime("%j - %d-%m-%Y")    
    data['output_day_dir'] = os.path.join(config['output_dir'], dia)
    # diferença entre exists e isdir ?????????????????????????
    if not os.path.exists(data['output_day_dir']):
        try:
            os.makedirs(data['output_day_dir'])
        except:
            messagebox.showerror(title='Erro',
                                 message='Não foi possível criar a pasta do dia no banco de imagens.\n')
            return False    
    
    data['output_dir'] = os.path.join(data['output_day_dir'], individuo[0])
    
    if not os.path.exists(data['output_dir']):
        try:
            os.makedirs(data['output_dir'])
        except:
            messagebox.showerror(title='Erro',
                                 message='Não foi possível criar a pasta do ID no dia do banco de imagens.\n')
            return False    
    else:
            messagebox.showerror(title='Erro',
                                 message='ID já existe hoje. Imagens não arquivadas!\n')
            return False

    if not os.path.exists(data['output_dir']) or not len(os.listdir(data['output_dir'])) == 0:
        messagebox.showerror(title='Erro',
                             message='ID já existe hoje. Imagens não arquivadas!\n')
        return False

    data['csv'] = os.path.join(data['output_dir'],'data.txt')
    
    if not os.path.isfile( data['csv'] ):
        criar_texto_instancia(individuo)
    else:
        messagebox.showerror(title='Erro',
                             message='Não foi possível salvar texto com dados. Pasta não vazia?\n')
        return False
    
    # mover

    for x in range(10):
        dst_original = os.path.join(data['output_dir'], 'original - ' +
                                    individuo[0] + ' - ' + dia + 
                                    ' - ' + str(x) + '.png')
        try:
            shutil.copy(data['file' + str(x+1)], dst_original)
        except:
            messagebox.showerror(title='Erro',
                                 message='Não foi possível mover a imagem X.\n')
            return False        
            
        dst_preproc =os.path.join(data['output_dir'], 'preproc-' +
                                    individuo[0] + ' - ' + dia + 
                                    ' - ' + str(x) + '.png')
        try:
            cv2.imwrite(dst_preproc, data['preproc' + str(x+1)])
        except:
            messagebox.showerror(title='Erro',
                                 message='Não foi possível salvar a imagem X.\n')
            return False

    messagebox.showinfo(title='Sucesso!',
                        message='Imagens arquivadas com sucesso!\n')
    return True
    
def criar_texto_instancia(individuo):
    global config
    global data

    # salvar num arquivo texto ['id','idade', 'grupo', 'data', 'obs']
    with open(data['csv'], 'w') as file:
        file.write(datetime.now().strftime("%d/%m/%Y, %H:%M:%S") +'\n')
        file.write(individuo[0] +'\n')
        file.write(individuo[1] +'\n')
        file.write(individuo[2] +'\n')
        file.write(config['obs'].get("1.0", tk.END) +'\n')        
        file.close()
    return

def criar_csv():
    global config

    with open(config['csv'], 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter= csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['id','idade', 'grupo'])
        csvwriter.close()
    
def archieve( ):
    global config
    global data
    global pre
    
    count = 0
    for x in range(10):
        if 'file' + str(x+1) in data:
            count += 1
    count = 10 # -------------------------------------------------------------------------------------------------------
    if count == 10:
        config['id'] = config['entry_id'].get()
        individuo = [ config['id'], config['entry_idade'].get(), config['combo_grupo'].get() ]
        if( individuo[0] in pre['individuo'] ):
            busca = pre['individuo'][individuo[0]]
            if( busca == individuo ):
                print('arquivar')
                arquivar_definitivo(individuo)
            else:
                answer = messagebox.askyesno(title='Importante',
                                    message='Houve alteração nos dados deste ID. Atualizar?')
                if (answer):
                    print('atualizar e arquivar')
                    atualizar_csv(individuo)
                    arquivar_definitivo(individuo)
        else:
            answer = messagebox.askyesno(title='Importante',
                                message='Incluir novo ID?')
            if (answer):
                print('adicionar id e arquivar')
                adicionar_csv(individuo)
                arquivar_definitivo(individuo)
    else:
        messagebox.showerror(title='Erro', message='Preencha todos os dedos!')

def create_form( container ):
    global config
    
    frame = ttk.Frame(container)
   
    label1 = ttk.Label(frame, text='ID:')
    label1.grid(column=0, row=0, sticky=tk.W)
    config['entry_id'] = ttk.Entry(frame, width=20, validate="key", validatecommand=(root.register(checkID), '%P'))
    config['entry_id'].grid(column=1, row=0, sticky=tk.W)
    config['entry_id'].bind('<KeyRelease>', checkkey)
    config['list_id'] = tk.Listbox(frame, width=20, height=6)
    config['list_id'].grid(column=1, row=1, sticky=tk.W, rowspan=2)
    config['list_id'].bind('<<ListboxSelect>>', selectedid)   
    label0 = ttk.Label(frame, text='', width=5 )
    label0.grid(column=2, row=0, sticky=tk.W)
    
    label2 = ttk.Label(frame, text='Idade:')
    label2.grid(column=3, row=0, sticky=tk.W)
    config['entry_idade'] = ttk.Entry(frame, width=20)
    config['entry_idade'].grid(column=4, row=0, sticky=tk.W)
    
    label3 = ttk.Label(frame, text='Grupo:')
    label3.grid(column=3, row=1, sticky=tk.W)
    config['combo_grupo'] = ttk.Combobox(frame, width=20)
    config['combo_grupo'].grid(column=4, row=1, sticky=tk.W)
    
    label4 = ttk.Label(frame, text='Obs.:')
    label4.grid(column=3, row=2, sticky=tk.W)
    config['obs'] = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=4)
    config['obs'].grid(column=4, row=2, sticky=tk.W, columnspan=2)
    
    label00 = ttk.Label(frame, text='', width=5 )
    label00.grid(column=7, row=0, sticky=tk.W)
    
    button1 = ttk.Button(frame, text='Arquivar', command=archieve)
    button1.grid(column=8, row=2, sticky=tk.E)
    
    return frame
    
def load_csv():
    global config
    global pre
   
    if( os.path.isfile( config['csv'] ) ):
        with open(config['csv'], 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            line_count = 0
            for row in csvreader:
                if line_count == 0:
                    colunas = ['id', 'idade', 'grupo'];
                    if( colunas != row ):
                        messagebox.showerror(title='Erro',
                                             message='O banco de imagens do local indicado está inconsistente.\n')
                        return False
                else:
                    if(len(row) == 3 and row[0] not in pre['individuo']  ):
                        pre['individuo'][row[0]] = row
                    else:
                        return False
                line_count += 1
            return True
  
    return False

def define_output( container ):
    global config
    global data    
    
    while True:
        diretorio = filedialog.askdirectory(parent=container,
                                            title='Selecione onde serão arquivadas as imagens',
                                            initialdir=config['output_dir'] )    
        if( diretorio != () and os.path.isdir(diretorio) ):
            config['csv'] = os.path.join(config['output_dir'],'data.csv')
            if( not os.path.isfile( config['csv'] ) ):
                answer = messagebox.askyesno(title='Importante',
                                    message='Não foi encontrado um banco de imagens existente.\nDeseja criar um novo?')
                if (not answer):
                    return False
                
                criar_csv()
                
            if ( not load_csv() ):                                
                messagebox.showerror(title='Erro',
                                     message='O banco de imagens do local indicado está inconsistente.\n')
                return False    
            
            copiar_pre_interface()
            config['output_dir'] = diretorio
            return True
      

def load_image( widget, number, event ):
    global config
    global data
    
    file = filedialog.askopenfilename(parent=widget, title='Selecione uma imagem',
                                      initialdir=config['camera_dir'],
                                      filetypes=(('Image files','*.jpg'),('All files', '*.*') ) )
    
    if( file != () and os.path.isfile(file) ):
        
        try:
            config['camera_dir'] = os.path.abspath(os.path.dirname(file))
            
            img_preproc_cv2 = preproc.preproc( cv2.imread(file) )
            img_preproc_cv2_rgb = cv2.cvtColor(img_preproc_cv2, cv2.COLOR_BGR2RGB)
            img_preproc = Image.fromarray(img_preproc_cv2_rgb)
            img = ImageTk.PhotoImage(img_preproc.resize((150,150)))
            
            data['file' + str(number)] = file
            data['preproc' + str(number)] = img_preproc_cv2
            
            widget.configure(image=img)
            widget.image = img
            widget.update()
            
        except:
            if 'file' + str(number) in data:
                del data['file' + str(number)]
            if 'preproc' + str(number) in data:
                del data['preproc' + str(number)]
            
            widget.configure(image=config['img'])
            widget.update()
            
            messagebox.showerror(title='Erro', message='Não foi possível identificar!')

def resize_image(image, width, height):
    new_image = image.resize((width, height))
    return new_image                                
    
    
def create_images( container ):
    global config
    global data
    
    frame = ttk.Frame(container)
    
    config['hands'] = ImageTk.PhotoImage(file='hands3.png')
    label = ttk.Label(frame, image=config['hands'])
    label.pack()
    
    config['img'] = ImageTk.PhotoImage(file='img2.png')

    label1 = ttk.Label(frame, image=config['img'])
    label1.place(x=0, y=220)
    label1.bind( "<Button>", lambda event: load_image(label1, 1, event) )

    label2 = ttk.Label(frame, image=config['img'])
    label2.place(x=50, y=110)
    label2.bind( "<Button>", lambda event: load_image(label2, 2, event) )

    label3 = ttk.Label(frame, image=config['img'])
    label3.place(x=100, y=0)
    label3.bind( "<Button>", lambda event: load_image(label3, 3, event) )

    label4 = ttk.Label(frame, image=config['img'])
    label4.place(x=210, y=0)
    label4.bind( "<Button>", lambda event: load_image(label4, 4, event) )

    label5 = ttk.Label(frame, image=config['img'])
    label5.place(x=300, y=110)
    label5.bind( "<Button>", lambda event: load_image(label5, 5, event) )
   
    label6 = ttk.Label(frame, image=config['img'])
    label6.place(x=400, y=110)
    label6.bind( "<Button>", lambda event: load_image(label6, 6, event) )

    label7 = ttk.Label(frame, image=config['img'])
    label7.place(x=490, y=0)
    label7.bind( "<Button>", lambda event: load_image(label7, 7, event) )

    label8 = ttk.Label(frame, image=config['img'])
    label8.place(x=600, y=0)
    label8.bind( "<Button>", lambda event: load_image(label8, 8, event) )

    label9 = ttk.Label(frame, image=config['img'])
    label9.place(x=650, y=110)
    label9.bind( "<Button>", lambda event: load_image(label9, 9, event) )

    label10 = ttk.Label(frame, image=config['img'])
    label10.place(x=700, y=220)
    label10.bind( "<Button>", lambda event: load_image(label10, 10, event) )
       
    return frame


def create_window( container ):
    
    frame = ttk.Frame(container)
  
    frame1 = create_images(frame)
    frame1.grid(column=0, row=0, sticky=tk.W)

    frame2 = create_form(frame)
    frame2.grid(column=0, row=1, sticky=tk.W)
   
    
    return frame
   
def checkkey(event):       
    value = event.widget.get()
    if value == '':
        data = config['list_id_values']
    else:
        data = []
        for item in config['list_id_values']:
            if value.lower() in item.lower():
                data.append(item)                
    update(data)
   
def update(data):
    config['list_id'].delete(0, 'end')
    for item in data:
        config['list_id'].insert('end', item)

def selectedid(event):
    i = config['list_id'].curselection()
    if ( len(i) == 1 and i[0] >= 0 and i[0] < config['list_id'].size() ):
        config['id'] = config['list_id'].get(i)
        
        individuo =  pre['individuo'][config['id']]

        if( len(individuo) == 3):
            config['entry_id'].delete(0, tk.END)
            config['entry_id'].insert(0, individuo[0] )
            config['entry_idade'].delete(0, tk.END)
            config['entry_idade'].insert(0, individuo[1] )
            config['combo_grupo'].set(individuo[2])
        else:
            messagebox.showerror(title='Erro', message='Interface inconsistente!')

def checkID(input):
    if len(input) == 0:
        return True
    elif input.isalnum():
        return True                        
    else:
        return False

# Inicio

data = {}
pre = {}
pre['individuo'] = { }
pre['ids'] = set()
pre['idades'] = set()
pre['grupos'] = set()
config = {'camera_dir' : os.getcwd(),
          'output_dir' : os.getcwd()  }

root = tk.Tk()
root.title('Projeto Esmalte')
root.geometry('1000x700')
root.resizable(False, False)

frame = create_window(root)
frame.pack(expand=1)

define_output( frame )


# start the app
root.mainloop()
