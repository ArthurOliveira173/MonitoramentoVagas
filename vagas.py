import cv2 as cv
import pickle
import numpy

#Iniciando posicoes para vertices de polígonos
vertices = []

#Carregando polígonos armazenados para impedir perda ao reiniciar programa
try:
    with open('VagasGList','rb') as f:
        vagas = pickle.load(f)
except:
    #Se não houver polígonos, Inicia-se a lista de posicoes para polígonos de vagas
    vagas = []

#Função para criar polígono com o clique do Mouse
def click(event, x, y, flags, param):
    global vertices
    global vagas

    #Ao clicar o botão esquerdo do Mouse, cria-se um novo vértice
    if event == cv.EVENT_LBUTTONDOWN:

        #Salvando posição do vértice
        vertices.append((x, y))

        #Se segurar a tecla Alt, o próximo vértice marca o fim do polígono
        if flags == 33:
            #Armazena a posição do polígono na lista de vagas
            vagas.append(numpy.array(vertices))
            #Reinicia polígono
            vertices.clear()
    #Ao clicar o botão direito do Mouse, remove-se o último polígono salvo
    if event == cv.EVENT_RBUTTONDOWN:
        vagas = vagas[:-1]
    #Armazenando polígonos para impedir perda ao reiniciar programa
    with open('VagasGList','wb') as f:
        pickle.dump(vagas,f)

#Capturando a imagem
cv.namedWindow('Imagem base')
while True:
    ref = cv.imread('static/parking.jpg')

    #Criar polígonos sobre as posições armazenadas
    for vaga in vagas:
        # Cria polígono (imagem, vértices, aberto(0)/fechado(1), cores(B,G,R), densidade)
        cv.polylines(ref, [vaga], 1, (255, 0, 0), 2)

    cv.imshow('Imagem base', ref)
    cv.setMouseCallback('Imagem base', click)

    #Encerra o programa ao apertar a tecla Esc
    if cv.waitKey(20) & 0xFF == 27:
        break
