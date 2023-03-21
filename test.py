import cv2 as cv
import pickle
import cvzone
import numpy

ocupado = [170, 240, 260, 359, 259, 396, 372, 437, 450, 428, 534, 462, 554, 494, 452, 472, 475, 370, 452, 395, 299, 380, 314,
           200, 242, 248, 197, 370, 660, 621, 672, 747, 955, 909, 664, 705, 596, 244, 285, 684, 740, 908, 1082, 1139, 957,
           823, 792, 530, 550, 984, 1279, 1358, 2150, 1773, 1452, 730, 800, 620]

#Captura de vídeo
cap = cv.VideoCapture('video.mp4')

#Carregando posições das vagas armazenadas
with open('VagasList', 'rb') as f:
    vagas = pickle.load(f)

#Carregando vagas para visualização na Web
with open('VagasGList', 'rb') as fg:
    vagasG = pickle.load(fg)

#Função para checar disponibilidade das vagas pela diferença de pixels (pixels pretos: vazio, pixels brancos: objeto presente)
def checarVagas(refDilatada, lot):
    #Auxiliar para criar uma imagem para cada vaga e verificar disponibilidade
    count = 1
    #Número de vagas disponíveis
    livres = 58
    #Processar polígonos sobre as posições armazenadas
    for vaga in vagas:

        #Recortando a área da imagem com a vaga
        rect = cv.boundingRect(vaga)
        x, y, w, h = rect
        recorte = refDilatada[y:y + h, x:x + w].copy()

        #Criando mascara ao redor da vaga
        pontos = vaga - vaga.min(axis=0)
        mascara = numpy.zeros(recorte.shape[:2], numpy.uint8)
        cv.drawContours(mascara, [pontos], -1, (255, 255, 255), -1, cv.LINE_AA)

        #Adicionando mascara ao recorte
        vagaInstancia = cv.bitwise_and(recorte, recorte, mask=mascara)

        #Mostrando o recorte de cada vaga individual durante a execução do vídeo
        #mostrarRecortes(vagaInstancia, count)

        #Mostra o número de pixels brancos em cada vaga
        #mostrarPixels(x, y, w, h, vagaInstancia, count, lot)

        #Verificar o estado de disponibilidade da vaga (Disponível/Ocupado)
        status = verificarDisponibilidade(vagaInstancia, count)

        # Mostrar a disponibilidade de cada vaga através de polígonos (verde: livre, vermelho: ocupado)
        livres = mostrarStatus(vaga, livres, status, lot)

        #Incrementando auxiliar
        count = count + 1

    # cvzone.putTextRect(lot, "Vagas livres: "+str(livres)+"/58", (25, 45), scale=1.5, thickness=2, offset=0, colorR=(188, 188, 188),
    #                    colorT=(0, 0, 0), font=cv.FONT_HERSHEY_DUPLEX)

#Função para mostrar o recorte de cada vaga individual durante a execução do vídeo
def mostrarRecortes(vaga, count):
    cv.imshow("vaga" + str(count), vaga)

#Função para mostrar a disponibilidade de cada vaga através de polígonos (verde: livre, vermelho: ocupado)
def mostrarStatus(vaga, livres, status, lot):
    #Se a vaga estiver vazia, criar polígono verde
    if status == False:
        # Cria polígono (imagem, vértices, aberto(0)/fechado(1), cores(B,G,R), densidade)
        cv.polylines(lot, [vaga], 1, (0, 255, 0), 2)
    #Se a vaga estiver ocupada, criar polígono vermelho
    else:
        #Reduz o número de vagas disponíveis em 1
        livres -= 1
        # Cria polígono (imagem, vértices, aberto(0)/fechado(1), cores(B,G,R), densidade)
        cv.polylines(lot, [vaga], 1, (0, 0, 255), 2)
    return livres

#Função para mostrar o número de pixels brancos em cada vaga
def mostrarPixels(x, y, w, h, img, count, ref):
    if (count%2 == 0):
        cX = int((x + w - 5) - (w / 2))
        cY = int((y + h) - (h / 3))
    else:
        cX = int((x + w - 5) - (w / 2))
        cY = int((y + h) - (h / 1.5))

    pixels = cv.countNonZero(img)
    cvzone.putTextRect(ref, str(pixels), (cX - 5, cY + 5), scale=1.5, thickness=1, offset=0)

#Função para verificar o estado de disponibilidade da vaga (Disponível/Ocupado)
def verificarDisponibilidade(vaga, count):
    global ocupado
    pixels = cv.countNonZero(vaga)

    if pixels >= ocupado[count-1]:
        return True
    else:
        return False

def main():
    # Contador para remover excesso de quadros para acelerar o vídeo
    frameCut = 0

    cap.set(cv.CAP_PROP_POS_FRAMES, 0)
    while True:
        # Se o quadro atual for o último quadro do vídeo, o vídeo é reproduzido novamente
        if cap.get(cv.CAP_PROP_POS_FRAMES) == cap.get(cv.CAP_PROP_FRAME_COUNT):
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            segundos = 0

        # Reprodução do vídeo
        success, ref = cap.read()

        frameCut += 1
        if not success:
            break
        elif frameCut != 1:
            if frameCut >= 8:
                frameCut = 0
        else:
            # Transformação do vídeo em pixels binários (preto e branco)
            refCinza = cv.cvtColor(ref, cv.COLOR_BGR2GRAY)
            refBlur = cv.GaussianBlur(refCinza, (3, 3), 1)
            refBordas = cv.adaptiveThreshold(refBlur, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 25, 16)
            refMediano = cv.medianBlur(refBordas, 3)
            kernel = numpy.ones((1, 2), numpy.uint8)
            refDilatada = cv.dilate(refMediano, kernel, iterations=1)

            # Checar disponibilidade das vagas pelo vídeo transformado
            checarVagas(refDilatada, ref)

            # Mostrar janela
            cv.imshow("Estacionamento", ref)

            # Encerra o programa ao apertar a tecla Esc
            if cv.waitKey(20) & 0xFF == 27:
                break
main()