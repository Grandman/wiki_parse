from threading import Thread
import sys
import queue
import time
import wikipedia
from py2neo import authenticate, Graph, Node, Relationship
import nltk
import string
import pymorphy2
from nltk.corpus import stopwords
from owlready import *

class NodeElement:
    def __init__(self, name, parent, level):
        self.name = name
        self.parent = parent
        self.level = level

def normalize_words(text):
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if ( i not in string.punctuation )]

    #deleting stop_words
    stop_words = stopwords.words('russian')
    stop_words.extend(['что', 'это', 'так', 'вот', 'быть', 'как', 'в', '—', 'к', 'на'])

    tokens = [i for i in tokens if ( i not in stop_words )]

    tokens = [i.replace("«", "").replace("»", "") for i in tokens]

    morph = pymorphy2.MorphAnalyzer()
    normalized_words = list(set(map(lambda x: morph.normal_forms(x)[0], tokens)))

    return normalized_words

concurrent = 100


authenticate("neo4j:7474", "neo4j", "123")
graph = Graph("http://neo4j:7474/db/data/")

programming = get_ontology('file:///code/programming.owl')
programming.load()

classes = programming.classes
string_classes = [str(e) for e in classes]
lang = 'ru'
wikipedia.set_lang(lang)
query = 'Программирование'
page = wikipedia.page(query)
tx = graph.begin()
a = Node("Notion", name=query)
node = tx.create(a)
tx.commit()
visited_links = []
array = page.links

def doWork():
    itera = 0
    global visited_links
    while True:
        try:
            node = q.get_nowait()
            # print(title)
            if node.name in visited_links:
               #  print('already visited')
               # a = graph.find_one(label="Notion", property_key='name', property_value=node.parent)
               # b = graph.find_one(label="Notion", property_key='name', property_value=node.name)
               # if b is None:
              #      q.task_done()
              #      continue
              #  tx = graph.begin()
              #  ab = Relationship(a, "depends", b)
              #  tx.create(ab)
              #  tx.commit()
                q.task_done()
                continue

            page = wikipedia.page(node.name)
            #######
            words = normalize_words(page.content)
            passed = False
            for c in classes:
              # print(c)
              instances = list(map(str, c.instances()))
              arr = set(words) & set(instances)
              # print("length first" + str(len(instances)))
              # print("length second" + str(len(arr)))
              if (len(arr) > 0 and len(arr) / len(instances) > 0.4):
                  passed = True
            # print(words)
            #####
            links = page.links
            q.task_done()
            print("Level: " + str(node.level))
            if passed == True:
                ##########
                a = graph.find_one(label="Notion", property_key='name', property_value=node.parent)
                b = graph.find_one(label="Notion", property_key='name', property_value=node.name)
                tx = graph.begin()
                if b is None:
                    b = Node("Notion", name=node.name)
                    tx.create(b)
                ab = Relationship(a, "depends", b)
                tx.create(ab)
                tx.commit()
                ##########

                for name in links:
                    q.put_nowait(NodeElement(name, node.name, node.level + 1))
                visited_links.extend(links)
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
    q.put(NodeElement(url, query, 1))
for i in range(concurrent):
    t = Thread(target=doWork)
    t.start()




