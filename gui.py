#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:55:19 2023

@author: lizier
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import ImageTk, Image
import pickle
import os
import preproc
import cv2

global config

def load_config( ):
    global config
    if (os.path.isfile('gui.cfg')):
        with open('gui.cfg', 'rb') as f:
            config = pickle.load(f)

def save_config( ):
    global config
    with open('gui.cfg', 'wb') as f:
        pickle.dump(config,f)
        
def archieve( ):
    global config
    global data
    
    count = 0
    for x in range(10):
        if 'file' + str(x+1) in data:
            count += 1
    
    if count == 10:
        messagebox.showerror(title='Erro', message='EBA')
    else:
        messagebox.showerror(title='Erro', message='Preencha todos os dedos!')
        
    

def create_form( container ):
    
    frame = ttk.Frame(container)
   
    str1 = tk.StringVar()
    label1 = ttk.Label(frame, text='ID:')
    label1.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    combobox1 = ttk.Combobox(frame, state='readonly', width=22, textvariable = str1)
    combobox1.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
    combobox1['values'] = ('Maria', 'Antônia')
    combobox1.current(1) 
    
    str2 = tk.StringVar()
    label2 = ttk.Label(frame, text='Idade:')
    label2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    combobox2 = ttk.Combobox(frame, width=22, textvariable = str2)
    combobox2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
    combobox2['values'] = ('25', '30')
    combobox2.current(1) 
    
    str3 = tk.StringVar()
    label3 = ttk.Label(frame, text='Grupo:')
    label3.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
    combobox3 = ttk.Combobox(frame, width=22, textvariable = str3)
    combobox3.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)
    combobox3['values'] = ('Professora', 'Limpeza')
    combobox3.current(1) 
    

    label4 = ttk.Label(frame, text='Obs.:')
    label4.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
    text4 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=25, height=2,font=("Times New Roman", 10))
    text4.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)
    
    
    return frame

def define_output( ):
    global config
    global data
    
    diretorio = filedialog.askdirectory(parent=data['output_dir'],
                                        title='Selecione uma pasta',
                                        initialdir=config['output_dir'] )
    
    if( diretorio != () and os.path.isdir(diretorio) ):
        config['output_dir'] = diretorio
        data['output_dir'].config(state='normal')
        data['output_dir'].delete(0, tk.END)
        data['output_dir'].insert(0,config['output_dir'])
        data['output_dir'].config(state='readonly')
        save_config()        
      

def create_commands( container ):
    global config
    global data 
    
    frame = ttk.Frame(container)

    label1 = ttk.Label(frame, text='Arquivar em:')
    label1.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    entry1 = ttk.Entry(frame, width=50)
    entry1.insert(0,config['output_dir'])
    entry1.config(state='readonly')
    data['output_dir'] = entry1
    entry1.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)
    button1 = ttk.Button(frame, width=3, text='...', command=define_output )
    button1.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)

    label2 = ttk.Label(frame, text='Imagens em:')
    label2.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    entry2 = ttk.Entry(frame, width=50)
    entry2.insert(0,config['camera_dir'])
    entry2.config(state='readonly')
    data['camera_dir'] = entry2
    entry2.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)
    button2 = ttk.Button(frame, width=3, text='...', command=define_output )
    button2.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)

    label3 = ttk.Label(frame, text='')
    label3.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)
    button3 = ttk.Button(frame, text='Arquivar', command=archieve)
    button3.grid(column=3, row=4, sticky=tk.W, padx=5, pady=5)
            
    return frame

def load_image( widget, number, event ):
    global config
    global data
    
    file = filedialog.askopenfilename(parent=widget, title='Selecione uma imagem',
                                      initialdir=config['camera_dir'],
                                      filetypes=(('Image files','*.jpg'),('All files', '*.*') ) )
    
    if( file != () and os.path.isfile(file) ):
        
        try:
            config['camera_dir'] = os.path.abspath(os.path.dirname(file))
            save_config( )
            
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
            
            widget.configure(image=data['img'])
            widget.update()
            
            messagebox.showerror(title='Erro', message='Não foi possível identificar!')

def resize_image(image, width, height):
    new_image = image.resize((width, height))
    return new_image                                
    
    
def create_images( container ):
    global data
    
    frame = ttk.Frame(container)
    
    image = Image.open('hands2.png')
    resized_hands_image = resize_image(image, int(image.width * 0.55), int(image.height * 0.55))
    data['hands'] = ImageTk.PhotoImage(resized_hands_image)
    label = ttk.Label(frame, image=data['hands'])
    label.pack()
    
    image = Image.open('img.png')
    resized_img_image = resize_image(image, int(image.width * 0.45), int(image.height * 0.45))
    data['img'] = ImageTk.PhotoImage(resized_img_image)

    label1 = ttk.Label(frame, image=data['img'])
    label1.place(x=0, y=300*0.55)
    label1.bind( "<Button>", lambda event: load_image(label1, 1, event) )

    label2 = ttk.Label(frame, image=data['img'])
    label2.place(x=75*0.55, y=150*0.55)
    label2.bind( "<Button>", lambda event: load_image(label2, 2, event) )

    label3 = ttk.Label(frame, image=data['img'])
    label3.place(x=150*0.55, y=0)
    label3.bind( "<Button>", lambda event: load_image(label3, 3, event) )

    label4 = ttk.Label(frame, image=data['img'])
    label4.place(x=300*0.55, y=0)
    label4.bind( "<Button>", lambda event: load_image(label4, 4, event) )

    label5 = ttk.Label(frame, image=data['img'])
    label5.place(x=450*0.55, y=150*0.55)
    label5.bind( "<Button>", lambda event: load_image(label5, 5, event) )
   
    label6 = ttk.Label(frame, image=data['img'])
    label6.place(x=1050*0.55, y=300*0.55)
    label6.bind( "<Button>", lambda event: load_image(label6, 6, event) )

    label7 = ttk.Label(frame, image=data['img'])
    label7.place(x=975*0.55, y=150*0.55)
    label7.bind( "<Button>", lambda event: load_image(label7, 7, event) )

    label8 = ttk.Label(frame, image=data['img'])
    label8.place(x=900*0.55, y=0)
    label8.bind( "<Button>", lambda event: load_image(label8, 8, event) )

    label9 = ttk.Label(frame, image=data['img'])
    label9.place(x=750*0.55, y=0)
    label9.bind( "<Button>", lambda event: load_image(label9, 9, event) )

    label10 = ttk.Label(frame, image=data['img'])
    label10.place(x=600*0.55, y=150*0.55)
    label10.bind( "<Button>", lambda event: load_image(label10, 10, event) )
       
    return frame


def create_window( container ):
    
    frame = ttk.Frame(container)
  
    frame1 = create_images(frame)
    frame1.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10, columnspan = 2)

    frame2 = create_form(frame)
    frame2.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)
    
    frame3 = create_commands(frame)
    frame3.grid(column=1, row=1, sticky=tk.W, padx=10, pady=10)
    
    return frame
   


config = { 'camera_dir' : os.getcwd(), 'output_dir' : os.getcwd()  }
load_config( )

data = { }

# root window
root = tk.Tk()
root.title('Projeto Esmalte')
root.geometry('1240x1080')
root.resizable(True, True)

frame = create_window(root)
frame.pack(expand=1)

# start the app
root.mainloop()

save_config( )
