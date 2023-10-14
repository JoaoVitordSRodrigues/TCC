# Importa a Biblioteca OPENCV --> Usada para o Reconhecimento em si 
import cv2

# variável que passa a xml que usaremos no código
xml_haar_cascade = 'haarcascade_frontalface_alt2.xml'

# Carrega o classificador
faceClassifier = cv2.CascadeClassifier(xml_haar_cascade)

# Inicia a Camera
capture = cv2.VideoCapture(0)

# Define o Tamanho da largura na captura de acordo com o tamanho da webcam 
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

# Define o Tamanho da altura na captura de acordo com o tamanho da webcam 
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Deixa a Captura ao vivo em um loop até ser pressionado a letra 'Q' e o sistema ser fechado
while not cv2.waitKey(20) & 0xFF == ord('q'):
    ret, frame_color = capture.read()

  # Define que a captura vai ser em imagem colorida 
    gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

  # Detecta o rosto em si da pessoa 
    faces = faceClassifier.detectMultiScale(gray)

  # Define altura e largura do que será detectado   
    for x, y, w, h in faces:
        cv2.rectangle(frame_color, (x,y), (x + w, y + h), (0,0,255), 2 )


  # Deixa em si a imagem colorida 
    cv2.imshow('color', frame_color)   
 