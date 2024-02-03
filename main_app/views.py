from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def subjects_index(request):
    pass

def subjects_detail(request):
    pass

def subjects_create(request):
    pass

def subjects_update(request):
    pass

def subjects_delete(request):
    pass
