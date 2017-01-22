import sys
import wikipedia
import treelib
from treelib import Node, Tree

query = sys.argv[1]
second_query = sys.argv[2]

print("query:" + query)
print("second query:" + second_query)

lang = 'ru'

print("lang: " + lang)

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
      try:
        page = wikipedia.page(link)
        for link in page.links:
          tree.create_node(link, parent = node.identifier)
        if second_query in page.links:
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

