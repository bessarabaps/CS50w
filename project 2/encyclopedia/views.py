from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render,redirect
from .forms import *
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def articles(request,name):
    entry = util.get_entry(name)
    if entry:
        return render(request, "encyclopedia/articles.html", {
            "name": name,
            "entry": entry
        })
    else:
        return render(request, "encyclopedia/EROR.html", {
                "text": "This page does not exist"
            })
    
def search(request):
    query = request.POST.get("q")
    entry = util.get_entry(query)
    if entry:
        return render(request, "encyclopedia/articles.html", {
            "name": query,
            "entry": entry
        })
    else:
        list_articles = util.list_entries()
        entries = []
        for item in list_articles:
            a = query.lower()
            b = item.lower()
            s = b.find(a)
            if s != -1:
                entries.append(item)
        if len(entries) > 0:
            return render(request, "encyclopedia/search.html", {
                "entries": entries
            }) 
        else:
            return render(request, "encyclopedia/EROR.html", {
                "text": "This page does not exist"
            })
        
def create(request):
    if request.method == "POST":
        userform = CreateNewPage(request.POST) 
        if userform.is_valid():
            title = userform.cleaned_data["title"]
            content = userform.cleaned_data["content"]
            entry = util.get_entry(title)
            if entry:
                return render(request, "encyclopedia/EROR.html", {
                    "text": "The page already exists"
                })
            else:
                try:
                    with open(f"entries/{title}.md",'w+') as f:
                        f.write(content)
                        f.close
                except FileNotFoundError:
                    return render(request, "encyclopedia/EROR.html", {
                    "text": "File create ERROR"
                })
                entry = util.get_entry(title)
                return render(request, "encyclopedia/articles.html", {
                    "name": title,
                    "entry": entry
                })

    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreateNewPage
        })

def edit(request, name):
     if request.method == "POST":
        userform = EditPage(request.POST)
        if userform.is_valid():
            content = userform.cleaned_data["content"]
            util.save_entry(name, content)
            entry = util.get_entry(name)
            return render(request, "encyclopedia/articles.html", {
                "name": name,
                "entry": entry
            })
        
     else:
         old_content = util.get_entry(name)
         
         return render(request, "encyclopedia/edit.html", {
            "form": EditPage({
                "content": old_content
            })
        })
     
def random_page(request):
    return redirect(f"/{random.choice(util.list_entries())}")
    

         
         

