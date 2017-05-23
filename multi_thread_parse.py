from threading import Thread
import sys
import queue
import time
import wikipedia
from py2neo import authenticate, Graph, Node, Relationship
class NodeElement:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

concurrent = 100


authenticate("neo4j:7474", "neo4j", "123")
graph = Graph("http://neo4j:7474/db/data/")

lang = 'ru'
wikipedia.set_lang(lang)
query = 'Игра'
page = wikipedia.page(query)
tx = graph.begin()
a = Node("Notion", name=query)
node = tx.create(a)
tx.commit()
array = page.links

def doWork():
    itera = 0
    while True:
        try:
            node = q.get_nowait()
            # print(title)
            a = graph.find_one(label="Notion", property_key='name', property_value=node.parent)
            b = graph.find_one(label="Notion", property_key='name', property_value=node.name)
            tx = graph.begin()
            if b is None:
                b = Node("Notion", name=node.name)
                tx.create(b)
            ab = Relationship(a, "depends", b)
            tx.create(ab)
            tx.commit()
            page1 = wikipedia.page(node.name)
            links = page1.links
            q.task_done()
            for name in links:
                q.put_nowait(NodeElement(name, node.name))
            itera += 1
            print(itera)
        except wikipedia.exceptions.WikipediaException as err:
           #  print("Oops!")
           #  print(err)
            pass
        except queue.Empty:
            time.sleep(1)
            pass

q = queue.Queue(100000000)
for url in array:
    q.put(NodeElement(url, query))
for i in range(concurrent):
    t = Thread(target=doWork)
    t.start()


