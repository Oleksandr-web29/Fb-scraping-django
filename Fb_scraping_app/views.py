from django.shortcuts import render
from .scraper import FacebookScraper
import time
import json

def index(request):
   if request.method == "POST":
      print(request.POST, 'request.POST')
      email = request.POST['email']
      passw = request.POST['password']
      query = request.POST['query']
      
      bot = FacebookScraper()
      try:
         # login
         bot.login(email,passw)
         # sleep
         time.sleep(5)
         # navigate to desired query and obtain the posts
         prof_link = bot.get_page(query)
         bot.navigate(prof_link)
         story_links = []
         time.sleep(5)
         comz = bot.all_comments()
         for coms in comz:
               story_links.append("https://mbasic.facebook.com"+coms)
         
         all_comments = []
         # iterate through story_links
         for story in story_links:
               url, name, comment = bot.get_comments_links(story)
               all_comments.append({"url":url, "name":name, "comment": comment})
         return render(request, 'index.html', {"msg":"success"})
      except:
         return render(request, 'index.html', {"msg":"err"})
   else:
      return render(request, 'index.html')
