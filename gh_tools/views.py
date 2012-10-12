from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from forms import LoginForm
from django.template import RequestContext

def about_page(request):
    return render_to_response('about.html', {}, RequestContext(request))

def contact_page(request):
    return render_to_response('contact.html', {}, RequestContext(request))

def home(request):
    return render_to_response('home.html', {}, RequestContext(request))

def logout_page(request):
    logout(request)    
    return HttpResponseRedirect('/home/')
    
def login_page(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login.html', {
                'error' : error,
                'form' : form,
        }, RequestContext(request))
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    error = u'account disabled'
                    return errorHandle(error)
            else:
                error = u'invalid login'
                return errorHandle(error)
        else:
            error = u'form is invalid'
            return errorHandle(error)
    else:
        form = LoginForm() # An unbound form
        return render_to_response('login.html', {
            'form': form,
        }, RequestContext(request))