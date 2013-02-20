from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from forms import LoginForm, AccountForm, ArticlePackForm, BlogForm
from models import ArticlePackModel, ArticleModel, NicheModel, BlogModel
from functools import wraps
import json
import tarfile

from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST, require_GET

from scripts import GetPageRank, bing_grab


def json_view(func):
    """
    decorator that removes some of the boilerplace from views that
    are supposed to return JSON

    :param int indent: number of spaces to indent output
    :param str mimetype: content type of the response (default text/plain)
    :returns: HttpResponse containing JSON representation of view output
    """
    @wraps(func)
    def _inner(*args, **kwargs):
        ret = func(*args, **kwargs)

        if isinstance(ret, HttpResponse):
            return ret

        status_code = 200

        if isinstance(ret, tuple) and len(ret) == 2:
            ret, status_code = ret

        return HttpResponse(json.dumps(ret, indent=4), mimetype='text/plain', status=status_code)

    return _inner

def about_page(request):
    return render_to_response('about.html', {}, RequestContext(request))

def contact_page(request):
    return render_to_response('contact.html', {}, RequestContext(request))

def home(request):
    return render_to_response('home.html', {}, RequestContext(request))

def logout_page(request):
    logout(request)    
    return HttpResponseRedirect('/home/')


@json_view
def account_page(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AccountForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            cleaned_data = form.cleaned_data
            username = cleaned_data['username']
            first_name = cleaned_data['first_name']
            last_name = cleaned_data['last_name']
            email = cleaned_data['email']
            password_old = cleaned_data['password_old']
            password_new = cleaned_data['password_new']
            if authenticate(username=username, password=password_old):
                u = User.objects.get(username__exact=username)
                if password_new > '':
                    u.set_password(password_new)
                if first_name > '':
                    u.first_name = first_name
                if last_name > '':
                    u.last_name = last_name   
                if email > '':
                    u.email = email
                u.save()
                return {'status':'success'}
            else:
                return {'status':'error', 'message':'Wrong password!'}
        else:
            return {'status':'error', 'message':'Invalid form!'}
    else:
        form = AccountForm() 
        return render_to_response('account.html', {'form': form,}, context_instance=RequestContext(request))


def login_page(request):
    def errorHandle(error):
        form = LoginForm()
        return render_to_response('login.html', {'error' : error,'form' : form,}, context_instance=RequestContext(request))
    if request.method == 'POST': 
        form = LoginForm(request.POST) 
        if form.is_valid(): 
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
        return render_to_response('login.html', {'form': form,}, context_instance=RequestContext(request))
    
def upload_article(request):
    if request.method == 'POST':
        form = ArticlePackForm(request.POST, request.FILES)
        if form.is_valid():
            niche = NicheModel.objects.get(id=int(request.POST['niche']))
            newpack = ArticlePackModel(packfile = request.FILES['packfile'], 
                                       description = request.POST['description'], 
                                       processed = False, 
                                       niche=niche)
            newpack.save()
            return HttpResponseRedirect('/upload_article/')
    else:
        form = ArticlePackForm()

    packs = ArticlePackModel.objects.all()

    return render_to_response(
        'upload_article.html',
        {'packs': packs, 'form': form},
        context_instance=RequestContext(request))

def manage_articles(request):
    articles = ArticleModel.objects.all()
    for article in articles:
        article.text = "%s..."%(article.text[:600])
    return render_to_response('manage_articles.html',
        {'articles': articles}, context_instance=RequestContext(request))


def manage_blogs(request, blog_id=None):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            niche = NicheModel.objects.get(id=int(request.POST['niche']))
            newblog = BlogModel(address=request.POST['address'],
                                user=request.POST['user'],
                                password=request.POST['password'],
                                niche=niche)
            newblog.save()
            return HttpResponseRedirect('/manage_blogs/')
    else:
        initial_data = None
        if blog_id:
            try:
                edit_blog = BlogModel.objects.get(pk=blog_id)
                initial_data = edit_blog.get_data()
            except Exception:
                pass
        form = BlogForm(initial_data)
        blogs = BlogModel.objects.all()
        return render_to_response('manage_blogs.html',
            {'blogs': blogs, 'form': form, 'blog_id': blog_id}, context_instance=RequestContext(request))


@json_view
def post_article(request):
    if request.method == 'POST':
        print('posted')
    else:
        dirs = ['PortalArticole.ro', 'EArticole.com']
        blogs = []
        blog_list = BlogModel.objects.all()
        for blog in blog_list:
            blogs.append({'id': blog.pk, 'value': blog.address})
        
        return render_to_response('post_article.html',
            {'blogs': json.dumps(blogs), 'dirs': json.dumps(dirs)}, context_instance=RequestContext(request))


@json_view
def article_list(request, blog_id=None):
    ret = {'status': 'error', "data": []}
    if blog_id:
        try:
            blog = BlogModel.objects.get(pk=blog_id)
            articles = ArticleModel.objects.filter(niche=blog.niche)
            for article in articles:
                ret["data"].append({'id': article.id, 'title': article.title, 
                                    'text': article.text})
            ret['status'] = 'ok';
        except Exception, e:
            print(e)
            pass
    
    return ret


@require_GET
@login_required
def remove_blog(request, blog_id):
    try:
        blog = BlogModel.objects.get(pk=blog_id)
        blog.delete()
    except Exception:
        pass
    return HttpResponseRedirect('/manage_blogs/')


@json_view
def process_pack(request, pack_id=None):
    if pack_id:
        pack = ArticlePackModel.objects.get(id = pack_id)
        if pack:
            try:
                tar = tarfile.open(pack.packfile.path, 'r:tar')
                members = tar.getmembers()
                for member in members:
                    if member.isfile and member.size > 0 :
                        title = member.name
                        while '/' in title:
                            title = title[title.index('/')+1:]
                        if '.' in title:
                            title = title[0:title.index('.')]
                        newarticle = ArticleModel(title = title, text = tar.extractfile(member.name).read(), niche=pack.niche)
                        newarticle.save()
                pack.processed = True
                pack.save()
                return {'status':'success'}
            except Exception:
                return {'status':'error'}
    return {'status': 'error'}


def pr_check(request):
    print(request.method)
    if request.method == 'POST':
        url = request.POST.get('urlToCheck', None)
        if url:
            page_rank = GetPageRank(url)
            return render_to_response('pr_check.html',
            {'page_rank': page_rank, 'target': url}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/pr_check/')
    else:
        return render_to_response('pr_check.html',
            {}, context_instance=RequestContext(request))

def bing_grabber(request):
    print(request.method)
    if request.method == 'POST':
        subject = request.POST.get('subjectToGrab', None)
        if subject:
            data = bing_grab(subject)
            return render_to_response('bing_grab.html',
            {'data': data, 'subject': subject}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/bing_grab/')
    else:
        return render_to_response('bing_grab.html',
            {}, context_instance=RequestContext(request))