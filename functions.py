def sendwhatsupmsg(mobile_no,message,h,m):
    import pywhatkit
    pywhatkit.sendwhatmsg(r'mobile_no','message',h,m)


def instapost(username,password,path,capture):
    from instagrapi import Client
    cs=Client()
    cs.login('username','password')
    cs.photo_upload('path','capture')


def sendmail(email_sender, password, subject, message, email_receiver):
    try:
        pywhatkit.send_mail(email_sender, password, subject, message, email_receiver)
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)


def searchgoogle(query):
    from googlesearch import search
  
    print("Search results:")
    for result in search(query, num_results=5):
        print(result)

def txtmsg(contact):
    from twilio.rest import Client

    account_sid = 'ACff032a0fcb43e7bd927519de7760'
    auth_token = '6977f153274f5cc8747a23c212e'

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Hello! This is a test message from Python.",
        from_='+15176985',   
        to=contact     
        )
    print("Message sent! SID:", message.sid)


def webscrap(link):
    import requests
    from bs4 import BeautifulSoup

    url =  link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.find_all("h2")
    for title in titles:
        print(title.text)  


def circles():
    import numpy as np
    import cv2

    width, height = 500, 500

    image = np.ones((height, width, 3), dtype=np.uint8) * 255


    colors = [
        (255, 0, 0),   # Red
        (0, 255, 0),   # Green
        (0, 0, 255),   # Blue
        (255, 255, 0), # Yellow
        (255, 0, 255), # Magenta
        (0, 255, 255)  # Cyan
    ]


    for _ in range(20):  # 20 circles
        center = (np.random.randint(0, width), np.random.randint(0, height))
        radius = np.random.randint(20, 100)
        color = colors[np.random.randint(0, len(colors))]
        cv2.circle(image, center, radius, color, -1)  # -1 fills the circle


    cv2.imshow("Random Circles", image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def swapface():
    import cv2
    import numpy as np
    
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def detect_face(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
        if len(faces) == 0:
            return None, None
    
        x, y, w, h = faces[0] 
        face_region = img[y:y+h, x:x+w]
        return face_region, (x, y, w, h)
    
    
    cap = cv2.VideoCapture(0)
    captured_images = []
    
    print(" Press SPACE to capture 2 face images. Press ESC to cancel.")
    
    while len(captured_images) < 2:
        ret, frame = cap.read()
        if not ret:
            break
    
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Press SPACE to capture Image {len(captured_images)+1}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Capture Faces", display_frame)
    
        key = cv2.waitKey(1)
        if key == 32: 
            captured_images.append(frame.copy())
            print(f"✔ Captured Image {len(captured_images)}")
        elif key == 27:  
            print(" Cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            exit()
    
    cap.release()
    cv2.destroyAllWindows()
    
    
    if len(captured_images) == 2:
        img1, img2 = captured_images
    
        face1, coords1 = detect_face(img1)
        face2, coords2 = detect_face(img2)
    
        if face1 is None or face2 is None:
            print("Could not detect face in one or both images.")
            exit()
    
       
        face2_resized = cv2.resize(face2, (coords1[2], coords1[3]))
        face1_resized = cv2.resize(face1, (coords2[2], coords2[3]))
    
       
        img1_result = img1.copy()
        img2_result = img2.copy()
    
       
        x1, y1, w1, h1 = coords1
        x2, y2, w2, h2 = coords2
    
        img1_result[y1:y1+h1, x1:x1+w1] = face2_resized
        img2_result[y2:y2+h2, x2:x2+w2] = face1_resized
    
        
        cv2.imshow("Image 1 with Face 2", img1_result)
        cv2.imshow("Image 2 with Face 1", img2_result)
        print(" Faces swapped. Press any key to close.")
    
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(" Not enough images were captured.")
