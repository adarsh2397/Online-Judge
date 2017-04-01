from django.shortcuts import render, redirect
from users.forms import UserForm
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
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
                    return redirect('problems:home')

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

