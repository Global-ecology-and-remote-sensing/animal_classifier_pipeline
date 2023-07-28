from tkinter import *
import tkinter as tk
import json
import PIL
from PIL import ImageTk, Image
import csv


#global variables and list
imagelist=[]
currentdisplay=0
displaylist=[]
specieslist=[]
confidencelist=[]
num=1

#convert json to csv
def convert_to_csv():
    rows=[]
    for i in range(len(specieslist)):
        if(i==num-1):
            rows.append([i+1, imagelist[i], specieslist[i], "Last Modify"])
        else:
            rows.append([i+1, imagelist[i], specieslist[i], ""])
    Output = imagefile+"\\SpeciesData.csv"
    csvfile= open(Output, 'w', encoding='UTF8', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(["ID", 'Image', 'Species', "Check Point"])
    writer.writerows(rows)

#___________________________________________________TEST
def resizer(e):
    global photo, new_photo, resizephoto, newwidth, newheight
    photo=Image.open(displayphoto)
    height=photo.height
    width=photo.width
    if (e.height<10000):
        newwidth=width*(e.height/height)
        newwidth=int(newwidth)
        if (newwidth>e.width):
            newheight=height*(e.width/width)
            newheight=int(newheight)
            resizephoto=photo.resize((e.width, newheight), Image.ANTIALIAS)
            new_photo = ImageTk.PhotoImage(resizephoto)
        else:
            resizephoto=photo.resize((newwidth, e.height), Image.ANTIALIAS)
            new_photo = ImageTk.PhotoImage(resizephoto)
        ImageCanvas.create_image(e.width/2,e.height/2,image=new_photo, anchor=CENTER)
    else:     
        newwidth=width*(10000/height)
        newwidth=int(newwidth)
        resizephoto=photo.resize((newwidth, 10000), Image.ANTIALIAS)
        new_photo = ImageTk.PhotoImage(resizephoto)
        ImageCanvas.create_image(e.width/2,e.height/2,image=new_photo, anchor=CENTER)
    
#Load previous image
def back():
    #global imglabel #(delete)
    global button_back
    global button_forward
    global imagenumber
    global specieslabel
    global num
    try:
        droplist.grid_forget()
        confirm.grid_forget()
        '''if num==(len(displaylist)):
            convert.grid_forget()'''
        if num==1:
            button_back = Button(root, text="<<", state=DISABLED)
        if num>1:
            num=num-1
        
        show() 
    except:
        if num==(len(displaylist)):
            convert.grid_forget()
        if num==1:
            button_back = Button(root, text="<<", state=DISABLED)
        if num>1:
            num=num-1        
        show() 
        
#load next image
def forward():
    #global imglabel #(delete)
    global button_back
    global button_forward
    global imagenumber
    global specieslabel
    global num
    try:
        droplist.grid_forget()
        confirm.grid_forget()
        if num<len(displaylist):
            num=num+1
        show()
    except:
        if num<len(displaylist):
            num=num+1
        show()
#update species label    
def updatedisplay():
    global specieslabel

    specieslabel.grid_forget()
    specieslabel=Label(text="Species: "+specieslist[num-1])
    specieslabel.grid(row=0, column=0, sticky="nsew")
    specieslabel.configure(font=("Arial",15))
#update json file and list
def mod_list():
    output= Label(root, text=clicked.get())
    new=output.cget("text")
    specieslist[num-1]=new
    droplist.grid_forget()
    confirm.grid_forget()
    with open(jsonfile, "r")as f:
        data=json.load(f)
    data["images"][num-1]["species"]=new
    with open(jsonfile, "w")as f:
        json.dump(data, f)
    updatedisplay()
#change label
def change_label():
    global confirm
    global droplist
    global clicked
    clicked=StringVar()
    clicked.set("Select")
    droplist=OptionMenu(root, clicked,"Bird", 
                        "Canis lupus familiaris", 
                        "Eurasian Otter", 
                        "Felis Catus", 
                        "Herpestes javanicus", 
                        "Hystrix brachyura",
                        "Macaca mulatta",
                        "Melogale species",
                        "Muntiacus species",
                        "Paguma larvata",
                        "Prionailurus bengalensis",
                        "Rodent",
                        "Sus scrofa",
                        "Viverricula indica",
                        "Other animal",
                        "N/A")
    droplist.grid(row=0, column=0, sticky="nsew")
    confirm=Button(text="Confirm", command=mod_list, bg="Yellow")
    confirm.configure(font=("Arial",15))
    confirm.grid(row=0, column=1, sticky="nsew")

    

#display UI
def show():
   # global imglabel #(delete)
    global specieslabel
    global imagenumber
    global button_back
    global button_forward
    global convert
    global middle_frame
    global displayphoto
    global ImageCanvas
    global middle_frame
    global confidencelabel
    
    middle_frame.grid_forget()
    specieslabel.grid_forget()
    imagenumber.grid_forget()
    button_back.grid_forget()
    button_forward.grid_forget()
    confidencelabel.grid_forget()

    specieslabel=Label(text="Species: "+specieslist[num-1])
    specieslabel.configure(font=("Arial",13))
    #imglabel = Label(image=displaylist[num-1])
    confidencelabel=Label(text="Animal: "+confidencelist[num-1])
    confidencelabel.configure(font=("Arial",10))
    button_forward=Button(root, text=">>", command=forward)
    button_forward.configure(font=("Arial",15))
    button_back=Button(root, text="<<", command=back)
    button_back.configure(font=("Arial",15))
    imagenumber = Label(root, text=num)
    imagenumber.configure(font=("Arial",15))

    specieslabel.grid(row=0, column=0, sticky = "nsew")
    #imglabel.grid(row=1, column=0, columnspan=4)
    confidencelabel.grid(row=2, column=1,columnspan=2, sticky = "nsew")
    button_back.grid(row=3, column=0, sticky = "nsew")
    imagenumber.grid(row=3, column=1, columnspan=2)
    button_forward.grid(row=3, column=3, sticky = "nsew")

    if num==(len(displaylist)):
        button_forward = Button(root, text=">>", state=DISABLED)
    convert=Button(root, text="Save",command=convert_to_csv)
    convert.configure(font=("Arial",15))
    convert.grid(row=2, column=3, sticky = "nsew")

    displayphoto=imagelist[num-1]
    middle_frame = Frame(root, width=600, height=400)
    middle_frame.grid(row=1, column=0, columnspan=4, sticky=N+E+S+W)
    ImageCanvas = tk.Canvas(middle_frame, width=600, height=400, bg="black")
    ImageCanvas.pack(fill="both", expand=TRUE)
    #ImageCanvas.create_image(0,0,image=displaylist[num-1], anchor="nw")
    
    root.bind("<Configure>", resizer)
    

#Jump to specific photo
def JumpTo():
    global num
    '''if num==(len(displaylist)):
        convert.grid_forget()'''
    newimage_num=int(jumpto.get())
    if (1<=newimage_num<=len(displaylist)):
        num=newimage_num
    show()


#display the first image
def display():
    global image
    #global imglabel #(delete)
    global specieslabel
    global imagenumber
    global jumpto
    global num
    global button_back
    global button_forward
    global displayphoto
    global ImageCanvas
    global middle_frame
    global droplist
    global confirm
    global confidencelabel
    root.columnconfigure(0, weight=2)
    root.columnconfigure(1, weight=2)   
    root.columnconfigure(2, weight=2)
    root.columnconfigure(3, weight=2)
    root.rowconfigure(1, weight=4)
    
    ##add photo to canvas and use sticky to adjust size
    for i in imagelist:
        image=Image.open(i)
        height=image.height
        width=image.width
        new_height=390
        new_width=width*(new_height/height)
        new_width=int(new_width)
        if(new_width>520):
            new_width=520
            new_height=height*(new_width/width)
            new_height=int(new_height)
        resize_image=image.resize((new_width, new_height))
        displaylist.append(ImageTk.PhotoImage(resize_image))
    
    specieslabel=Label(text="Species: "+specieslist[0])
    specieslabel.configure(font=("Arial",13))
    specieslabel.grid(row=0, column=0, sticky = "nsew")
    changebutton=Button(text="Change", command=change_label)
    changebutton.configure(font=("Arial",15))
    changebutton.grid(row=0, column=1)
    jumpto=Entry(root, width=10)
    jumpto.grid(row=0, column=2, sticky="nsew")
    jumptobutton=Button(text="Jump To", command=JumpTo)
    jumptobutton.configure(font=("Arial",15))
    jumptobutton.grid(row=0, column=3, sticky = "nsew")

    ###imglabel=Label(image=displaylist[0])
    ###imglabel.grid(row=1, column=0, columnspan=4)
    #__________________________________________test
    displayphoto=imagelist[0]
    middle_frame = Frame(root, width=600, height=400)
    middle_frame.grid(row=1, column=0, columnspan=4, sticky=N+E+S+W)
    ImageCanvas = tk.Canvas(middle_frame, width=600, height=400, bg="black")
    ImageCanvas.pack(fill="both", expand=TRUE)
    #ImageCanvas.create_image(0,0,image=displaylist[0], anchor="nw")
    root.bind("<Configure>", resizer)
    
   
    #Label(middle_frame,  image=displaylist[0],  bg='grey').grid(row=0,  column=0,  padx=5,  pady=5, sticky='w'+'e'+'n'+'s')
    #test
    '''root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    ImageCanvas = tk.Canvas(root, width=600, height=400, bg="blue")
    ImageCanvas.grid(row = 1 ,column = 0, columnspan = 5)
    ImageCanvas.pack(expand=True)
    ImageCanvas.create_image(300, 200, image=displaylist[0])'''
    confidencelabel=Label(text="Animal: "+confidencelist[0])
    confidencelabel.configure(font=("Arial",10))
    confidencelabel.grid(row=2, column=1,columnspan=2, sticky = "nsew")
    button_forward=Button(root, text=">>", command=forward)
    button_forward.configure(font=("Arial",15))
    button_back=Button(root, text="<<", command=back)
    button_back.configure(font=("Arial",15))
    imagenumber = Label(root, text=num)
    imagenumber.configure(font=("Arial",15))
    button_back.grid(row=3, column=0, sticky = "nsew")
    imagenumber.grid(row=3, column=1, columnspan=2, sticky = "nsew")
    button_forward.grid(row=3, column=3, sticky = "nsew")
    
        
#get images path
def getpath():
    global jsonfile
    global imagefile
    global confidencelist
    jsonfile= e.get()
    imagefile=e2.get() 
    e.destroy()
    e2.destroy()
    Label1.destroy()
    Label2.destroy()
    myButton.destroy()
#read json file
    try:
        with open(jsonfile, "r")as f:
            data=json.load(f)
    #get file name
        data1=data["images"]
        for i in range(len(data1)):
            imagepath=[imagefile,"\\",data1[i]["file"]]
            imagelist.append("".join(imagepath))
            specieslist.append(data1[i]["species"])
            confidencelist.append(data1[i]["confidence"])
        display()
    except: main()

#first page    
def main():
    global Label1
    global Label2
    global e
    global e2
    global myButton
    global root
    
    root.geometry("900x600")
    ##ask for input (file path)
    #Enter Json file path
    Label1=Label(root, text="Path to JSON file")
    Label1.pack()
    e = Entry(root, width=50, borderwidth=5)
    e.pack()
    #Enter image file path
    Label2=Label(root, text="Path to Image file")
    Label2.pack()
    e2 = Entry(root, width=50, borderwidth=5)
    e2.pack()
    #Confirm Button
    myButton = Button(root, text = "Confirm", command = getpath)
    myButton.pack()

    root.mainloop()     
root = Tk()
main()

