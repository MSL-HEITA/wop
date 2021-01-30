from django.shortcuts import render , redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User , auth
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import FormMixin
import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import cv2

# Create your views here.

def home(request):
    class BlogGrid(generic.ListView):
        queryset = Blog.objects.order_by('-date_posted')
        template_name = 'home-2.html'


    return render(request,'home-2.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email_adress']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password2 == password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is already taken.')
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'email is  already in use by another user.')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save();
                return redirect('dashboard/username')
        else:
            messages.info(request,'passwords do not match...')  
            return redirect('register')      
    else:    
        return render(request,'register.html', )


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard/username')
        else:
            messages.info(request, 'invalid login credentials')
            return redirect('login')
    else:            
        return render(request, 'login.html')    


@login_required
def userlogout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):


    return render(request, 'dashboard.html'  )


class BlogList(generic.ListView):
    queryset = Blog.objects.order_by('-date_posted')
    template_name = 'blog.html'
    paginate_by = 5
    
    
    


class BlogDetail( FormMixin ,generic.DetailView):
    model = Blog
    template_name = 'blog-details.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog_details/<int:id>/',kwargs={"pk": Blog.objects.get('pk')} )

    def get_context_data(self, **kwargs):
        context = super(BlogDetail, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={
            'post': self.object
        })
        context['comment_form'] = self.object.comments.filter(active=True)
        return context 

    def post(self, request, *args, **kwargs):
        form.instance.post = Post.objects.get(pk=self.kwargs.get("pk"))
        if not request.user.is_authenticated:
            messages.info(request,'You need to sign-in in order to take part!!!')
            return redirect('login')
        form = self.get_form()
        form.instance.post = Blog.objects.get(pk=self.kwargs.get("pk"))
        

        if form.is_valid():
            parent_obj = None
            # get parent comment id from hidden input
            try:
                # id integer e.g. 15
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            # if parent_id has been submitted get parent_obj id
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                # if parent object exist
                if parent_obj:
                    # create replay comment object
                    replay_comment = comment_form.save(commit=False)
                    # assign parent_obj to replay comment
                    replay_comment.parent = parent_obj

            post = form.save(commit=False)
            form.name = Profile()
            form.created_on = datetime.datetime.now()
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(BlogDetail, self).form_valid(form)           


    


class BlogGrid(generic.ListView):
    queryset = Blog.objects.order_by('-date_posted')
    template_name = 'blog-grid.html'

    
      


def candidate(request):
    return render(request, 'candidate.html')

def candidate_details(request):
    return render(request, 'candidate-details.html')

def checkout(request):
    return render(request, 'checkout.html')

def invoice(request):
    return render(request, 'invoice.html')

def payment_complete(request):
    return render(request, 'payment-complete.html')

def pricing(request):
    return render(request, 'pricing.html')

def dashboard_pricing(request):
    return render(request, 'dashboard-pricing.html')

def employer_pricing(request):
    return render(request, 'employer-dashboard-pricing.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request,'faq.html')

def dashboard_alert(request):
    return render(request, 'dashboard-alert.html')

def dashboard_applied(request):
    return render(request, 'dashboard-applied.html') 

def dashboard_bookmark(request):
    return render(request, 'dashboard-bookmark.html')

def dashboard_edit(request):
    return render(request, 'dashboard-edit-profile.html')

@login_required
def dashboard_message(request):
    
    return render(request, 'dashboard-message.html')

def edit_resume(request):
    return render(request, 'edit-resume.html')

def employer_dashboard(request):
    return render(request, 'employer-dashboard.html')


@login_required
def job_post(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) 
            post.author = Profile()
            post.date_posted = datetime.datetime.now()
            post.save()
            messages.info(request,' Your blog has been successfully post :) ')
            return redirect('job_post') 
    else:
        form = BlogForm()

    return render(request, 'post-job.html' ,{'form':form})

def employer_dashboard_post(request):
    return render(request, 'employer-dashboard-post-job.html')

def employer_dashboard_job(request):
    return render(request, 'employer-dashboard-manage-job.html') 

def employer_dashboard_candidate(request):
    return render(request, 'employer-dashboard-manage-candidate.html')

def employer_dashboard_edit(request):
    return render(request, 'employer-dashboard-edit-profile.html')

def employer_dashboard_message(request):
    return render(request, 'employer-dashboard-message.html')

def employer_details(request):
    return render(request, 'employer-details.html')

def employer_listing(request):
    return render(request, 'employer-listing.html')

def resume(request):
    return render(request, 'resume.html')
    
def add_resume(request):
    return render(request, 'add-resume.html')  
def about_us(request):
    return render(request, 'about-us.html')

def _404(request):
    return render(request, '404.html')

def how(request):
    return render(request, 'how-it-work.html')

def terms(request):
    return render(request, 'terms-and-condition.html')       

def job_detail(request):
    return render(request, 'job-details.html')

def job_listing(request):
    return render(request, 'job-listing.html')

def job_map(request):
    return render(request, 'job-listing-with-map.html')

def search(request, *args, **kwargs):
     
    pass


