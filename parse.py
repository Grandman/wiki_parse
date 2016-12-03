import sys
import wikipedia

query = sys.argv[1]

print "query:" + query

lang = 'ru'

print "lang: " + lang

wikipedia.set_lang(lang)

page = wikipedia.page(query)

print "content: " + page.content

print '========links========='
for link in page.links:
  print link

for link in page.links:
  page = wikipedia.page(link)
  print "content: " + page.content

