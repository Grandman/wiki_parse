from django.shortcuts import render

from .forms import WordsForm
import sys
import wikipedia
import treelib
from treelib import Node, Tree
from owlready import *
import subprocess
import psutil


def index(request):
    context = { "form" : WordsForm() }
    return render(request, 'main/index.html', context)

def parse(request):
    form = WordsForm(request.POST, request.FILES)
    if form.is_valid():
        query = form.cleaned_data['first_word']
        second_query = form.cleaned_data['last_word'].lower()
        max_level = form.cleaned_data['max_level']
        coefficient = form.cleaned_data['coefficient']
        file_path = '/code/static/test.owl'
        handle_uploaded_file(request.FILES['file'], file_path)

        lang = 'ru'
        process = subprocess.Popen(['python3', 'multi_thread_parse.py', query, second_query, str(max_level), str(coefficient)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        request.session['process'] = process.pid
        return render(request, 'main/parse.html', {'result': process })
def status(request):
  pid = request.session.get('process')
  status = psutil.pid_exists(pid)
  return render(request, 'main/status.html', {'result': status})

def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
