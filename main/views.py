from django.shortcuts import render

from .forms import WordsForm
import sys
import wikipedia
import treelib
from treelib import Node, Tree
from owlready import *


def index(request):
    context = { "form" : WordsForm() }
    return render(request, 'main/index.html', context)

def parse(request):
    form = WordsForm(request.POST, request.FILES)
    if form.is_valid():
        query = form.cleaned_data['first_word']
        second_query = form.cleaned_data['last_word'].lower()
        file_path = '/code/test.owl'
        handle_uploaded_file(request.FILES['file'], file_path)

        lang = 'ru'

        # loading ontology

        programming = get_ontology('file://' + file_path)
        programming.load()
        classes = programming.classes
        string_classes = [str(e) for e in classes]

        wikipedia.set_lang(lang)
        page = wikipedia.page(query)
        tree = Tree()
        # print '========links========='
        found = False
        tmp_links = page.links
        main_node = tree.create_node(query)
        depth = 0
        while found == False:
            nodes = list(filter(lambda x: tree.depth(x) == depth, tree.all_nodes()))
            print("Total at level " + str(depth) + ": " + str(len(nodes)))
            for node in nodes:
              link = node.tag
              if not any(link.replace(" ", "_").lower() == e for e in string_classes):
                continue
              try:
                page = wikipedia.page(link)
                for link in page.links:
                  tree.create_node(link.lower(), parent = node.identifier)
                if second_query in [s.lower() for s in page.links]:
                    found = True
                    print('FOUNDED')
                    break
              except wikipedia.exceptions.WikipediaException as err:
                print("Oops!")
                print(err)
            depth += 1
        tree.show()
        nodes = list(filter(lambda x: x.tag == second_query, list(tree.all_nodes())))
        node = nodes[0]
        string = node.tag
        while tree.parent(node.identifier) != None:
          node = tree.parent(node.identifier)
          string += " => " + node.tag
        result = string

        return render(request, 'main/parse.html', {'result': result })

def handle_uploaded_file(f, path):
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
