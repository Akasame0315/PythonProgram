import cv2
import mediapipe as mp
import time
import math
import autopy
import Globals
import threading
from google.protobuf.json_format import MessageToDict

cap = cv2.VideoCapture(Globals.cameraNum)
mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 2, min_detection_confidence = 0.8,  min_tracking_confidence=0.8) #False=動態, 2=最多偵測2隻手
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color = (0, 0, 255), thickness = 5)   #點的樣式
handConnStyle = mpDraw.DrawingSpec(color = (0, 255, 255), thickness = 3) #線的樣式
pTime, cTime = 0, 0
v1, v2 = 0, 0
Rtext, Ltext, RSign, LSign = "","","",""
RPos, LPos = [0, 0], [0, 0]

def mouseMove(x, y):
    autopy.mouse.move(x , y) # 平滑移动鼠标

# 根據兩點的座標，計算角度
def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_

# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list

# 根據手指角度的串列內容，返回對應的手勢名稱
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1>=50 and f2>=50 and f3>=50 and f4>=50 and f5>=50:
        return '0'
    elif f1>=50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '1'
    elif f1>=50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '2'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5>50:
        return '3'
    elif f1>=50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '4'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5<50:
        return '5'
    elif f1<50 and f2>=50 and f3>=50 and f4>=50 and f5<50:
        return '6'
    elif f1<50 and f2<50 and f3>=50 and f4>=50 and f5>=50:
        return '7'
    elif f1<50 and f2<50 and f3<50 and f4>=50 and f5>=50:
        return '8'
    elif f1<50 and f2<50 and f3<50 and f4<50 and f5>=50:
        return '9'
    else:
        return "none"

# 根據中指根部在畫面上的座標，返回上或下的字串
def hand_updown(height, position):
    if position < (height/2): return "UP"
    elif position >= (height/2): return "DOWN"
    else: return "none"

def modeswitch():
    global pTime, cTime
    global Rtext, Ltext, RSign, LSign
    global cap
    global RPos, LPos, xPos, yPos
    while True:
        # mouse = threading.Thread(target=mouseMove, args=(RPos[0], RPos[1]))
        # mouse.start()
        ret, img = cap.read()
        img = cv2.flip(img, 1)  #畫面鏡像
        if ret:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #bgr圖片轉rgb
            result = hands.process(imgRGB)
            imgHeight = img.shape[0]
            imgWidth = img.shape[1]
            cv2.putText(img, "+", (int(imgWidth/2),int(imgHeight/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 中心點
            
            # print(result.multi_hand_landmarks)  #手21個點的座標
            if result.multi_hand_landmarks: #判斷有沒有偵測到手
                for handLms in result.multi_hand_landmarks: #把每個點畫上去
                    finger_points = []                   # 記錄手指節點座標的串列
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConnStyle) #第三個參數是畫點跟點的連線
                    for i, lm in enumerate(handLms.landmark): #21個點的座標
                        xPos = lm.x*imgWidth
                        yPos = lm.y*imgHeight
                        # xPos = lm.x*(1920)
                        # yPos = lm.y*1080
                        # print(i, xPos, yPos)
                        finger_points.append((xPos,yPos))
                    # if len(result.multi_handedness) == 2:   #判斷有兩隻手
                    #     print("two hands.")
                    # elif len(result.multi_handedness) == 1: #判斷只有一隻手
                    #     print("one hands.")
                    if len(result.multi_handedness) == 2:   #判斷有兩隻手
                        if finger_points:
                            # 中指根部在鏡頭右邊判斷是右手
                            if finger_points[9][0] > (imgWidth/2):
                                finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                                Rtext = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                                # RSign = hand_updown(int(imgHeight), finger_points[9][1])    #判斷右手在畫面上下
                                # RPos  = [int(finger_points[9][0]), int(finger_points[9][1])]
                                # RPos  = [int(xPos), int(yPos)]
                                cv2.putText(img, f"RText:{Rtext}", (30,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                                # cv2.putText(img,f"{RPos}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                            #中指根部在鏡頭左邊判斷是左手
                            if finger_points[9][0] < imgWidth/2:
                                finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                                #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                                Ltext = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                                # LSign = hand_updown(int(imgHeight), finger_points[9][1])    #判斷左手在畫面上下
                                # LPos = [int(finger_points[9][0]), int(finger_points[9][1])]
                                cv2.putText(img, f"LText:{Ltext}", (30,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                                # cv2.putText(img,f"{LPos}", (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            #設定fps
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, f"fps:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            cv2.imshow('img', img)

        if cv2.waitKey(1) == ord('q'):  #按Q退出
            cv2.destroyAllWindows()
            break

def handIdentify():
    global pTime, cTime
    global Rtext, Ltext, RSign, LSign
    global cap
    global RPos, LPos, xPos, yPos
    while True:
        # mouse = threading.Thread(target=mouseMove, args=(RPos[0], RPos[1]))
        # mouse.start()
        ret, img = cap.read()
        img = cv2.flip(img, 1)  #畫面鏡像
        if ret:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #bgr圖片轉rgb
            result = hands.process(imgRGB)
            imgHeight = img.shape[0]
            imgWidth = img.shape[1]
            cv2.putText(img, "+", (int(imgWidth/2),int(imgHeight/2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 中心點
            
            # print(result.multi_hand_landmarks)  #手21個點的座標
            if result.multi_hand_landmarks: #判斷有沒有偵測到手
                for handLms in result.multi_hand_landmarks: #把每個點畫上去
                    finger_points = []                   # 記錄手指節點座標的串列
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConnStyle) #第三個參數是畫點跟點的連線
                    for i, lm in enumerate(handLms.landmark): #21個點的座標
                        xPos = lm.x*imgWidth
                        yPos = lm.y*imgHeight
                        # xPos = lm.x*(1920)
                        # yPos = lm.y*1080
                        # print(i, xPos, yPos)
                        finger_points.append((xPos,yPos))
                    # if len(result.multi_handedness) == 2:   #判斷有兩隻手
                    #     print("two hands.")
                    # elif len(result.multi_handedness) == 1: #判斷只有一隻手
                    #     print("one hands.")
                    if len(result.multi_handedness) == 2:   #判斷有兩隻手
                        if finger_points:
                            finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                            Rtext = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                            # if Rtext == '5':
                            #     Rpos  = [int(finger_points[9][0]/imgWidth*1280), int(finger_points[9][1]/imgHeight*800)]
                            #     cv2.putText(img, f"Text:{Rtext}", (30,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                            #     cv2.putText(img, f"pos {Rpos}", (30,120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                            # cv2.putText(img, f"pos {pos}", (30,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                            
                            #中指根部在鏡頭右邊判斷是右手
                            if finger_points[9][0] > (imgWidth/2):
                                finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                                Rtext = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                                # RSign = hand_updown(int(imgHeight), finger_points[9][1])    #判斷右手在畫面上下
                                RPos  = [(int(finger_points[9][0]/imgWidth*2560)-1280), int(finger_points[9][1]/imgHeight*800)]
                                # RPos  = [int(xPos), int(yPos)]
                                cv2.putText(img, f"RText:{Rtext}", (30,90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                                cv2.putText(img,f"{RPos}", (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
                            # #中指根部在鏡頭左邊判斷是左手
                            if finger_points[9][0] < imgWidth/2:
                                finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                                #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                                Ltext = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                                # LSign = hand_updown(int(imgHeight), finger_points[9][1])    #判斷左手在畫面上下
                                LPos = [int(finger_points[9][0]), int(finger_points[9][1])]
                                cv2.putText(img, f"LText:{Ltext}", (30,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) # 印出文字
                                cv2.putText(img,f"{LPos}", (30, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

            #設定fps
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, f"fps:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            cv2.imshow('img', img)

        if cv2.waitKey(1) == ord('q'):  #按Q退出
            cv2.destroyAllWindows()
            break
# handIdentify()