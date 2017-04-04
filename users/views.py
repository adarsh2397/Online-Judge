from django.shortcuts import render, redirect
from users.forms import UserForm, AdditionalDetails
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from users.models import UserDetails
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.shortcuts import get_object_or_404
from problems.models import Runs
# Create your views here.

IMAGE_FILE_TYPES = ['jpg','png']

class UserFormView(View):
    form_class = UserForm
    template_name = 'users/registration_form.html'

    #display empty form (default)
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form' : form,})

    def post(self,request):
        form = self.form_class(request.POST)

        if request.POST["username"] == "":
            return render(request,self.template_name,{'form':form,'error_message' : 'Firstname is required'})

        if form.is_valid():
            user = form.save(commit=False)

            #cleaned data

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)

            user.save()


            #returns User objects if the credentials are correct
            user = authenticate(username=username,password=password)

            if user is not None:

                if user.is_active:

                    login(request, user)
                    # you can access the User Details using request.Username ...etc
                    return redirect('users:additional')

        return render(request, self.template_name, {'form': form, })


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('problems:home')
            else:
                return render(request, 'users/login.html', {'error_message': "Your account has been disabled"})
        else:
            return render(request, 'users/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'users/login.html')

def logout_user(request):
    logout(request)
    return redirect('users:login')

class AdditionalDetailsView(View):
    form_class = AdditionalDetails
    template_name = 'users/additional_form.html'

    #display empty form (default)
    def get(self,request):
        if request.user.is_authenticated:
            try:
                UserDetails.objects.get(user=request.user)
                return redirect('problems:home')
            except UserDetails.DoesNotExist:
                form = self.form_class(None)
                return render(request, self.template_name, {'form': form, })
        else:
            return redirect('users:login')

    def post(self,request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                user_details = form.save(commit=False)
                user_details.user = request.user
                user_details.profile_update = True
                user_details.save()

                context = {'user' : request.user}

                return redirect('problems:home')
            else:
                return render(request,'users/additional_form.html',{'form' : form})


def my_view(request):
    user_details = request.user.userdetails

    if request.method == "POST":
        form = AdditionalDetails(request.POST, request.FILES, instance=user_details)

        if form.is_valid():
            user_details = form.save(commit=False)
            user_details.user = request.user
            user_details.profile_update = True
            user_details.save()

            return render(request,'users/additional_form.html',{'form':form})

    else:
        form = AdditionalDetails(instance=user_details)

    return render(request,'users/additional_form.html',{'form':form})

def profile_display(request,user_id):
    details = {}
    user = User.objects.get(pk=user_id)
    runs = Runs.objects.all().filter(user=request.user)
    details['submissions'] = len(runs)
    context = {'details' : details, 'user' : user}
    return render(request,'users/profile_display.html',context)


