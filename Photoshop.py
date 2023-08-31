### Import des librairies

import tkinter as tk
import random
import numpy as np
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import filedialog
from tkinter import simpledialog

### Définition des fonctions pour afficher l'image en cours de traitement

def nbrCol(matrice):
    return(len(matrice[0]))

def nbrLig(matrice):
    return len(matrice)

def saving(matPix, filename):
    toSave=pil.Image.new("RGBA",(nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrCol(matPix)):
        for j in range(nbrLig(matPix)):
            toSave.putpixel((i,j),matPix[j][i])
    toSave.save(filename)
    
def loading(filename):
    toLoad=pil.Image.open(filename)
    mat=[[(255,255,255,255)]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]=toLoad.getpixel((j,i))
    return mat
  
create=True
nomImgCourante=""
nomImgDebut = ""

def charger(widg):
    global create
    global photo
    global img
    global canvas
    global dessin
    global nomImgCourante
    global nomImgDebut
    filename= filedialog.askopenfile(mode='rb', title='Choose a file')
    img = pil.Image.open(filename)
    nomImgCourante=filename.name
    nomImgDebut = filename.name
    photo = ImageTk.PhotoImage(img)
    if create:    
        canvas = tk.Canvas(widg, width = img.size[0], height = img.size[1])
        dessin = canvas.create_image(0,0,anchor = tk.NW, image=photo)
        canvas.grid(row=0,column=1,rowspan=4,columnspan=2)
        create=False
        
    else:
        canvas.grid_forget()
        canvas = tk.Canvas(widg, width = img.size[0], height = img.size[1])
        dessin=canvas.create_image(0,0,anchor = tk.NW, image=photo)
        canvas.grid(row=0,column=1,rowspan=4,columnspan=2)

def modify(matrice):
    global imgModif
    global nomImgCourante
    saving(matrice,"modif.png")
    imgModif=ImageTk.PhotoImage(file="modif.png")
    canvas.itemconfigure(dessin, image=imgModif)
    nomImgCourante="modif.png"

def reaffiche():
    global imgDebut
    global nomImgCourante
    if not create :
        imgDebut=ImageTk.PhotoImage(file=nomImgDebut)
        canvas.itemconfigure(dessin, image=imgDebut)
        nomImgCourante = nomImgDebut
        
### Définition des fonctions de modification de l'image
    
def filtre_vert():
    mat=loading(nomImgCourante)
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat[i][j]=(0,mat[i][j][1],0,255)
    modify(mat)
            
def negatif():
    mat=loading(nomImgCourante)
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat[i][j]=(255-mat[i][j][0],255-mat[i][j][1],255-mat[i][j][2],255)
    modify(mat)
            
def symetrique():
    mat=loading(nomImgCourante)
    matSym=[[(0,0,0,0)]*nbrCol(mat) for k in range(nbrLig(mat))]
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            matSym[i][nbrCol(mat)-1-j]=mat[i][j]
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat[i][j]=matSym[i][j]
    modify(mat)

def gris():
    #On utilise la conversion CIE709 qui permet de calculer la teinte de gris qui va être affichée dans le pixel
    #La teinte affichée est : gris=0,2125*rouge + 0,0721*bleu + 0,7154*vert
    mat=loading(nomImgCourante)
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            val_pixel = int((mat[i][j][0]*0.2125) + (mat[i][j][2]*7.21*10**(-2)) + (mat[i][j][1]*0.7154))
            mat[i][j] = (val_pixel, val_pixel, val_pixel, 255)
            
    modify(mat)

def noirBlanc():
    mat=loading(nomImgCourante)
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            luminosite = int((mat[i][j][0] + mat[i][j][1] + mat[i][j][2]) / 3)
            if luminosite > 127:
                mat[i][j] = (255, 255, 255, 255)
            else:
                mat[i][j]= (0, 0, 0, 255)
            # un pixel est blanc quand sa luminosité est > à 127, noir sinon
    modify(mat)

def zoom():
    mat=loading(nomImgCourante)
    #créer une matrice de largeur et hauteur deux fois plus grande
    mat_res = [[(0, 0, 0, 0)]*nbrCol(mat)*2 for i in range(2*nbrLig(mat))] 
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            for k in range(2):
                for l in range(2):
                    mat_res[i*2+k][j*2+l] = mat[i][j]

    modify(mat_res)

def shrink():
    mat=loading(nomImgCourante)
    #créer une matrice de largeur et hauteur deux fois plus petite
    nb_l = nbrLig(mat)
    nb_c = nbrCol(mat)

    mat_res = [[(0, 0, 0, 0)]* ((nb_c +1)//2)for i in range((nb_l+1)//2)]
    for i in range(nbrLig(mat_res)):
        for j in range(nbrCol(mat_res)):
            r = 0
            g = 0
            b = 0
            for k in range(2):
                if 2*i+k < nb_l:
                    for l in range(2):
                        if 2*j+l < nb_c:
                            r += mat[2*i+k][2*j+l][0]
                            g += mat[2*i+k][2*j+l][1]
                            b += mat[2*i+k][2*j+l][2]
            mat_res[i][j] = (r//4, g//4, b//4, 255)
    modify(mat_res)

def poster():
    shrink()
    zoom()

def rotate_gauche():
    mat=loading(nomImgCourante)
    col = nbrLig(mat)
    lig = nbrCol(mat)
    mat_res = [[(0, 0, 0, 0)]*nbrLig(mat) for i in range(nbrCol(mat))]
    for i in range(nbrLig(mat_res)):
        for j in range(nbrCol(mat_res)):
            mat_res[i][j]=mat[j][nbrCol(mat)-1-i]
    modify(mat_res)

def rotate_droite():
    mat=loading(nomImgCourante)
    mat_res = [[(0, 0, 0, 0)]*nbrLig(mat) for i in range(nbrCol(mat))]
    for i in range(nbrLig(mat_res)):
        for j in range(nbrCol(mat_res)):
            mat_res[i][j] = mat[nbrLig(mat)-1-j][i]
    modify(mat_res)

def flou():            # fonction non optimisée mais permet d'avoir un flou plus homogène que sa version mieux optimisée
    mat=loading(nomImgCourante)
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            if (0 < i < nbrLig(mat)-1) and (0 < j < nbrCol(mat)-1):
                rouge = int((mat[i][j][0] + mat[i][j-1][0] + mat[i][j+1][0] + mat[i-1][j-1][0] + mat[i-1][j][0] + mat[i-1][j+1][0] + mat[i+1][j-1][0] +mat[i+1][j][0] + mat[i+1][j+1][0]) /9)
                vert = int((mat[i][j][1] + mat[i][j-1][1] + mat[i][j+1][1] + mat[i-1][j-1][1] + mat[i-1][j][1] + mat[i-1][j+1][1] + mat[i+1][j-1][1] +mat[i+1][j][1] + mat[i+1][j+1][1]) /9)
                bleu = int((mat[i][j][2] + mat[i][j-1][2] + mat[i][j+1][2] + mat[i-1][j-1][2] + mat[i-1][j][2] + mat[i-1][j+1][2] + mat[i+1][j-1][2] +mat[i+1][j][2] + mat[i+1][j+1][2]) /9)
            elif (i==0) and (j==0):
                rouge = int((mat[i][j][0] + mat[i][j+1][0] + mat[i+1][j][0] + mat[i+1][j+1][0]) /4)
                vert = int((mat[i][j][1] + mat[i][j+1][1] + mat[i+1][j][1] + mat[i+1][j+1][1]) /4)
                bleu = int((mat[i][j][2] + mat[i][j+1][2] + mat[i+1][j][2] + mat[i+1][j+1][2]) /4)
            elif (i==0) and (j==nbrCol(mat)-1):
                rouge = int((mat[i][j][0] + mat[i][j-1][0] + mat[i+1][j][0] + mat[i+1][j-1][0]) /4)
                vert = int((mat[i][j][1] + mat[i][j-1][1] + mat[i+1][j][1] + mat[i+1][j-1][1]) /4)
                bleu = int((mat[i][j][2] + mat[i][j-1][2] + mat[i+1][j][2] + mat[i+1][j-1][2]) /4)
            elif (i==nbrLig(mat)-1) and (j==0):
                rouge = int((mat[i][j][0] + mat[i][j+1][0] + mat[i-1][j][0] + mat[i-1][j+1][0]) /4)
                vert = int((mat[i][j][1] + mat[i][j+1][1] + mat[i-1][j][1] + mat[i-1][j+1][1]) /4)
                bleu = int((mat[i][j][2] + mat[i][j+1][2] + mat[i-1][j][2] + mat[i-1][j+1][2]) /4)
            elif (i==nbrLig(mat)-1) and (j==nbrCol(mat)-1):
                rouge = int((mat[i][j][0] + mat[i][j-1][0] + mat[i-1][j][0] + mat[i-1][j-1][0]) /4)
                vert = int((mat[i][j][1] + mat[i][j-1][1] + mat[i-1][j][1] + mat[i-1][j-1][1]) /4)
                bleu = int((mat[i][j][2] + mat[i][j-1][2] + mat[i-1][j][2] + mat[i-1][j-1][2]) /4)
            elif (0 < i < (nbrLig(mat)-1)) and (j==0):
                rouge = int((mat[i][j][0] + mat[i+1][j][0] + mat[i+1][j+1][0] + mat[i][j+1][0] + mat[i-1][j][0] + mat[i-1][j+1][0]) /6)
                vert = int((mat[i][j][1] + mat[i+1][j][1] + mat[i+1][j+1][1] + mat[i][j+1][1] + mat[i-1][j][1] + mat[i-1][j+1][1]) /6)
                bleu = int((mat[i][j][2] + mat[i+1][j][2] + mat[i+1][j+1][2] + mat[i][j+1][2] + mat[i-1][j][2] + mat[i-1][j+1][2]) /6)
            elif (0 < i < (nbrLig(mat)-1)) and (j==nbrCol(mat)-1):
                rouge = int((mat[i][j][0] + mat[i+1][j][0] + mat[i+1][j-1][0] + mat[i][j-1][0] + mat[i-1][j][0] + mat[i-1][j-1][0]) /6)
                vert = int((mat[i][j][1] + mat[i+1][j][1] + mat[i+1][j-1][1] + mat[i][j-1][1] + mat[i-1][j][1] + mat[i-1][j-1][1]) /6)
                bleu = int((mat[i][j][2] + mat[i+1][j][2] + mat[i+1][j-1][2] + mat[i][j-1][2] + mat[i-1][j][2] + mat[i-1][j-1][2]) /6)
            elif (i==0) and (0 < j < (nbrCol(mat)-1)):
                rouge = int((mat[i][j][0] + mat[i+1][j][0] + mat[i+1][j+1][0] + mat[i+1][j][0] + mat[i-1][j-1][0] + mat[i][j-1][0]) /6)
                vert = int((mat[i][j][1] + mat[i+1][j][1] + mat[i+1][j+1][1] + mat[i+1][j][1] + mat[i-1][j-1][1] + mat[i][j-1][1]) /6)
                bleu = int((mat[i][j][2] + mat[i+1][j][2] + mat[i+1][j+1][2] + mat[i+1][j][2] + mat[i-1][j-1][2] + mat[i][j-1][2]) /6)
            elif (i==nbrLig(mat)-1) and (0 < j < (nbrCol(mat)-1)):
                rouge = int((mat[i][j][0] + mat[i-1][j][0] + mat[i-1][j+1][0] + mat[i-1][j-1][0] + mat[i][j-1][0] + mat[i][j+1][0]) /6)
                vert = int((mat[i][j][1] + mat[i-1][j][1] + mat[i-1][j+1][1] + mat[i-1][j-1][1] + mat[i][j-1][1] + mat[i][j+1][1]) /6)
                bleu = int((mat[i][j][2] + mat[i-1][j][2] + mat[i-1][j+1][2] + mat[i-1][j-1][2] + mat[i][j-1][2] + mat[i][j+1][2]) /6)

            mat[i][j] = (rouge, vert, bleu, 255)

    modify(mat)

def dithering():
    mat=loading(nomImgCourante)
    mat_res = [[(0, 0, 0, 0)]*nbrCol(mat) for i in range(nbrLig(mat))]
    for i in range(nbrLig(mat_res)):
        for j in range(nbrCol(mat_res)):
            luminosite = int((mat[i][j][0] + mat[i][j][1] + mat[i][j][2]) / 3)
            proba = luminosite/256
            nb = np.random.choice(np.arange(0, 2), p=[1-proba, proba])
            if nb == 0:
                mat_res[i][j]=(0, 0, 0, 255)
            else:
                mat_res[i][j]=(255, 255, 255, 255)

    modify(mat_res)

def modif_lum(val):
    mat=loading(nomImgCourante)
    mat_res= [[(0, 0, 0, 0)]*nbrCol(mat) for i in range(nbrLig(mat))]
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat_res[i][j] = (mat[i][j][0]+val, mat[i][j][1]+val, mat[i][j][2]+val, 255)
    modify(mat_res)

def bruitage():        # non optimisé
    mat=loading(nomImgCourante)
    mat_res = [[(0, 0, 0, 0)]* nbrCol(mat) for i in range(nbrLig(mat))]
    for i in range(nbrLig(mat_res)):
        for j in range(nbrCol(mat_res)):
            canal = random.randint(0,4)
            plus_ou_moins = random.randint(0,2)
            if canal == 0:
                if plus_ou_moins == 0:
                    if mat[i][j][0] <= 50:
                        mat_res[i][j] = (0, mat[i][j][1], mat[i][j][2], mat[i][j][3])
                    else:
                        mat_res[i][j] = (mat[i][j][0] - 50, mat[i][j][1], mat[i][j][2], mat[i][j][3])
                else :
                    if mat[i][j][0] >= 205:
                        mat_res[i][j] = (255, mat[i][j][1], mat[i][j][2], mat[i][j][3])
                    else:
                        mat_res[i][j] = (mat[i][j][0] + 50, mat[i][j][1], mat[i][j][2], mat[i][j][3])
            elif canal == 1:
                if plus_ou_moins == 0:
                    if mat[i][j][1] <= 50:
                        mat_res[i][j] = (mat[i][j][0], 0, mat[i][j][2], mat[i][j][3])
                    else:
                        mat_res[i][j] = (mat[i][j][0], mat[i][j][1] - 50, mat[i][j][2], mat[i][j][3])
                else :
                    if mat[i][j][1] >= 205:
                        mat_res[i][j] = (mat[i][j][0], 255, mat[i][j][2], mat[i][j][3])
                    else:
                        mat_res[i][j] = (mat[i][j][0], mat[i][j][1] + 50, mat[i][j][2], mat[i][j][3])
            elif canal == 2:
                if plus_ou_moins == 0:
                    if mat[i][j][2] <= 50:
                        mat_res[i][j] = (mat[i][j][0], mat[i][j][1], 0, mat[i][j][3])
                    else:
                        mat_res[i][j] = (mat[i][j][0], mat[i][j][1], mat[i][j][2] - 50, mat[i][j][3])
                else :
                    if mat[i][j][2] >= 205:
                        mat_res[i][j] = (mat[i][j][0], mat[i][j][1], 255, mat[i][j][3])
                    else:
                        mat_res[i][j] = (mat[i][j][0], mat[i][j][1], mat[i][j][2] + 50, mat[i][j][3])
    modify(mat_res)
    
    ### Interface graphique
    
    create=True
   
fenetre = tk.Tk()
fenetre.title("Mon Petit Photoshop")

def fermer_fenetre():
    fenetre.destroy()

#Création des Widgets :

bouton_retour = tk.Button(fenetre, text="Retour", command=reaffiche)

bouton_charger = tk.Button(fenetre, text="Charger", command=lambda :charger(fenetre))

bouton_quitter = tk.Button(fenetre, text="Quitter", command=fermer_fenetre)

label = tk.Label(fenetre, text="Camille Le Corre 22101284")

bouton_sauvegarder = tk.Button(fenetre, text="Sauvegarder", command=saving)

image = tk.Canvas()

bouton_vert = tk.Button(fenetre, text="Filtre vert", command=filtre_vert)

bouton_negatif = tk.Button(fenetre, text="Négatif", command=negatif)

bouton_symetrique = tk.Button(fenetre, text="Symétrique", command=symetrique)

bouton_gris = tk.Button(fenetre, text="Niveaux de gris", command=gris)

bouton_noirblanc_moche = tk.Button(fenetre, text="Noir et Blanc", command=noirBlanc)

bouton_zoom = tk.Button(fenetre, text="Zoom", command=zoom)

bouton_dezoom = tk.Button(fenetre, text="Dézoom", command=shrink)

bouton_flou = tk.Button(fenetre, text="Flou", command=flou)

bouton_noirblanc_beau = tk.Button(fenetre, text="Noir et Blanc (moyenne)", command=dithering)

bouton_poster = tk.Button(fenetre, text="Poster", command=poster)

bouton_rot_gauche = tk.Button(fenetre, text="Rotation Gauche", command=rotate_gauche)

bouton_rot_droite = tk.Button(fenetre, text="Rotation Droite", command=rotate_droite)

slider = tk.Scale(fenetre, from_=-100, to=100)

bouton_slider = tk.Button(fenetre, text="Luminosité", command=lambda: modif_lum(slider.get()))

bouton_bruitage = tk.Button(fenetre, text="Bruitage", command=bruitage)


#Positionnement des Widgets

bouton_retour.grid(column=0, row=8)

bouton_charger.grid(column=0, row=7)

bouton_quitter.grid(column=3, row=8)

label.grid(column=1, row=8)

image.grid(column=1, columnspan=1, row=0, rowspan=8)

bouton_vert.grid(column=3, row=0)

bouton_negatif.grid(column=3, row=1)

bouton_symetrique.grid(column=3, row=2)

bouton_gris.grid(column=3, row=3)

bouton_noirblanc_moche.grid(column=3, row=4)

bouton_zoom.grid(column=0, row=0)

bouton_dezoom.grid(column=0, row=1)

bouton_flou.grid(column=0, row=2)

bouton_noirblanc_beau.grid(column=3, row=5)

bouton_poster.grid(column=0, row=3)

bouton_rot_gauche.grid(column=0, row=5)

bouton_rot_droite.grid(column=0, row=4)

slider.grid(column=3, row=6)

bouton_slider.grid(column=3, row=7)

bouton_bruitage.grid(column=0, row=6)

#Lancement de la boucle 

fenetre.mainloop()
