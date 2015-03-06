'''
This script converts dowloaded html pages from the crawler to xml format so that it could be indexed by SOLR
Usage:
  python convert.py data_target output_directory
  data_target is the output directory of the crawler
'''
import sys
#from boilerpipe.extract import Extractor
from bs4 import BeautifulSoup
from os import walk
import urllib
import os.path
import re
import traceback

N=5000 #Number of pages per file
allfiles = "allfiles.txt"
TITLE = re.compile('<title>(.*?)</title>', re.IGNORECASE|re.DOTALL)

def decode_url(url):
  return urllib.unquote(url).replace("%2F", "/")

def check_html_content(html_content):
  #BeautifulSoup has a bug. If begining of the html content is <!doctype>,
  #it returns Segmentation Fault
  return "<!doctype html>\n" + html_content
  '''
  head = html_content[:100]
  if "<!doctype>" in head:
    html_content = html_content.replace("<!doctype>", "<!doctype html>", 1)
  elif "<!DOCTYPE>" in head:
    html_content = html_content.replace("<!DOCTYPE>", "<!doctype html>", 1)
  return html_content
  '''

def get_all_files(dirname):
    
    files = []
    if os.path.isfile(allfiles):
      with open(allfiles) as lines:
        for line in lines:
          files.append(line.strip("\n"))
    else:
      f = open(allfiles, "w")
      for [path, dirnames, filenames] in walk(dirname):
          for filename in filenames:
            f.write(path + "/" + filename + "\n")
            files.append(path + "/" + filename)
      f.close()
    return files

def encode_xml(value):
  value = value.replace("\"", "&quot;")
  value = value.replace("\'", "&apos;")
  value = value.replace("<", "&lt;")
  value = value.replace(">", "&gt;")
  value = value.replace("&", "&amp;")
  return value

def get_title(html_content):
  res = TITLE.search(html_content)
  if res:
    return res.group(1)
  else:
    return "None"
 
def convert(filename):
  '''
  Convert a html page into a xml-formatted string
  '''
  try:
    html_content = open(filename).read()
    #soup = BeautifulSoup(html_content) #by default, bs uses lxml but lxml causes segfault, html5lib is super slow.
    #soup = BeautifulSoup(html_content, "html5lib")
    #text = soup.get_text()
    #text = " ".join(text.split())
    '''
    title_tag = soup.title
    title = "None"
    if title_tag:
      title = title_tag.string
      if title == None:
        title = "None"
      else:
        title = encode_xml(title.encode('utf8'))
    '''
    title = get_title(html_content)
    #title = encode_xml(title.encode('utf8'))
    title = encode_xml(title)
    url = decode_url(filename.split("/")[-1])
    url = encode_xml(url)
    xml = '<doc>\n' + \
          '  <field name=\"id\">' + url + '</field>\n' + \
          '  <field name=\"url\">' + url + '</field>\n' + \
          '  <field name=\"name\">' + title + '</field>\n' + \
          '</doc>\n'
    #        '    <field name = text>' + text + '</field>\n' + \
    return xml
  except:
    traceback.print_exc(file=sys.stdout)
    print filename
    return None

def convert_all(input_dir, output_dir):
  filenames = get_all_files(input_dir)
  print "Done reading directories " + str(len(filenames)) + " files"
  count = 0
  docs = []
  for filename in filenames:
    count += 1
    doc = convert(filename)
    if doc:
      docs.append(doc + "\n")
    if (count % N) == 0:
      out = open(output_dir + "/" + str(count) + '.xml', 'w')    
      data = ''.join(docs)
      out.write('<add>\n' + data + '\n</add>')
      out.close()
      docs = []
  out = open(output_dir + "/" + str(count) + '.xml', 'w')
  data = ''.join(docs)
  out.write('<add>\n' + data + '\n</add>')
  out.close()

def main(argv):
  input_dir = argv[0]
  output_dir = argv[1]
  convert_all(input_dir, output_dir)

if __name__=="__main__":
  main(sys.argv[1:])
