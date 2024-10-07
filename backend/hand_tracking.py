import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def check_for_hand_hover(hand_landmarks, button_rect):
    """Check if hand is over a button."""
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    x = int(index_finger_tip.x * 800)  # Assuming 800px screen width
    y = int(index_finger_tip.y * 600)  # Assuming 600px screen height
    return button_rect.contains(x, y)

def start_hand_tracking_for_buttons(alvex_screen):
    """Start hand tracking and check for interaction with buttons."""
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Pass hand landmarks to the A.L.V.E.X. screen to check for interaction
                    alvex_screen.handle_hand_gesture(hand_landmarks)

            cv2.imshow('Hand Tracking', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
