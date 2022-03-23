# mp3_player

from random import randint
import pygame
from pygame import mixer
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import pickle
import os
import time
from mutagen.mp3 import MP3



root = Tk()
root.title("Project0")
root.geometry("850x450")


#Criar Playlist Box
song_box = Listbox(root, bg = "black", fg = "green", font = ('arial',15), width = 80,
                   selectbackground = "gray", selectforeground = "yellow")
song_box.pack(pady = 20)
os.chdir('/home/sergio/Music')

Titles = []

T_playlist = []

class Playlist():
    def __init__(self, nome):
        self.nome = nome
        Titles.append(self.nome)
       
    
    def display_titulo_playlist(self):
        self.l = Label(root, text = self.nome, font = ("Arial", 15), bg = "gray", fg = "black")
        self.l.place(x = 1, y = 0, height = 20, width = 847)
        
    def adicionar_faixa(self):
        self.songs = filedialog.askopenfilenames(initialdir = '/home/sergio/Music',
                                      title = "Escolher músicas")
        for song in self.songs:
            song_box.insert(END, song[19:])
    
    def excluir_faixa(self):
        song_box.delete(ANCHOR)
        mixer.music.stop()
    
    def limpar_playlist(self):
        song_box.delete(0, END)
        mixer.music.stop()
    




class SalvarPlaylist(Playlist):
    def __init__(self, nome):
        super().__init__(nome)
    
    def salvar_playlist(self):
        file_name = filedialog.asksaveasfilename(
            initialdir = '/home/sergio/Music/Playlists',
            title = "Salvar playlist",
            filetypes = (("mp3 file", "*.mp3"), ("All files", "*.*")))
        
        if file_name:
            if file_name.endswith(".mp3"):
                pass
            else:
                file_name = f'{file_name}.mp3'
                
        all_tracks = song_box.get(0, END)
        
        output_file = open(file_name, "wb")
        
        pickle.dump(all_tracks, output_file)
        
        title_playlist = file_name[29:-4]
        
        T_playlist.append(title_playlist)
        
        SalvarPlaylist(title_playlist).display_titulo_playlist()
        
        
class NovaPlaylist(Playlist):
    def __init__(self, nome):
        super().__init__(nome)
        
    def nova_playlist(self):
        nplist.display_titulo_playlist()
        nplist.limpar_playlist()
        nplist.adicionar_faixa()
        
        
class AbrirPlaylist(Playlist):
    def __init__(self, nome):
        super().__init__(nome)
        
    def selecionar_playlist(self):
        file_name = filedialog.askopenfilename(
            initialdir = '/home/sergio/Music/Playlists',
            title = "Abrir playlist",
            filetypes = (("mp3 file", "*.mp3"), ("All files", "*.*")))
        
        if file_name:
            song_box.delete(0, END)
            
            input_file = open(file_name, "rb")
            
            all_tracks = pickle.load(input_file)
            
            for song in all_tracks:
                song_box.insert(END, song)
                
        title_playlist = file_name[29:-4]
        T_playlist.append(title_playlist)
        AbrirPlaylist(title_playlist).display_titulo_playlist()
          
        
class RemoverPlaylist(Playlist):
    def __init__(self, nome):
        super().__init__(nome)

    def aviso_destruicao(self):
        self.j_a = Toplevel(root)
        self.j_a.title("Deletar playlist")
        self.j_a.geometry("300x200")
        Label(self.j_a, text = """Tem certeza que deseja deletar "{}"
permanentemente?""".format(T_playlist[-1])).pack()
        Button(self.j_a, text = "Deletar", command = lambda: eplist.deletar_playlist()).place(x = 130, y = 50) 
        Button(self.j_a, text = "Cancelar", command = lambda: self.j_a.destroy()).place(x = 40, y = 50) 

    def deletar_playlist(self):
        if os.path.exists('/home/sergio/Music/Playlists/{}.mp3'.format(Titles[-1])):
            os.remove('/home/sergio/Music/Playlists/{}.mp3'.format(Titles[-1]))
            self.j_a.destroy()
        
        
        eplist.display_titulo_playlist()
        eplist.limpar_playlist()
    
 
 

class Busca():
        
    def buscar_faixa(self):
        self.barra_busca = Label(root, text = "Pesquisar faixa dentro da playlist", bg = "light blue")
        self.barra_busca.place(x = 590, y = 0)
        bsc_str = StringVar(root, "")
        self.aba_busca = Entry(root, textvariable = bsc_str)
        self.aba_busca.place(x = 590, y = 22)
        self.bsc_btn = Button(root, text = "Procurar", command = lambda: bsc.selecionar_faixa())
        self.bsc_btn.place(x = 760, y = 22)
        
    def selecionar_faixa(self):
        msc_bsc = self.aba_busca.get()
        self.barra_busca.destroy()
        self.aba_busca.destroy()
        self.bsc_btn.destroy()
        for i in range(len(song_box.get(0, END))):
            if msc_bsc in song_box.get(i):
                song_box.selection_set(i)



    
plist = Playlist("")

nplist = NovaPlaylist("")

aplist = AbrirPlaylist("")

splist = SalvarPlaylist("") 

eplist = RemoverPlaylist("")

bsc = Busca()


#Criar Menu
my_menu = Menu(root)
root.config(menu = my_menu)



#Criar Menu de Playlist
add_playlist_menu = Menu(my_menu)
my_menu.add_cascade(label = "Playlist", menu = add_playlist_menu)
add_playlist_menu.add_command(label = "Nova playlist", command = nplist.nova_playlist)
add_playlist_menu.add_command(label = "Abrir playlist", command = aplist.selecionar_playlist)
add_playlist_menu.add_command(label = "Salvar playlist", command = splist.salvar_playlist)
add_playlist_menu.add_command(label = "Excluir playlist", command = eplist.aviso_destruicao)


#Criar Menu de Músicas
add_playlist_menu = Menu(my_menu)
my_menu.add_cascade(label = "Adicionar", menu = add_playlist_menu)
add_playlist_menu.add_command(label = "Nova faixa", command = plist.adicionar_faixa)    


#Deletar Menu de Músicas
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Remover", menu = remove_song_menu)
remove_song_menu.add_command(label = "Excluir faixa", command = plist.excluir_faixa) 
remove_song_menu.add_command(label = "Limpar playlist", command = plist.limpar_playlist) 


#Barra de Pesquisa
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Procurar", menu = add_song_menu)
add_song_menu.add_command(label = "Buscar faixa", command = bsc.buscar_faixa)
   

d = [1]
class Player():
    def __init__(self, musica_atual, q):
        self.musica_atual = musica_atual
        self.q = q
    
    def play(self):
        if self.q == 0:
            self.musica_atual = song_box.get(ACTIVE)
        
        
        self.lb = Label(root, text = str(self.musica_atual), font = ("arial", 15), bg = "dark blue", fg = "white")
        self.lb.place(x = 2, y = 190, width = 855, height = 50)
            
                
        mixer.music.load(self.musica_atual)
        songstatus.set("Playing")
        mixer.music.play()
        self.q = 0
        tempo_atual[0] = 0
        if len(tempo_atual) == 2:
            tempo_atual.pop(-1)
        if song_status[0] == 1:
            d[0] += 1
        TimeSlide().play_time()
        


    def pause(self):
        songstatus.set("Paused")
        mixer.music.pause()
        tempo_atual.append(0)
        TimeSlide().play_time()

    def stop(self):
        songstatus.set("Stopped")
        mixer.music.stop()
        tempo_atual.append(1)
        TimeSlide().play_time()

    def resume(self):
        songstatus.set("Resuming")
        mixer.music.unpause()
        tempo_atual.pop(-1)
        TimeSlide().play_time()
        
        
    def loop_faixa(self):
        if l_s[0] == 0:
            l_s[0] = 1
            loop_status.config(text = "ON")
        else:
            l_s[0] = 0
            loop_status.config(text = "OFF")
            
    def shuffle(self):
        self.random_track_index = randint(0, song_box.size() - 1)
        self.musica_atual = song_box.get(self.random_track_index)
        song_box.selection_clear(0, END)
        song_box.activate(self.random_track_index)
        song_box.selection_set(self.random_track_index)
        self.q += 1
        Player(self.musica_atual, self.q).play()
    
    
    
    def faixa_seguinte(self):
        for i in range(song_box.size()):
            if self.musica_atual == song_box.get(i):
                print(song_box.get(i))
                IndexNS = i + 1
                if IndexNS > song_box.size() - 1:
                    IndexNS = 0
                break
                
        self.musica_atual = song_box.get(IndexNS)
        song_box.selection_clear(0, END)
        song_box.activate(IndexNS)
        song_box.selection_set(IndexNS)
        self.q += 1
        Player(self.musica_atual, self.q).play()
        

        
    def faixa_anterior(self):
        for i in range(song_box.size()):
            if self.musica_atual == song_box.get(i):
                print(song_box.get(i))
                IndexNS = i - 1
                if IndexNS < 0:
                    IndexNS = song_box.size() - 1
                break
                
        self.musica_atual = song_box.get(IndexNS)
        song_box.selection_clear(0, END)
        song_box.activate(IndexNS)
        song_box.selection_set(IndexNS)
        self.q += 1
        Player(self.musica_atual, self.q).play()
        

    
mixer.init()
songstatus=StringVar()
songstatus.set("choosing")

c_l = []
tempo_atual = [0]
song_status = [0]
l_s = [0]


class TimeSlide():
    
    def play_time(self):
        song = song_box.get(ACTIVE)
        song = f'/home/sergio/Music/{song}'
        song_mut = MP3(song)
        comp_song = song_mut.info.length
        
        tempo_form = time.strftime("%M:%S", time.gmtime(tempo_atual[0]))
        comp_song_conv = time.strftime("%M:%S", time.gmtime(comp_song))
        c_l.append(comp_song_conv)
        if tempo_form == comp_song_conv:
            tempo_atual.append(1)
        
        slider_label.config(text = tempo_form + " de " + comp_song_conv)
        my_slider.config(from_ = 0, to = comp_song, value = tempo_atual[0])
        
        #update
        if len(tempo_atual) == 1:
            tempo_atual[0] += 1
            song_status[0] = 1
            slider_label.after(int(1000 * d[0]), TimeSlide().play_time)
        else:
            song_status[0] = 0
            d[0] = 1
            if tempo_atual[-1] == 1:
                tempo_atual[0] = 0
                slider_label.config(text = "00:00 de " + comp_song_conv)
                my_slider.config(from_ = 0, to = comp_song, value = tempo_atual[0])
                if l_s[0] == 1:
                    plyr.play()



    def slide(self, x):
        t_f = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        if c_l:
            slider_label.config(text = t_f + " de " + c_l[-1])
        
            mixer.music.set_pos(my_slider.get())
            tempo_atual[0] = int(my_slider.get())

          
        else:
            slider_label.config(text = t_f + " de 01:40")



#Slider
my_slider = ttk.Scale(root, from_ = 0, to = 100, orient = HORIZONTAL, length = 600, value = 0, command = TimeSlide().slide)
my_slider.pack()

#Slider Label
slider_label = Label(root, text = "00:00 de 00:00")
slider_label.pack()

plyr = Player(song_box.get(0), 0)


#Imagens dos Botões
back_btn_img = (Image.open('/home/sergio/Pictures/back-btn.png'))
forward_btn_img = (Image.open('/home/sergio/Pictures/forward-btn.png'))
play_btn_img = (Image.open('/home/sergio/Pictures/play-btn.png'))
resume_btn_img = (Image.open('/home/sergio/Pictures/resume-btn.png'))
pause_btn_img = (Image.open('/home/sergio/Pictures/pause-btn.png'))
stop_btn_img = (Image.open('/home/sergio/Pictures/stop-btn.png'))
loop_btn_img = (Image.open('/home/sergio/Pictures/loop-btn.png'))
shuffle_btn_img = (Image.open('/home/sergio/Pictures/shuffle-btn.png'))

#Imagens com tamanhos ajustados
resized_image = back_btn_img.resize((70,70), Image.ANTIALIAS)
back_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = forward_btn_img.resize((70,70), Image.ANTIALIAS)
forward_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = play_btn_img.resize((70,70), Image.ANTIALIAS)
play_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = resume_btn_img.resize((70,70), Image.ANTIALIAS)
resume_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = pause_btn_img.resize((70,70), Image.ANTIALIAS)
pause_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = stop_btn_img.resize((70,70), Image.ANTIALIAS)
stop_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = loop_btn_img.resize((70,70), Image.ANTIALIAS)
loop_btn_img = ImageTk.PhotoImage(resized_image)
resized_image = shuffle_btn_img.resize((70,70), Image.ANTIALIAS)
shuffle_btn_img = ImageTk.PhotoImage(resized_image)

#Frame de controle do Player 
controls_frame = Frame(root)
controls_frame.pack()


loop_status = Label(root, text = "OFF", bg = "white")
loop_status.place(x = 605, y = 360) 
#Controles dos Botões
back_btn = Button(controls_frame, image = back_btn_img, borderwidth = 2, command = plyr.faixa_anterior)
forward_btn = Button(controls_frame, image = forward_btn_img, borderwidth = 2, command = plyr.faixa_seguinte)
play_btn = Button(controls_frame, image = play_btn_img, borderwidth = 2, command = plyr.play)
resume_btn = Button(controls_frame, image = resume_btn_img, borderwidth = 2, command = plyr.resume)
pause_btn = Button(controls_frame, image = pause_btn_img, borderwidth = 2, command = plyr.pause)
stop_btn = Button(controls_frame, image = stop_btn_img, borderwidth = 2, command = plyr.stop)
loop_btn = Button(controls_frame, image = loop_btn_img, borderwidth = 2, command = plyr.loop_faixa)
shuffle_btn = Button(controls_frame, image = shuffle_btn_img, borderwidth = 2, command = plyr.shuffle)

#Display dos Botões
back_btn.grid(row = 0, column = 0)
forward_btn.grid(row = 0, column = 1)
play_btn.grid(row = 0, column = 2)
resume_btn.grid(row = 0, column = 3)
pause_btn.grid(row = 0, column = 4)
stop_btn.grid(row = 0, column = 5)
loop_btn.grid(row = 0, column = 6)
shuffle_btn.grid(row = 0, column = 7)
    

    
    

root.mainloop()
