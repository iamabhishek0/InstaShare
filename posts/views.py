
from django.views import generic
from django.contrib import messages
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django import forms
from .forms import UserRegistrationForm,PostForm
from .models import Post
import cv2
import os
import numpy as np
from PIL import Image




def post_list(request):

    blog_post = Post.objects.all()
    query = request.GET.get("q")
    if query:
        blog_post = blog_post.filter(Q(title__icontains=query)|
                                    Q(content__icontains=query)).distinct()
    paginator = Paginator(blog_post, 3)  # Show 25 contacts per page

    page = request.GET.get('page')
    all_posts = paginator.get_page(page)


    return render(request, 'posts/index.html', {'all_posts': all_posts})


class Detailview(generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'

def tag(request,pk):
    subjects = ["", "Abhishek", "Smita"]
    def detect_face(img):
        # convert the test image to gray image as opencv face detector expects gray images
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # load OpenCV face detector, I am using LBP which is fast
        # there is also a more accurate but slow Haar classifier
        face_cascade = cv2.CascadeClassifier('opencv-face-recognition-python-master/opencv-files/lbpcascade_frontalface.xml')

        # let's detect multiscale (some images may be closer to camera than others) images
        # result is a list of faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

        # if no faces are detected then return original img
        if (len(faces) == 0):
            return None, None

        # under the assumption that there will be only one face,
        # extract the face area
        (x, y, w, h) = faces[0]

        # return only the face part of the image
        return gray[y:y + w, x:x + h], faces[0]
    def prepare_training_data(data_folder_path):

        # ------STEP-1--------
        # get the directories (one directory for each subject) in data folder
        dirs = os.listdir(data_folder_path)

        # list to hold all subject faces
        faces = []
        # list to hold labels for all subjects
        labels = []

        # let's go through each directory and read images within it
        for dir_name in dirs:

            # our subject directories start with letter 's' so
            # ignore any non-relevant directories if any
            if not dir_name.startswith("s"):
                continue;

            # ------STEP-2--------
            # extract label number of subject from dir_name
            # format of dir name = slabel
            # , so removing letter 's' from dir_name will give us label
            label = int(dir_name.replace("s", ""))

            # build path of directory containin images for current subject subject
            # sample subject_dir_path = "training-data/s1"
            subject_dir_path = data_folder_path + "/" + dir_name

            # get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path)

            # ------STEP-3--------
            # go through each image name, read image,
            # detect face and add face to list of faces
            for image_name in subject_images_names:

                # ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue;

                # build image path
                # sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name

                # read image
                image = cv2.imread(image_path)

                # display an image window to show the image
                # cv2.imshow("Training on image...", cv2.resize(image, (400, 500)))
                # cv2.waitKey(100)

                # detect face
                face, rect = detect_face(image)

                # ------STEP-4--------
                # for the purpose of this tutorial
                # we will ignore faces that are not detected
                if face is not None:
                    # add face to list of faces
                    faces.append(face)
                    # add label for this face
                    labels.append(label)

        # cv2.destroyAllWindows()
        # cv2.waitKey(1)
        # cv2.destroyAllWindows()

        return faces, labels
    print("Preparing data...")
    print(os.listdir())
    faces, labels = prepare_training_data("opencv-face-recognition-python-master/training-data")
    print("Data prepared")

    # print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    face_recognizer.train(faces, np.array(labels))

    def draw_rectangle(img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # function to draw text on give image starting from
    # passed (x, y) coordinates.
    def draw_text(img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    def predict(test_img):
        # make a copy of the image as we don't want to chang original image
        img = test_img.copy()
        # detect face from the image
        face, rect = detect_face(img)
        # predict the image using our face recognizer
        if face is not None:
            label, confidence = face_recognizer.predict(face)
            # get name of respective label returned by face recognizer
            label_text = subjects[label]

            # draw a rectangle around face detected
            draw_rectangle(img, rect)
            # draw name of predicted person
            draw_text(img, label_text, rect[0], rect[1] - 5)

            return img, label_text
        else:
            print("wrong")
            return

    # Now that we have the prediction function well defined, next step is to actually call this function on our test images and display those test images to see if our face recognizer correctly recognized them. So let's do it. This is what we have been waiting for.

    # In[10]:

    print("Predicting images...")
    image_name=Post.objects.filter(pk=pk)[0].post_image.url
    post=Post.objects.filter(pk=pk)[0]

    # load test images
    image_name=image_name[1:]

    test_img1 = cv2.imread(image_name)

    # test_img2 = cv2.imread("test-data/test2.jpg")
    # test_img3 = cv2.imread("test-data/test3.jpg")

    # perform a prediction
    predicted_img1, l = predict(test_img1)

    # predicted_img2, l1 = predict(test_img2)
    # predicted_img3 = predict(test_img3)

    print("Prediction complete")
    # print(type(labels[0]))
    # print(type(faces[0]))
    print('media/tag'+image_name[6:])
    post.tagged_image='tag'+image_name[6:]
    post.tagging=l
    post.save()

    cv2.imwrite('media/tag'+image_name[6:], predicted_img1)
    # print(predicted_img2)

    # display both images
    # cv2.imshow(subjects[1], cv2.resize(predicted_img1, (400, 500)))
    # cv2.imshow(subjects[2], cv2.resize(predicted_img2, (400, 500)))
    # cv2.imshow(subjects[2], cv2.resize(predicted_img3, (400, 500)))

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.waitKey(1)
    # cv2.destroyAllWindows()
    # cv2.waitKey(2)
    # cv2.destroyAllWindows()
    return render(request, 'posts/tagged.html',{'post':post})
def tagyes(request,pk):
    post = Post.objects.filter(pk=pk)[0]
    post.want_to_tag=True
    post.save()
    return render(request,'posts/detail.html',{'post':post})
def tagno(request,pk):
    post = Post.objects.filter(pk=pk)[0]
    post.want_to_tag=False
    post.save()
    return render(request,'posts/detail.html',{'post':post})


def post_create(request):


    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()

        messages.success(request, "Successfully Created")
        return HttpResponseRedirect('/')
    context = {
        "form": form,
    }
    return render(request, "posts/post_form.html", context)


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'content', 'post_image']

class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('post:index')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'posts/register.html', {'form' : form})


# ignore it

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated



class HelloView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)