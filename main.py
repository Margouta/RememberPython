import tkinter as tk
import tkinter.messagebox as messagebox
import os
import yaml
import webbrowser
from datetime import date

ver = "0.1"

def afficher_matiere(matiere):
    folder_name = matiere.lower()
    folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Check if the folder exists, if not, create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Create the "Ancien" folder if it doesn't exist
    ancien_folder_path = os.path.join(folder_path, "ancien")
    if not os.path.exists(ancien_folder_path):
        os.makedirs(ancien_folder_path)
    
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    if len(files) == 1:
        file_path = os.path.join(folder_path, files[0])
        os.startfile(file_path)  # Open the file in the default file editor
    else:
        if len(files) == 0:
            result = messagebox.askquestion("Dossier vide", f"Le dossier {folder_name} est vide. Voulez-vous ouvrir le dossier ?")
            if result == 'yes':
                os.startfile(folder_path)
        else:
            # Ask if the folder should be opened
            result = messagebox.askquestion("Fichiers multiples", f"Le dossier {folder_name} contient plusieurs fichiers. Voulez-vous ouvrir le dossier ?")
            if result == 'yes':
                os.startfile(folder_path)
def ouvrir_dossier(matiere):
    folder_name = matiere.lower()
    folder_path = os.path.join(os.getcwd(), folder_name)
    os.startfile(folder_path)

def creer_interface():
    fenetre = tk.Tk()
    fenetre.title("Remember V"+ver)
    fenetre.resizable(False, False)  # Disable window resizing
    
    # Change the background color
    fenetre.configure(bg="lightgray")

    with open("config.yml", "r", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    images = {}  # Store PhotoImage objects

    # Add the logo image
    icon = tk.PhotoImage(file="icon.png")
    logo_image = tk.PhotoImage(file="ban.png")
    fenetre.iconphoto(True, icon)  # Set the window icon
    logo_label = tk.Label(fenetre, image=logo_image)
    logo_label.pack()  # Set the logo width to fill the window horizontally
    # Function to handle logo click event
    def logo_click():
        result = messagebox.askquestion("À propos", f"Remember V{ver} by little Aywen rewrited in Python by Margouta. Souaithez-vous ouvrir la configuration ?")
        if result == 'yes':
            config = os.path.join(os.getcwd(), "config.yml")
            os.startfile(config)

    # Bind the logo click event to the logo label
    logo_label.bind("<Button-1>", lambda event: logo_click())

    # Add the date label
    today = date.today()
    date_label = tk.Label(fenetre, text="Nous sommes le " + today.strftime("%d/%m/%Y"), bg="lightgray")
    date_label.pack()

    for matiere, image_path in config.items():
        bouton = tk.Button(fenetre, text=matiere.capitalize(), command=lambda matiere=matiere: afficher_matiere(matiere), width=200)
        bouton.pack()

        image = tk.PhotoImage(file="icons/"+image_path)
        image = image.subsample(int(image.height()/32))
        bouton.config(image=image, compound=tk.LEFT)

        # Change the button color
        bouton.config(bg="gray", fg="white")

        images[matiere] = image  # Store PhotoImage object

        # Add context menu for right-click
        context_menu = tk.Menu(fenetre, tearoff=0)
        context_menu.add_command(label="Déplacer vers Ancien", command=lambda matiere=matiere: deplacer_vers_ancien(matiere))
        context_menu.add_command(label="Ouvrir le dossier", command=lambda matiere=matiere: ouvrir_dossier(matiere))
        bouton.bind("<Button-3>", lambda event, context_menu=context_menu: context_menu.post(event.x_root, event.y_root))

    fenetre.bind("<KeyPress>", lambda event: check_easter_egg(event, fenetre))
    fenetre.mainloop()

def check_easter_egg(event, fenetre):
    sequence = "haut haut bas bas gauche droite gauche droite"
    keys = ["Up", "Up", "Down", "Down", "Left", "Right", "Left", "Right"]
    current_sequence = getattr(fenetre, "easter_egg_sequence", [])
    current_sequence.append(event.keysym)
    if current_sequence[-len(sequence):] == keys:
        fenetre.easter_egg_sequence = []
        video_path = "https://glor.cc/bestmusiceasteregg"
        webbrowser.open(video_path)
        messagebox.showinfo("Easter Egg", "Vous avez trouvé l'easter egg ! C'est parti pour la musique !!!")
    else:
        fenetre.easter_egg_sequence = current_sequence[-len(sequence):]

def deplacer_vers_ancien(matiere):
    folder_name = matiere.lower()
    folder_path = os.path.join(os.getcwd(), folder_name)
    ancien_folder_path = os.path.join(folder_path, "ancien")
    
    files = [file for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    
    if len(files) == 0:
        messagebox.showerror("Erreur", f"Le dossier {matiere} est vide.")
        return
    
    for file in files:
        file_path = os.path.join(folder_path, file)
        new_file_path = os.path.join(ancien_folder_path, file)
        os.rename(file_path, new_file_path)

    messagebox.showinfo("Déplacement terminé", f"Les fichiers de la matière {matiere} ont été déplacés vers le dossier 'ancien'.")

creer_interface()