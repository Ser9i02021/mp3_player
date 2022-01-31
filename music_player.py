import pygame
from pygame import mixer
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import tkinter as tk
import os
from random import randint
from tkinter.filedialog import asksaveasfile
import pickle

root = Tk()
root.title("Project0")
root.geometry("850x350")


#Criar Playlist Box
song_box = Listbox(root, bg = "black", fg = "green", font = ('arial',15), width = 80,
                   selectbackground = "gray", selectforeground = "yellow")
song_box.pack(pady = 20)
os.chdir(r'D:\Users\UsuarioDirectD\Music\Songs')


class Playlist():
    def __init__(self, title_playlist):
        self.title_playlist = title_playlist
        
    
    def text_display_playlist(self):
        l2 = Label(root, text = self.title_playlist, font = ("Arial", 15), bg = "gray", fg = "black")
        l2.place(x = 1, y = 0, height = 20, width = 60)
        
        
        
    def adicionar_faixa(self):
        self.songs = filedialog.askopenfilenames(initialdir = r'D:\Users\UsuarioDirectD\Music\Songs',
                                      title = "Escolher músicas")
        for song in self.songs:
            song_box.insert(END, song[36:])
    
    def remover_faixa(self):
        song_box.delete(ANCHOR)
        mixer.music.stop()
    
    def limpar_playlist(self):
        song_box.delete(0, END)
        mixer.music.stop()
        
    def salvar_playlist(self):
        file_name = filedialog.asksaveasfilename(
            initialdir = r'D:\Users\UsuarioDirectD\Music\Playlists',
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
        
        title_playlist = file_name[40:-4]
        
        Playlist(title_playlist).text_display_playlist()
            

    
        
class NovaPlaylist(Playlist):
    def __init__(self, nome):
        self.nome = nome
        
    def adicionar_faixas(self):
        plist.limpar_playlist()
        self.songs = filedialog.askopenfilenames(initialdir = r'D:\Users\UsuarioDirectD\Music\Songs',
                                      title = "Escolher músicas")
        for song in self.songs:
            song_box.insert(END, song[36:])
    
        
        
class AbrirPlaylist(Playlist):
    def __init__(self, nome):
        self.nome = nome
        
    def selecionar_playlist(self):
        file_name = filedialog.askopenfilename(
            initialdir = r'D:\Users\UsuarioDirectD\Music\Playlists',
            title = "Abrir playlist",
            filetypes = (("mp3 file", "*.mp3"), ("All files", "*.*")))
        
        if file_name:
            song_box.delete(0, END)
            
            input_file = open(file_name, "rb")
            
            all_tracks = pickle.load(input_file)
            
            for song in all_tracks:
                song_box.insert(END, song)
                
        title_playlist = file_name[40:-4]
        Playlist(title_playlist).text_display_playlist()
        
        
class RemoverPlaylist(Playlist):
    def __init__(self, nome):
        self.nome = nome

    def remover_playlist(self):
        plist.text_display_playlist()  
        plist.limpar_playlist()
 
 
 
 
 
 
 
class Busca():
        
    def buscar_faixa(self):
        pass
    
    def buscar_playlist(self):
        pass

    
plist = Playlist("playlist0")

nplist = NovaPlaylist("ok")

aplist = AbrirPlaylist("ok")

rplist = RemoverPlaylist("ok")

bsc = Busca()


#Criar Menu
my_menu = Menu(root)
root.config(menu = my_menu)



#Criar Menu de Playlist
add_playlist_menu = Menu(my_menu)
my_menu.add_cascade(label = "Playlist", menu = add_playlist_menu)
add_playlist_menu.add_command(label = "Nova playlist", command = nplist.adicionar_faixas)
add_playlist_menu.add_command(label = "Abrir playlist", command = aplist.selecionar_playlist)
add_playlist_menu.add_command(label = "Salvar playlist", command = nplist.salvar_playlist)


#Criar Menu de Músicas
add_playlist_menu = Menu(my_menu)
my_menu.add_cascade(label = "Adicionar faixa", menu = add_playlist_menu)
add_playlist_menu.add_command(label = "Nova faixa", command = plist.adicionar_faixa)    


#Deletar Menu de Músicas
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Remover faixa", menu = remove_song_menu)
remove_song_menu.add_command(label = "Excluir faixa", command = plist.remover_faixa) 
remove_song_menu.add_command(label = "Limpar playlist", command = plist.limpar_playlist) 


#Barra de Pesquisa
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Procurar", menu = add_song_menu)
add_song_menu.add_command(label = "Buscar faixa", command = bsc.buscar_faixa)
add_song_menu.add_command(label = "Buscar playlist", command = bsc.buscar_playlist)





class Player():
    def __init__(self, musica_atual, q):
        self.musica_atual = musica_atual
        self.q = q
    
    def play(self):
        if self.q == 0:
            self.musica_atual = song_box.get(ACTIVE)
        
        
        self.lb = Label(root, text = str(self.musica_atual), font = ("arial", 15), bg = "dark blue", fg = "white")
        self.lb.place(x = 2, y = 190, width = 900, height = 50)
            
                
        mixer.music.load(self.musica_atual)
        songstatus.set("Playing")
        mixer.music.play()
        self.q = 0


    def pause(self):
        songstatus.set("Paused")
        mixer.music.pause()

    def stop(self):
        songstatus.set("Stopped")
        mixer.music.stop()

    def resume(self):
        songstatus.set("Resuming")
        mixer.music.unpause()
        
    def loop_faixa(self):
        pass
            
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




plyr = Player(song_box.get(0), 0)


#Imagens dos Botões
back_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\back-btn.png'))
forward_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\forward-btn.png'))
play_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\play-btn.png'))
resume_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\resume-btn.png'))
pause_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\pause-btn.png'))
stop_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\stop-btn.png'))
loop_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\loop-btn.png'))
shuffle_btn_img = (Image.open(r'D:\Users\UsuarioDirectD\Downloads\next\shuffle-btn.png'))

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
