import forca
import adivinhacao

print("*********************************")
print("Escolha seu jogo:")
print("*********************************")

print("(1)Forca (2)Adivinhação")

jogo = int(input("Qual jogo?"))

if(jogo == 1):
    print("Jogo da forca selecionado")
    forca.jogar()

elif(jogo == 2):
    print("Adivinhação selecionado")
    adivinhacao.jogar()