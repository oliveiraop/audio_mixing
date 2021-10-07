import os
import wave
import struct
import numpy as np
import matplotlib.pyplot as plt


def StereoToMono(pasta):
    erro = ""
    erroT = ""
    for nome in os.listdir(pasta):
        if (nome.endswith('.wav')):
            arquivoWav = wave.open(pasta+"/"+nome, 'rb')
            nchannels =  arquivoWav.getnchannels() #"Número canais: ",
            sampwidth = arquivoWav.getsampwidth() # "Número bytes: " ,
            framerate = arquivoWav.getframerate() #"Taxa de amostragem: "
            nframes = arquivoWav.getnframes() # "Número de frames: "
            if (nchannels != 2 or sampwidth != 2):
                erroS = ("Arquivo "+nome+" não pôde ser convertido\n")
                erroT = erroT+erroS
            else:
                params = list(arquivoWav.getparams())
                params[0] = 1 #um canal
                params = tuple(params)
                ## copiar dados stereo e transformar em mono
                frames = arquivoWav.readframes(nframes) # gravação dos frames em um vetor de bytes
                arquivoWav.close()
                fmt = "<%ih" % (nframes * nchannels) ## tamanho do vetor de bytes
                wavDataList =  list(struct.unpack(fmt, frames)) ## transformar o vetor bytes em uma lista de inteiros
                channelZero = wavDataList[0::nchannels] #valores pares da lista (um lado do audio)
                channelOne = wavDataList[1::nchannels] # valores impares (outro lado do audio)
                arquivoWav = wave.open(pasta+"/"+nome, 'wb')
                arquivoWav.setparams(params) # alteração dos parametros do
                ## loop que pega frame por frame e empacota como bytes e escreve no .wav
                for i in range(0, len(channelZero)):
                    channelZero[i] = int((channelZero[i] + channelOne[i])/2)
                    data = struct.pack('<h', channelZero[i])
                    arquivoWav.writeframesraw(data)
                arquivoWav.close()
        else:
            erroS = ("Arquivo "+nome+" não é um arquivo Wav\n")
            erroT = erroT+erroS

    erro = erroT + "Conversão concluida"

    return erro
            ##check final do arquivo mono para efeito de testes
            ##arquivoWav = wave.open("./"+pasta+"/"+nome, 'rb')
            ##nchannels =  arquivoWav.getnchannels() #"Número canais: ",
            ##nframes = arquivoWav.getnframes() # "Número de frames: "
            ##frames = arquivoWav.readframes(nframes)
            ##fmt = "<%ih" % (nframes * nchannels)
            ##wavDataList =  list(struct.unpack(fmt, frames))
            ##print(len(wavDataList))

def PlotWav(filepath):


    if (filepath.endswith('.wav')):
        arquivoWav = wave.open(filepath, "rb")
        nchannels = arquivoWav.getnchannels()
        sampwidth = arquivoWav.getsampwidth()
        nframes = arquivoWav.getnframes()
        frames = arquivoWav.readframes(nframes)
        fs = arquivoWav.getframerate()
        if (nchannels != 2 or sampwidth != 2):
            fmt = "<%ih" % (nframes * nchannels)
            wavDataList =  list(struct.unpack(fmt, frames))
            for i in range(0, len(wavDataList)):
                wavDataList[i] = wavDataList[i]/32767
            Time=np.linspace(0, len(wavDataList)/fs, num=len(wavDataList))
            plt.figure()
            plt.title(os.path.basename(filepath)+" Signal")
            plt.ylim(1,-1)
            plt.plot(Time, wavDataList)
            plt.show()

        

def IndexarPasta(pasta):
    erro = ""
    erroT=""
    i = 1
    for nome in os.listdir(pasta):
        if (nome.endswith('.wav')):
            os.rename(pasta+"/"+nome, pasta+"/"+str(i)+".wav")
            i = i+1
        else:
            erroS = ("Arquivo "+nome+" não é um arquivo Wav\n")
            erroT=erroT+erroS
    erro = (erroT + "Indexação Concluída")
    return erro

def DobrarBPM (filepath):
    erroS = "Arquivo com BPM Dobrados"
    if (filepath.endswith('.wav')):
        arquivoWav = wave.open(filepath, "rb")
        nchannels = arquivoWav.getnchannels()
        sampwidth = arquivoWav.getsampwidth()
        nframes = arquivoWav.getnframes()
        frames = arquivoWav.readframes(nframes)
        fs = arquivoWav.getframerate()
        if (nchannels != 1 or sampwidth != 2):
            erroS = ("Arquivo não pôde ser convertido\n")
        else:
            params = list(arquivoWav.getparams())
            params[5] = nframes/2 #um canal
            params = tuple(params)
            arquivoWav.close()
            fmt = "<%ih" % (nframes * nchannels) ## tamanho do vetor de bytes
            wavDataList =  list(struct.unpack(fmt, frames)) ## transformar o vetor bytes em uma lista de inteiros
            channelZero = wavDataList[0::2] #valores pares da lista (um lado do audio)
            arquivoWav = wave.open(filepath, 'wb')
            arquivoWav.setparams(params) # alteração dos parametros do
            ## loop que pega frame por frame e empacota como bytes e escreve no .wav
            for i in range(0, len(channelZero)):
                data = struct.pack('<h', channelZero[i])
                arquivoWav.writeframesraw(data)
            arquivoWav.close()
    else:
        erroS = ("Arquivo não é um arquivo Wav\n")

    return erroS

def ReduzirBPM (filepath):
    erroS = "Arquivo com BPM Reduzidos pela metade"
    if (filepath.endswith('.wav')):
        arquivoWav = wave.open(filepath, "rb")
        nchannels = arquivoWav.getnchannels()
        sampwidth = arquivoWav.getsampwidth()
        nframes = arquivoWav.getnframes()
        frames = arquivoWav.readframes(nframes)
        fs = arquivoWav.getframerate()
        if (nchannels != 1 or sampwidth != 2):
            erroS = ("Arquivo não pôde ser convertido\n")
        else:
            params = list(arquivoWav.getparams())
            params[5] = nframes*2
            params = tuple(params)
            arquivoWav.close()
            fmt = "<%ih" % (nframes * nchannels) ## tamanho do vetor de bytes
            wavDataList =  list(struct.unpack(fmt, frames)) ## transformar o vetor bytes em uma lista de inteiros
            arquivoWav = wave.open(filepath, 'wb')
            arquivoWav.setparams(params) # alteração dos parametros do
            ## loop que pega frame por frame e empacota como bytes e escreve no .wav
            for i in range(0, len(wavDataList)):
                data = struct.pack('<h', wavDataList[i])
                arquivoWav.writeframesraw(data)
                arquivoWav.writeframesraw(data)
            arquivoWav.close()
    else:
        erroS = ("Arquivo não é um arquivo Wav\n")

    return erroS
