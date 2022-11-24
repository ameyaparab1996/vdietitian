from dietplan import genPlan

from django.shortcuts import render, redirect
from dietplan.forms import UserForm, UserInfoForm, feedbackForm
from .models import UserDetails, feedback
from django.contrib import messages
from datetime import date
import openpyxl
import json
from django.utils import timezone
from dietplan import feedback as feedbackpy

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

# important imports to enable login and logout functionality
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.template import loader



def index(request):
    return render(request, 'index.html')


# log out view
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# Register user view
def user_register(request):
    form_error = " "
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            template = loader.get_template('registration/confirmmesg.html')
            return HttpResponse(template.render())
            #return HttpResponse('Please confirm your email address to complete the registration')
            #registered = True
            form_error = 'Registration Successfull! Please login to continue.'
        else:
            form_error = user_form.errors
    else:
        user_form = UserForm()
    return render(request, 'registration/registration.html', {'registered': registered,
                                                              'user_form': user_form,
                                                              'form_error': form_error})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        #login(request, user)
        # return redirect('home')
        template = loader.get_template("registration/emailconfirmed.html")
        return HttpResponse(template.render())
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# Log in user view
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("User inactive")
        else:
            print('Someone tried login and failed!')
            print('username: {} and password: {}'.format(username, password))
            messages.add_message(request, messages.ERROR, 'Invalid login details supplied')
            return render(request, 'registration/login.html', {})
    else:
        return render(request, 'registration/login.html', {})


# view of necessary input form
@login_required
def UserInfoView(request, pk):
    show = True
    if request.method == 'POST':
        uif = UserInfoForm(data=request.POST)
        current_user = request.user

        if uif.is_valid():
            unsaved = uif.save(commit=False)
            """
            assign the current logged in user's object to the UserInfoForm's
            User field(which has one to one relationship with the User model)
            """
            unsaved.user = current_user
            unsaved.save()
            # new code
            weight = int(float(request.POST['weight']))
            height = int(float(request.POST['height']))
            gender = request.POST['gender']
            goal = request.POST['goal']
            dob = request.POST['date_of_birth']
            #print(dob)

            today = date.today()
            age = (int(today.year) - 1) - int(dob[0:4])
            lifestyle = request.POST['lifestyle']
            profession = request.POST['profession']
            userid = request.user.id
            testxl = openpyxl.load_workbook("test.xlsx")
            test_sheet = testxl.get_sheet_by_name("Sheet1")
            # new code to enter data into test file
            test_sheet.append([age, gender, weight, height, goal, lifestyle, profession,'NA', userid])
            #print(test_sheet.max_row)
            print("**********Saving user info from views.py to test.xlsx file.")
            testxl.save("test.xlsx")
            print("**********Saved.")

            print("**********Generating minimum calorie intake")
            ###########################################################################
            #Calculating BMR and Calorie intake                                       #
            #Men (BMR)   : 10 x weight (kg) + 6.25 x height (cm) – 5 x age (y) + 5    #
            #Women (BMR) : 10 x weight (kg) + 6.25 x height (cm) – 5 x age (y) – 161. #
            #                                                                         #
            #Calorie intake = BMR * Activity Factor                                   #
            #                                                                         #
            #Activity Factors:                                                        #
            #Sedentary = BMR X 1.2 (little or no exercise, desk job)                  #
            #Lightly active = BMR X 1.375 (light exercise or sports 1-3 days/wk)      #
            #Mod. active = BMR X 1.55 (moderate exercise or sports 3-5 days/wk)       #
            #Very active = BMR X 1.725 (hard exercise or sports 6-7 days/wk)          #
            #Extr. Active = BMR X 1.9 (hard daily exercise or sports & physical labor #
            #                           job or 2 X day training, football camp, etc.) #
            ###########################################################################

            if (gender == "Male"):
                BMR = 10*weight + 6.25*height - 5*age + 5
            elif (gender == 'Female'):
                BMR = 10*weight + 6.25*height - 5*age - 161

            if (lifestyle == "Sedentary"):
                factor = 1.2
            elif (lifestyle == "Lightly active"):
                factor = 1.375
            elif (lifestyle == "Moderately active"):
                factor = 1.55
            elif (lifestyle == "Very active"):
                factor = 1.725
            elif (lifestyle == "Extremely active"):
                factor = 1.9

            calorieintake = BMR * factor
            print("Gender: " + str(gender) + " | BMR: " + str(BMR) + " | factor: " + str(factor) + " | calorieintake: " + str(calorieintake))
            print("**********Generated!")

            print("**********Calling genPlan.py script.")
            genPlan.generate(request.user.id, BMR, calorieintake)
            # end of new code
            return HttpResponseRedirect(reverse('index'))
        else:
            uiform_error = uif.errors
    else:
        uif = UserInfoForm()
        # check if user has already submitted the form
        if UserDetails.objects.filter(user_id=request.user.id).exists():
            show = False
    return render(request, 'userInfoFormTemplate.html', {'uif': uif, 'show': show})

@login_required
def user_profile(request, pk):
    try:
        uif = UserDetails.objects.get(user_id=request.user.id)
    except UserDetails.DoesNotExist:
        return render(request, 'profile.html')
    thePlan = uif.dietPlan
    #print(type(uif.dietPlan))
    if feedback.objects.filter(user_id = request.user.id).exists():
        disabledFeedbackField = True
    else:
        disabledFeedbackField = False
    #print(uif)
    return render(request, 'profile.html', {'uif':uif,'plan':thePlan,
                                            'disable':disabledFeedbackField})
@login_required
def feedbackView(request):
    if request.method == 'POST':
        ff = feedbackForm(data = request.POST)
        current_user = request.user

        if ff.is_valid():

            new_weight = float(request.POST['weight'])
            uif = UserDetails.objects.get(user_id=request.user.id)

            #Check if feedback is positive or negative
            old_weight = uif.weight
            weight_difference = new_weight - old_weight #Ans +ve when gain weight and -ve when loose weight
            if uif.goal == 'Gain weight':
                if weight_difference >= 0.5:
                    feedback_is = 'Positive'
                else:
                    feedback_is = 'Negative'
            elif uif.goal == 'Loose weight':
                if weight_difference <= -0.5:
                    feedback_is = 'Positive'
                else:
                    feedback_is = 'Negative'
            elif uif.goal == 'Stay Fit':
                if weight_difference >= -0.5 and weight_difference <= 0.5:
                    feedback_is = 'Positive'
                else:
                    feedback_is = 'Negative'

            #Handle feedback is positive or negative
            feedbackpy.handlefeedback(feedback_is, request.user.pk)
            # print(uif.goal)
            # print(weight)

            unsaved = ff.save(commit=False)
            unsaved.user = current_user
            unsaved.save()

            #change the weight in main table
            import psycopg2
            try:
                conn = psycopg2.connect("dbname='virtualdietitian' user='postgres' host='localhost' password='password'")
                print("************connected to postgres db to update new weight")
            except:
                print ("************I am unable to connect to the postgres database to update new weight")
            cur = conn.cursor()
            user_id = current_user.id

            execstr = "UPDATE dietplan_userdetails SET \"weight\" = \'"+str(new_weight)+"\' WHERE user_id = "+str(user_id)
            cur.execute(execstr)
            try:
                conn.commit()
                print("************Commited new weight")
            except:
                print("************didn't commit new weight")


            return render(request, 'feedbackSubmitted.html')

    else:
        ff = feedbackForm()
        return render(request, 'feedback.html' ,{'ff':ff})
