# views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import File, Directory, CompilationOption
from .forms import CompilationOptionForm, FileForm, DirectoryForm, FileSection
from django.shortcuts import redirect
from django import forms

from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

def file_content(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.divide_into_sections()  # ensure the file is divided into sections
    file_sections = FileSection.objects.filter(file=file)
    sections = [
        {
            'id': section.id,
            'content': section.content,
            'section_type': section.section_type.type,
            'section_status': section.section_status.status,
            'status_data': section.status_data.data
        }
        for section in file_sections
    ]
    return JsonResponse({
        'file_content': file.content,
        'compiled_content': file.compiled_content,
        'sections': sections
    })



def home(request):
    root_directories = Directory.objects.filter(parent_directory__isnull=True)
    compilation_options = get_object_or_404(CompilationOption)
    return render(request, 'core/home.html', {'root_directories': root_directories, 'compilation_options': compilation_options, 'file_id': 1})

@login_required
def add_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            return redirect('home')
        else:
            return render(request, 'core/add_file.html', {'form': form})
    else:
        form = FileForm()
        return render(request, 'core/add_file.html', {'form': form})


@login_required    
def add_directory(request):
    if request.method == 'POST':
        form = DirectoryForm(request.POST)
        if form.is_valid():
            # create a new `Directory` but don't save it to the db yet
            directory = form.save(commit=False)
            # set the owner to the currently logged in user
            directory.owner = request.user
            # now save it to the db
            directory.save()
            return redirect('home')
    else:
        form = DirectoryForm()
        return render(request, 'core/add_directory.html', {'form': form})    
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CompilationOption

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import subprocess
import os
import tempfile
import os
import tempfile
import subprocess
from django.shortcuts import get_object_or_404, HttpResponse
from .models import File

def compile_and_update(request, file_id):
    file = get_object_or_404(File, id=file_id)

    compilation_option = get_object_or_404(CompilationOption, id=1)

    with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp:
        temp.write(file.content.encode())
        temp_filename = temp.name

    compiled_file_name = f'{temp_filename.rsplit(".", 1)[0]}.asm'

    options = f'--std-{compilation_option.standard.lower()} --{compilation_option.optimization} -m{compilation_option.processor.lower()}'
    print(options)

    command = f'sdcc -S {temp_filename} -o {compiled_file_name}'
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()

    if stderr:
        os.unlink(temp_filename)  # delete the temp file
        if os.path.exists(compiled_file_name):
            os.unlink(compiled_file_name)  # delete the compiled file if it exists
        return HttpResponse(f'Compilation error: {stderr}')

    if os.path.exists(compiled_file_name):
        with open(compiled_file_name, 'r') as f:
            file.compiled_content = f.read()
            file.save()

    os.unlink(temp_filename)  # delete the temp file
    if os.path.exists(compiled_file_name):
        os.unlink(compiled_file_name)  # delete the compiled file

    #return HttpResponse('Compilation and update successful.')
    return JsonResponse({'compiled_content': file.compiled_content})

@csrf_exempt
def update_standard(request):
    if request.method == 'POST':
        standard = request.POST.get('standard')
        # Assuming you have only one CompilationOption object.
        # Adjust accordingly if you have more.
        option = CompilationOption.objects.first()
        option.standard = standard
        option.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})
    
@csrf_exempt
def update_optimization(request):
    if request.method == 'POST':
        optimization = request.POST.get('optimization')
        # Assuming you have only one CompilationOption object.
        # Adjust accordingly if you have more.
        option = CompilationOption.objects.first()
        option.optimization = optimization
        option.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

@csrf_exempt
def update_processor(request):
    if request.method == 'POST':
        processor = request.POST.get('processor')
        # Assuming you have only one CompilationOption object.
        # Adjust accordingly if you have more.
        option = CompilationOption.objects.first()
        option.processor = processor
        option.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})


def update_compilation_options(request, file_id):
    compilation_option = get_object_or_404(CompilationOption)
    if request.method == "POST":
        form = CompilationOptionForm(request.POST, instance=compilation_option)
        if form.is_valid():
            form.save()
            #return redirect(request.META.get('HTTP_REFERER', '/'))
            #next = request.POST.get('next', '/')
            #return redirect(next)
            return redirect('file_content', file_id)
    else:
        form = CompilationOptionForm(instance=compilation_option)
    return render(request, 'core/update_compilation_options.html', {'form': form})

from django.shortcuts import redirect
from .models import File, Directory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def delete_file_view(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        file = File.objects.get(id=file_id)
        if request.user == file.owner:
            file.is_available = False
            file.save()
        return redirect('home')

    return render(request, 'core/delete_file.html')

@login_required
def delete_directory_view(request):
    if request.method == 'POST':
        directory_id = request.POST.get('directory_id')
        directory = Directory.objects.get(id=directory_id)
        for file in directory.file_set.all():
            file.is_available = False
            file.save()
        if request.user == directory.owner:
            directory.is_available = False
            directory.save()
        return redirect('home')

    return render(request, 'core/delete_directory.html')

from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from .forms import SignUpForm

class MyLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))
    
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'core/signup.html'


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import File

@csrf_exempt
def update_file_content(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        file_content = request.POST.get('file_content')
        print("view File ID:", file_id)
        print("view File Content:", file_content)
        file = File.objects.get(id=file_id)
        file.content = file_content
        file.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})   
