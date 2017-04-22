import sys
import wikipedia
import treelib
from treelib import Node, Tree
from owlready import *

query = sys.argv[1]
second_query = sys.argv[2].lower()

print("query:" + query)
print("second query:" + second_query)

lang = 'ru'

print("lang: " + lang)

# loading ontology

programming = get_ontology('file:///code/programming.owl')
programming.load()
classes = programming.classes
string_classes = [str(e) for e in classes]

print(programming.classes)

wikipedia.set_lang(lang)
page = wikipedia.page(query)
# print "content: " + page.content
tree = Tree()
# print '========li1nks========='
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
      # print(link.lower())
      # print(string_classes)
      try:
        page = wikipedia.page(link)
        # print(link.lower())
        for link in page.links:
          # print(link)
          tree.create_node(link.lower(), parent = node.identifier)
        if second_query in [s.lower() for s in page.links]:
            found = True
            print('FOUNDED')
            print('FOUNDED')
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
print(string)
#fo link in page.links:
#  page = wikipedia.page(link)
#  print "content: " + page.content

