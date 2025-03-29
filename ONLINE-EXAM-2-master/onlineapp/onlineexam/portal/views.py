from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *

from .models import FaceImage



from django.shortcuts import render
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required







from django.http import StreamingHttpResponse
import cv2
import numpy as np
import sqlite3
import os
import mediapipe as mp
from django.conf import settings
import threading


# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'form.html')

def register1(request):
    return render(request, 'form1.html')

def dashboard(request):
    teacher = adminimage.objects.get(teacher= request.user)
    context={'teacher':teacher}
    return render(request, 'dashboard.html',context=context)


@login_required
def dashstudent(request):
    obj = studentimage.objects.get(student=request.user)
    context = {'obj': obj}
    return render(request, 'dashstudent.html',context=context)


def admin_register(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('uname')
        password = request.POST.get('pasd')
        confirmpassword = request.POST.get('passw')
        image = request.POST.get('admin-image')
        cdata = request.POST.get('check')
        try:
         if password == confirmpassword:
            hashe_password = make_password(password)
            status = True if cdata == 'on' else False
            admin = User(first_name=firstname, last_name=lastname, email=email, username=username, password=hashe_password)
            admin.save()
            adminimages=adminimage(admin = admin,image = image,confirmadmin = status)
            adminimages.save()
        except Exception as e:
            print(f"Error: {e}")
        return redirect(index)

   

def student_register(request):
    if request.method == 'POST':
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        email = request.POST.get('email')
        registernumber = request.POST.get('rnumber')
        passw = request.POST.get('password')
        confirmpassword = request.POST.get('passw')
        images = request.FILES.get('student-image')
        cdata = request.POST.get('check')
        try:
            if passw == confirmpassword:
                hashe_password = make_password(passw)
                status = True if cdata == 'on' else False
                student = User(first_name=firstname, last_name=lastname, email=email, username=registernumber, password=hashe_password)
                student.save()
                studentimages = studentimage(student=student, image=images, confirmstudent=status)
                studentimages.save()  # Save the student image instance
        except Exception as e:
            print(f"Error: {e}")
        return redirect(index)

def loginpage(request):
    return render(request, 'login.html')

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        pasd = request.POST.get('pwd')

        adminuser = authenticate(username=username, password=pasd)
        if adminuser is not None:
            login(request, adminuser)
            return redirect(dashboard)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(loginpage)

def adminlogout(request):
    logout(request)
    return redirect(index) 




def studentlogin(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        pasd = request.POST.get('pwd')

        studentuser = authenticate(username=username, password=pasd)

        
        if studentuser is not None:
            login(request, studentuser)
            return redirect(dashstudent)
        else:
            messages.error(request, 'Invalid username or password')
            return redirect(loginpage)
            

def studentlogout(request):
    logout(request)
    return redirect(index)  


def question(request):
    if request.method == 'POST':
        qnsno = request.POST.get('questionno')
        enterquestion = request.POST.get('question')
        optiona = request.POST.get('opa')
        optionb = request.POST.get('opb')
        optionc = request.POST.get('opc')
        optiond = request.POST.get('opd')     
        rightanswer = request.POST.get('rightans')
        qns=questionmodel(question_number=qnsno,question=enterquestion,answer1=optiona,answer2=optionb,answer3=optionc,answer4=optiond,rightanswer=rightanswer)
        qns.save()
        return redirect(dashboard)


def home(request):
    if request.method == 'POST':
        # Check if the form has the required fields
        if 'image' in request.FILES and 'name' in request.POST:
            name = request.POST['name']
            image = request.FILES['image']

            # Save the new FaceImage instance
            try:
                face_image = FaceImage(image=image, name=name)
                face_image.save()
                messages.success(request, f"Image for '{name}' saved successfully!")
            except Exception as e:
                messages.error(request, f"Error saving image: {str(e)}")
        else:
            messages.error(request, "Please provide both a name and an image.")

    # Render the home page
    return redirect(dashstudent )










def quiz_view(request):
    if request.method == 'POST':
        data = request.POST
        score = 1  # Initialize score to 0
        total_questions = questionmodel.objects.count()

        # Debug: Print submitted data to verify
        print("Submitted data:", data)

        # Loop through submitted answers and validate
        for question in questionmodel.objects.all():
            question_id = str(question.question_number)  # Match with name
            user_answer = data.get(f'qns_{question_id}')  # Get submitted answer

            # Debug: Print each question and user answer
            print(f"Q{question_id}: {question.question}, User Answer: {user_answer}, Correct: {question.rightanswer}")

            # Validate answer (compare with rightanswer)
            if user_answer and user_answer.strip().lower() == question.rightanswer.strip().lower():
                score += 1  # Increment score if answer is correct
            
            
        # Return score as JSON
        return JsonResponse({'score': score, 'total_questions': total_questions})

    # Render questions for GET request
    questions = questionmodel.objects.all()
    return render(request, 'quiz.html', {'data': questions})






# Open a single camera feed
# Open a single camera feed
"""cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to read frame from camera")
            break

        # Resize frame if needed
        frame = cv2.resize(frame, (640, 480))

        # Convert frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame as a streaming response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    print("Video feed request")
    return StreamingHttpResponse(generate_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
    """


def exam(request):
    data = questionmodel.objects.all()
    context = {'data': data}
    return render(request, 'exam.html',context=context)







# Global variables for camera access
cap = None
camera_lock = threading.Lock()

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_faces=1
)

# Camera parameters
camera_matrix = np.array([
    [640, 0, 320],
    [0, 640, 240],
    [0, 0, 1]
], dtype="double")

dist_coeffs = np.zeros((4, 1))

def load_images_from_db():
    """Load face images from database with proper storage handling"""
    face_images = FaceImage.objects.all()
    images = []
    labels = []
    label_to_id = {}
    current_id = 0

    for face_image in face_images:
        image_path = os.path.join(settings.MEDIA_ROOT, face_image.image.name)
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
        if img is not None:
            if face_image.name not in label_to_id:
                label_to_id[face_image.name] = current_id
                current_id += 1
            
            # Resize image to standard size
            img = cv2.resize(img, (150, 150))
            images.append(img)
            labels.append(label_to_id[face_image.name])
    
    return images, np.array(labels), label_to_id

def home(request):
    """Handle face image uploads"""
    if request.method == 'POST':
        if 'image' in request.FILES and 'name' in request.POST:
            name = request.POST['name']
            image = request.FILES['image']
            
            try:
                # Create and save FaceImage instance
                face_image = FaceImage(name=name)
                face_image.image.save(
                    f"{name}_{image.name}",
                    ContentFile(image.read()),
                    save=True
                )
                messages.success(request, f"Image for '{name}' saved successfully!")
            except Exception as e:
                messages.error(request, f"Error saving image: {str(e)}")
        else:
            messages.error(request, "Please provide both a name and an image.")
    
    return redirect('dashstudent')

def initialize_recognizer():
    """Initialize face recognition model"""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=2,
        neighbors=16,
        grid_x=8,
        grid_y=8,
        threshold=70
    )
    
    images, labels, label_to_id = load_images_from_db()
    if images:
        recognizer.train(images, labels)
        return recognizer, face_cascade, label_to_id
    return None, None, None

def process_frame(frame, recognizer, face_cascade, label_to_id):
    """Process each video frame for face recognition"""
    try:
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=6,
            minSize=(80, 80),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            if roi_gray.size > 0:
                # Preprocess face ROI
                roi_gray = cv2.resize(roi_gray, (150, 150))
                roi_gray = cv2.equalizeHist(roi_gray)
                
                # Recognize face
                id_, confidence = recognizer.predict(roi_gray)
                name = "Unknown"
                if confidence < 65:  # Confidence threshold
                    for key, value in label_to_id.items():
                        if value == id_:
                            name = key
                            break
                
                # Draw results
                color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                cv2.putText(frame, f"{name} ({confidence:.1f})", 
                          (x, y-15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        return frame
        
    except Exception as e:
        print(f"Frame processing error: {e}")
        return frame

def generate_frames():
    """Generate video frames with face recognition"""
    global cap
    recognizer, face_cascade, label_to_id = initialize_recognizer()
    
    while True:
        with camera_lock:
            if cap is None or not cap.isOpened():
                break
            ret, frame = cap.read()
        
        if not ret:
            break
            
        if recognizer:
            frame = process_frame(frame, recognizer, face_cascade, label_to_id)
        
        # Resize and encode frame
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

def video_feed(request):
    """Stream video feed with face recognition"""
    global cap
    try:
        if cap is None:
            # Try different backends
            for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
                cap = cv2.VideoCapture(0, backend)
                if cap.isOpened():
                    break
                    
            if not cap.isOpened():
                return HttpResponse("Could not open camera", status=500)
        
        return StreamingHttpResponse(
            generate_frames(),
            content_type='multipart/x-mixed-replace; boundary=frame'
        )
        
    except Exception as e:
        print(f"Video feed error: {e}")
        return HttpResponse(f"Error: {str(e)}", status=500)

def release_camera(request):
    """Release camera resources"""
    global cap
    with camera_lock:
        if cap is not None:
            cap.release()
            cap = None
    return HttpResponse("Camera released")

# ... (keep all your other existing views unchanged)