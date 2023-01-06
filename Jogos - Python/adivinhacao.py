import random

def jogar():

    print("*********************************")
    print("Bem vindo ao jogo de Adivinhação!")
    print("*********************************")

    numero_secreto = round(random.randrange(1,101))
    tentativas = 0
    pontos = 1000

    print("Escolha um nível de dificuldade:")
    print("(1) Fácil (2) Médio (3) Dificil")
    nivel = int(input("Defina o nível:"))

    if (nivel ==1):
        tentativas = 20

    elif(nivel == 2):
        tentativas = 10

    else:
        tentativas = 5


    for rodada in range(1,tentativas + 1):
        print("Tentativa: {} de {}".format(rodada, tentativas))
        chute = (input ("Digite um entre 1 e 100 número:"))
        chute = int(chute)
        print("Você digitou", chute)

        if(chute < 1 or chute > 100):
            print("Você deve digitar um numero entre 1 a 100")
            continue

        acertou = chute == numero_secreto
        maior   = chute > numero_secreto
        menor   = chute < numero_secreto

        if (acertou):
            print("Você acertou! e fez {} pontos".format(pontos))
            break

        else:
            if(maior):
                print("Seu numero foi maior do que o esperado.")

            elif(menor):
                print("O numero foi menor que o esperado.")
                pontos_perdidos = abs(numero_secreto - chute)
                pontos = pontos - pontos_perdidos

    print("FIM DE JOGO")

if(__name__=="__main__"):
    jogar()