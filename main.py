from tkinter import *
import functions as f
from tkinter import filedialog

class Application:
    def __init__(main, master=None):
        
        main.fontePadrao = ("Arial", "12")
        main.selecionarPasta = Frame(master)
        main.selecionarPasta["pady"] = 10
        main.selecionarPasta.pack()
        
        main.localPasta = Frame(master)
        main.localPasta.pack()

        main.botoes = Frame(master)
        main.botoes.pack()

        main.info = Frame(master)
        main.info.pack()
        
        main.pasta = Label(main.localPasta, text="Nenhuma Pasta Selecionada")
        main.pasta["font"] = main.fontePadrao
        main.pasta.pack()

        main.infotex = Label(main.localPasta, text="")
        main.infotex["fg"] = "red"
        main.infotex["font"] = ("Arial", "12", "bold")
        main.infotex.pack()
        
        main.indexar = Button(main.botoes)
        main.indexar["text"] = "Indexar"
        main.indexar["font"] = main.fontePadrao
        main.indexar["command"] = main.indexarButton
        main.indexar.pack()

        main.downmix = Button(main.botoes)
        main.downmix["text"] = "Realizar Downmix"
        main.downmix["font"] = main.fontePadrao
        main.downmix["command"] = main.downmixButton
        main.downmix.pack()

        main.plot = Button(main.botoes)
        main.plot["text"] = "Plotar Gráfico"
        main.plot["font"] = main.fontePadrao
        main.plot["command"] = main.plotButton
        main.plot.pack()
        
        main.selecBut = Button(main.selecionarPasta)
        main.selecBut["text"] = "Selecionar Pasta"
        main.selecBut["command"] = main.browseButton
        main.selecBut.pack()

        main.dobrarBPM = Button(main.botoes)
        main.dobrarBPM["text"] = "Dobrar BPM"
        main.dobrarBPM["font"] = main.fontePadrao
        main.dobrarBPM["command"] = main.bpmButton
        main.dobrarBPM.pack()

        main.reduzirBPM = Button(main.botoes)
        main.reduzirBPM["text"] = "Reduzir BPM"
        main.reduzirBPM["font"] = main.fontePadrao
        main.reduzirBPM["command"] = main.rBpmButton
        main.reduzirBPM.pack()

    def rBpmButton(main):
        filename = filedialog.askopenfilename()
        if (filename != ""):
            main.infotex["text"] = f.ReduzirBPM(filename)
        
    def bpmButton(main):
        filename = filedialog.askopenfilename()
        if (filename != ""):
            main.infotex["text"] = f.DobrarBPM(filename)

    def browseButton(main):
        filename = filedialog.askdirectory()
        if (filename != ""):
            main.pasta["text"] = filename
            
    def plotButton(main):
        filename = filedialog.askopenfilename()
        if (filename != ""):
            f.PlotWav(filename)

    def downmixButton(main):
        if (main.pasta["text"] != "Nenhuma Pasta Selecionada"):
            result = f.StereoToMono(main.pasta["text"])
            main.infotex["text"] = result
        else:
            main.infotex["text"] = "Selecionar Pasta"

    def indexarButton(main):
        if (main.pasta["text"] != "Nenhuma Pasta Selecionada"):
            result = f.IndexarPasta(main.pasta["text"])
            main.infotex["text"] = result
        else:
            main.infotex["text"] = "Selecionar Pasta"
        
root = Tk()
Application(root)
root.title("DownMix")
root.mainloop()
