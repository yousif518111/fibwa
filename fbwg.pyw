import pygame
from sys import exit
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import win32gui
import win32con
import time
import keyboard
import configparser
import os
import shutil

# Initialize Pygame and variables
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
play_music = True

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
BUTTON_WIDTH = 350
BUTTON_HEIGHT = 50
BUTTON_EXPAND_WIDTH = 370
BUTTON_HEIGHT_EXPAND = 60
BUTTON_GAP = 20
BG_COLOR = "#101010"  # Dark background color

# Load sounds
pygame.mixer.set_num_channels(2)
btnhover = pygame.mixer.Sound("sounds/btnhover.wav")
bgmusic = pygame.mixer.Sound("sounds/bgmusic.wav")
btnpress=pygame.mixer.Sound("sounds/btnpress.wav")

#----Config File----#
config = configparser.ConfigParser()
config.read('config.ini')
music = config.getboolean('Settings', 'music')
framerate = config.getint('Settings', 'framerate')

if music:
    bgmusic.play(-1)

bg_image = pygame.image.load('bg.png')
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

idk=False
settings_icon = pygame.image.load('Ui/settings.png')
settings_icon = pygame.transform.scale(settings_icon, (100, 100))
settings_icon_rect = settings_icon.get_rect(topleft=(715, 0))


music_on_image = pygame.image.load('Ui/music_on.png')
music_off_image = pygame.image.load('Ui/music_off.png')


MUSIC_BUTTON_SIZE = (50, 50)
music_on_image = pygame.transform.scale(music_on_image, MUSIC_BUTTON_SIZE)
music_off_image = pygame.transform.scale(music_off_image, MUSIC_BUTTON_SIZE)

# Set initial music button image
music_button_image = music_on_image if music else music_off_image
music_button_rect = music_button_image.get_rect(topleft=(670, 25))

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Fireboy and Watergirl')

# Button class
class Button:
    def __init__(self, text, y, command, color, hover_color):
        self.text = text
        self.y = y
        self.rect = pygame.Rect(-10, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font('fonts/solemnit.ttf', 36)
        self.expanded = False
        self.command = command
        self.hovered = False
        
    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
            if not self.hovered:
                pygame.mixer.Channel(1).play(btnhover)
                self.hovered = True
        else:
            color = self.color
            self.hovered = False
        
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(midright=self.rect.midright)
        screen.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.expanded = True
            self.rect.width = BUTTON_EXPAND_WIDTH
            self.rect.height = BUTTON_HEIGHT_EXPAND
            if pygame.mouse.get_pressed()[0]:
                self.command()
        else:
            self.expanded = False
            self.rect.width = BUTTON_WIDTH
            self.rect.height = BUTTON_HEIGHT



#------------Settings Start------------#
def settings():
    config = configparser.ConfigParser()
    config.read('config.ini')
    #----Window----#
    root1= tk.Tk()
    root1.title("Settings")
    root1.geometry("300x220")
    root1.resizable(False, False)

    #----tabs----#
    notebook = ttk.Notebook(root1)
    tab1= ttk.Frame(notebook)
    notebook.add(tab1, text="General")
    tab2= ttk.Frame(notebook)
    tab3= ttk.Frame(notebook)
    notebook.add(tab2, text="Reset")
    notebook.add(tab3, text="Info")
    notebook.pack(expand=1, fill='both')

    #----Fonts----#
    title_font= ("fonts/bruce4ever", 30, "bold")
    error_font=("comic sans", 10)
    entry1_font=("comic sans", 8)
    #---entry---#
    framerate_label=tk.Label(tab1,text="Change framerate", font=error_font, fg="black")
    framerate_label.place(x=0, y=0)
    def on_entry_click(event):
       if entry1.get() == "5-120":
          entry1.delete(0, tk.END)
          entry1.configure(foreground="black")

    def on_focus_out(event):
       if entry1.get() == "":
          entry1.insert(0, "5-120")
          entry1.configure(foreground="#ececec")

    def framerate_change():
        error_fps1=tk.Label(tab1,text="ⓘInvalid input: not an integer", font=error_font, fg="dark red")
        error_fps2=tk.Label(tab1,text="ⓘFramerate must be between 5 and 120", font=error_font, fg="dark red")
        try:
            framerate1 = int(entry1.get())
            if 5 <= framerate1 <= 120:
                config.set('Settings', 'framerate', str(framerate1))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                print(f"Framerate set to {framerate1}")
            else:
                error_fps2.place(x=5, y=10)
                root1.after(5000, error_fps2.destroy)
        except ValueError:
            error_fps1.place(x=3, y=0)
            root1.after(5000, error_fps1.destroy)
        restart_ask=messagebox.askyesno("Restart Required", "A restart is required to complete this action\nRestart Now?")
        if restart_ask==None or False:
            return
        elif restart_ask:
            subprocess.Popen(["Restart.exe"])
            exit()
            
        
    entry1 = tk.Entry(tab1,relief="sunken",justify="left", width=10, fg="#ebecbc")
    entry1.insert(0, "5-120")
    entry1.place(x=10,y=30)
    entry1.bind("<FocusIn>", on_entry_click)
    entry1.bind("<FocusOut>", on_focus_out)
    submit_btn=tk.Button(tab1,font=entry1_font,text = 'Change', command = framerate_change,height=1)
    submit_btn.place(x=15,y=50)

    #----Combobox----#
    combo_values =["Choose an item",
        "Fireboy and Watergirl 1: the Forest Temple", 
        "Fireboy and Watergirl 2: In the Light Temple", 
        "Fireboy and Watergirl 3: In the Ice Temple", 
        "Fireboy and Watergirl 4: In the Crystal Temple",
        "All Games"]

    combo = ttk.Combobox(tab2, state="readonly",values=combo_values, width=40)
    combo.place(x=25,y=60)
    combo.current(0)

    reset_success=tk.Label(root1, font=error_font, text= "ⓘ Reset Succesful!", fg="green")
    error1=tk.Label(root1, font=error_font, text= "ⓘ Uh Oh, Something went wrong", fg="Dark red")
    

    #----Info----#
    info_label=tk.Label(tab3, text="Created by u/kingofstupidness (reddit)\nOr yousif518111 (github)\nContact me at yousif51811@gmail.com\n\nYou may use this program under the circumstance\nthat this page with credits on it stays in the\nprogram with all it's original aspects\n\nVersion: 0.1.0\n\n©Oslo Albert\n Creator of the Fireboy and Watergirl series")
    info_label.pack()

    #----combo commands----#
    def btn_press():
        error2=tk.Label(root1, font=error_font, text= "ⓘ Please choose a game!", fg="Dark red")
        response=messagebox.askyesno("Confirm Reset", "Are you sure you would like to do this? \nyour data will be lost forever.")
        combo_selected = combo.get()
        if combo_selected == "Choose an item":
            error2.place(x=25, y=55)
            root1.after(5000, error2.destroy)
            return
        if response == None or response == False:
            return
        elif response:
            if combo_selected == "Fireboy and Watergirl 1: the Forest Temple":
                reset_fbwg1()
            elif combo_selected == "Fireboy and Watergirl 2: In the Light Temple":
                reset_fbwg2()
            elif combo_selected == "Fireboy and Watergirl 3: In the Ice Temple":
                reset_fbwg3()
            elif combo_selected == "Fireboy and Watergirl 4: In the Crystal Temple":
                reset_fbwg4()   
            elif combo_selected == "All Games":
                reset_all()
            else:
                error1.place(x=25, y=55)
                root1.after(5000, error1.destroy)

    def reset_all():
        try:
            reset_success=tk.Label(tab2, font=error_font, text= "ⓘ Reset Succesful!", fg="green")
            os.remove("swf/1.swf")
            os.remove("swf/2.swf")
            os.remove("swf/3.swf")
            os.remove("swf/4.swf")
            time.sleep(2)
            shutil.copy("swf/reset/1.swf", "swf/")
            shutil.copy("swf/reset/2.swf", "swf/")
            shutil.copy("swf/reset/3.swf", "swf/")
            shutil.copy("swf/reset/4.swf", "swf/")
            reset_success.place(x=25, y=35)
            root1.after(5000, reset_success.destroy)
        except FileNotFoundError:
            shutil.copy("swf/reset/1.swf", "swf/")
            shutil.copy("swf/reset/2.swf", "swf/")
            shutil.copy("swf/reset/3.swf", "swf/")
            shutil.copy("swf/reset/4.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        if not FileNotFoundError:
            error1.place(x=25, y=35)
            root1.after(5000, error1.destroy)
        
    def reset_fbwg1(): 
        try:
            reset_success=tk.Label(tab2, font=error_font, text= "ⓘ Reset Succesful!", fg="green")
            os.remove("swf/1.swf")
            time.sleep(1)
            shutil.copy("swf/reset/1.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        except FileNotFoundError:
            shutil.copy("swf/reset/1.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        if not FileNotFoundError:
            error1.place(x=25, y=35)
            root1.after(5000, error1.destroy)

    def reset_fbwg2(): 
        try:
            reset_success=tk.Label(tab2, font=error_font, text= "ⓘ Reset Succesful!", fg="green")
            os.remove("swf/2.swf")
            time.sleep(1)
            shutil.copy("swf/reset/2.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        except FileNotFoundError:
            shutil.copy("swf/reset/2.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        if not FileNotFoundError:
            error1.place(x=25, y=35)
            root1.after(5000, error1.destroy)

    def reset_fbwg3(): 
        try:
            reset_success=tk.Label(tab2, font=error_font, text= "ⓘ Reset Succesful!", fg="green")
            os.remove("swf/3.swf")
            time.sleep(1)
            shutil.copy("swf/reset/3.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        except FileNotFoundError:
            shutil.copy("swf/reset/3.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        if not FileNotFoundError:
            error1.place(x=25, y=35)
            root1.after(5000, error1.destroy)

    def reset_fbwg4():
        try:
            reset_success=tk.Label(tab1, font=error_font, text= "ⓘ Reset Succesful!", fg="green")
            os.remove("swf/4.swf")
            time.sleep(1)
            shutil.copy("swf/reset/4.swf", "swf/")
            reset_success.place(x=25, y =35)
            root.after(5000, reset_success.destroy)
        except FileNotFoundError:
            shutil.copy("swf/reset/4.swf", "swf/")
            reset_success.place(x=25, y =35)
            root1.after(5000, reset_success.destroy)
        if not FileNotFoundError:
            error1.place(x=25, y=35)
            root1.after(5000, error1.destroy)
    reset_all_btn= tk.Button(tab2, text="Reset progress", command=btn_press)
    reset_all_btn.place(x=110, y=110)
    reset_text=tk.Label(tab2, text="Please choose a game that you would \nlike to reset")
    reset_text.pack()

    root1.mainloop()
#------------Settings End------------#


#------------Close start------------#
def close_x():
    class TransparentWindow:
        def __init__(self, master):
            self.master = master
            self.master.attributes('-transparentcolor', 'white')
            self.master.overrideredirect(True)
            self.master.geometry('-20+20')
            self.master.lift()
            self.master.wm_attributes('-topmost', True)
            self.master.wm_attributes('-transparentcolor', 'white')

        # Load transparent PNG button image and scale it down
            image = Image.open('Ui/x.png')
            image = image.resize((60, 60), Image.LANCZOS)  # Adjust the size as needed
            photo = ImageTk.PhotoImage(image)

            # Create and position the button in the top-right corner without margin
            self.close_button = tk.Button(self.master, image=photo, command=self.close_window, activebackground="#f44336", bd=0, highlightthickness=0, relief="flat")
            self.close_button.image = photo  # Keep a reference to the image
            self.close_button.pack(side='top', anchor='ne', padx=0, pady=0)  # Place it at the top-right corner without margin

        def close_window(self):
            os.system("taskkill /f /im fp.exe")
            self.master.destroy()

    if __name__ == "__main__":
        root = tk.Tk()
        app = TransparentWindow(root)
        root.mainloop()
#------------Close end------------#
def launch_fp1():
    process = subprocess.Popen(["fp.exe", "swf/1.swf"])
    time.sleep(0.3)
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    return process
def launch_fp2():
    process = subprocess.Popen(["fp.exe", "swf/2.swf"])
    time.sleep(0.3)
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    return process
def launch_fp3():
    process = subprocess.Popen(["fp.exe", "swf/3.swf"])
    time.sleep(0.3) 
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    return process
def launch_fp4():
    process = subprocess.Popen(["fp.exe", "swf/4.swf"])
    time.sleep(0.3) 
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    return process

# Define button commands
def command1():
    bgmusic.stop()
    btnpress.play(0)
    time.sleep(3)
    process = launch_fp1()
    keyboard.press_and_release('ctrl+f')
    close_x()
    bgmusic.stop()


def command2():
    bgmusic.stop()
    btnpress.play(0)
    time.sleep(3)
    process = launch_fp2()
    keyboard.press_and_release('ctrl+f')
    close_x()
    bgmusic.stop()

def command3():
    bgmusic.stop()
    btnpress.play(0)
    time.sleep(3)
    process = launch_fp3()
    keyboard.press_and_release('ctrl+f')
    close_x()
    bgmusic.stop()

def command4():
    bgmusic.stop()
    btnpress.play(0)
    time.sleep(3)
    process = launch_fp4()
    keyboard.press_and_release('ctrl+f')
    close_x()
    bgmusic.stop()

def command5():
    None

def command6():
    None

def toggle_music():
    global music_button_image, music
    music = not music
    config.set('Settings', 'music', str(music).lower())
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    music_button_image = music_on_image if music else music_off_image
    if music:
        bgmusic.play(-1)
    else:
        bgmusic.stop()

def open_settings():
    global music_button_image, music
    bgmusic.stop()
    music_button_image = music_off_image
    music = not music
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    settings()
# List of button texts, commands, colors, and hover colors
button_data = [
    ("The Forest Temple ", command1, (100, 200, 100), (150, 250, 150)),
    ("The Light Temple ", command2, (100, 100, 200), (150, 150, 250)),
    ("The Ice Temple ", command3, (200, 100, 100), (250, 150, 150)),
    ("The Crystal Temple ", command4, (200, 200, 100), (250, 250, 150)),
    ("Coming soon ", command5, (100, 200, 200), (150, 250, 250)),
    ("Coming soon ", command6, (200, 100, 200), (250, 150, 250)),
]

# Create buttons
buttons = []
for i, (text, command, color, hover_color) in enumerate(button_data):
    button = Button(text, 50 + i * (BUTTON_HEIGHT + BUTTON_GAP), command, color, hover_color)
    buttons.append(button)

# Main loop
while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if settings_icon_rect.collidepoint(mouse_pos):
                open_settings()
            if music_button_rect.collidepoint(mouse_pos):
                toggle_music()

    # Update buttons
    for button in buttons:
        button.update(mouse_pos)

    # Draw everything
    screen.blit(bg_image, (0, 0))
    for button in buttons:
        button.draw(screen)
    screen.blit(settings_icon, settings_icon_rect)
    screen.blit(music_button_image, music_button_rect)
    clock.tick(framerate)
    pygame.display.flip()
