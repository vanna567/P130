import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

cap = cv2.VideoCapture(0)

# Descomenta el código correcto

#Width  = int(cap.get(cv2.CAP_PROP_FRAME_Height)) 
#Height  = int(cap.get(cv2.CAP_PROP_FRAME_Width))

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

#width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
#height  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

#width  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
#height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

state = None

# Define una función para contar los dedos
def countFingers(image, hand_landmarks, handNo=0):

    global state

    if hand_landmarks:
        # Obtén todos los puntos de referencia de la PRIMERA MANO VISIBLE
        landmarks = hand_landmarks[handNo].landmark

        # Contar dedos        
        fingers = []

        for lm_index in tipIds:
                # Obtén el valor de la punta y la parte baja del dedo
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Revisa si los dedos están abiertos o cerrados
                if lm_index !=4:
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # imprime("El DEDO con el id ",lm_index," está abierto")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # imprime ("El dedo con el id ",lm_index," está cerrado")

        
        totalFingers = fingers.count(1)
      
        # Control de la presentación
        # Descomenta el codigo correcto

        #finger_tip_y = (landmarks[8].x)*width
        #finger_tip_x = (landmarks[8].y)*height

        #finger_tip_x = (landmarks[8].x)*height
        #finger_tip_y = (landmarks[8].y)*width

        finger_tip_x = (landmarks[8].x)*width
        finger_tip_y = (landmarks[8].y)*height

        #finger_tip_x = (landmarks[8].x)*Width
        #finger_tip_y = (landmarks[8].y)*Height
        
        
        if totalFingers >= 1:
            if  finger_tip_x < height-250:
                print("Desplazarse hacia arriba")
                keyboard.press(Key.up)

            if finger_tip_x > height-250:
                print("Desplazarse hacia abajo")
                keyboard.press(Key.down)
       
        
        
# Define una función para
def drawHandLanmarks(image, hand_landmarks):

    #  Establece conexiones entre puntos de referencia
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)
    
    # Detecta los puntos de referencia de las manos 
    results = hands.process(image)

    # Obtén la posición del punto de referencia del resultado procesado
    hand_landmarks = results.multi_hand_landmarks

    # Establece los puntos de referencia
    drawHandLanmarks(image, hand_landmarks)

    # Obtén la posición de los dedos de la mano       
    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Sal de la ventana al presionar la barra espaciadora
    key = cv2.waitKey(1)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
