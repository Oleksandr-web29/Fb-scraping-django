from django.shortcuts import render
import openai
import requests
from bs4 import BeautifulSoup

openai.api_key = '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'

def get_ingredients_from_link(link):
   models = openai.Model.list()
   print(models)
   response = openai.Completion.create(
      prompt=f"Access content from URL: {link}",
      model="voxscript-plugin-model" # Replace with the appropriate model name if different
   )
   return response.choices[0].text
   # r = requests.get(link)
   # print(r, 'ingredients')
   # soup = BeautifulSoup(r.content, 'html.parser')
   # ingredients = [item.text for item in soup.find_all('li')]
   # return ingredients

def categorize_ingredients(ingredients):
   # response = openai.Completion.create(
   #    prompt=f"Categorize the following ingredients into supermarket aisles: {ingredients}",
   #    model="text-davinci-002" # or the model you're using for this
   # )
   response = openai.Completion.create(
      prompt=f"Instacart, can you help me order these ingredients: {ingredients}",
      model="instacart-plugin-model" # Replace with the appropriate model name if different
    )
   return response.choices[0].text


def index(request):
   categorized = ""
   # models = openai.Model.list()
   # print(models, 'models')
   if request.method == "POST":
      print(request.POST, 'request.POST')
      if 'ingredients' in request.POST:
         ingredients = request.POST['ingredients']
         print(ingredients, 'ingredients')
         categorized = categorize_ingredients(ingredients)
      if 'recipe_link' in request.POST:
         recipe_link = request.POST['recipe_link']
         ingredients = get_ingredients_from_link(recipe_link)
         categorized = categorize_ingredients(ingredients)
      return render(request, 'index.html', {'categorized': categorized})
   else:
      return render(request, 'index.html')
