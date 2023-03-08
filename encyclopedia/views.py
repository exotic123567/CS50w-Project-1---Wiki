from django.shortcuts import render

from . import util
import markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdowner = markdown.Markdown()
    entryPage = util.get_entry(title)
    if entryPage is None:
        return render(request, "encyclopedia/nonExistingEntry.html", {
            "entryTitle": title
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entryPage),
            "entryTitle": entry
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        markdowner = markdown.Markdown()
        searchPage = util.get_entry(entry_search)
        if searchPage is not None:
            return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(searchPage),
            "entryTitle": searchPage
            })
        else:
            contentList = util.list_entries()
            ls=[]
            for i in range(len(contentList)):
                if entry_search.lower() in contentList[i].lower():
                    ls.append(contentList[i])
            return render(request, "encyclopedia/search.html", {
            "searchTitle": entry_search,
            "searchList": ls,
            "lenList": len(ls)
            })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        ls=util.list_entries()
        for i in range(len(ls)):
            if title.lower() == ls[i].lower():
                return render(request, "encyclopedia/alreadyExists.html", {
                    "newtitle": title
                })
    util.save_entry(title, content)
    markdowner = markdown.Markdown()
    entryPage = util.get_entry(title)
    html_content=markdowner.convert(entryPage)
    return render(request, "encyclopedia/entry.html", {
        "entryTitle": title,
        "entry": html_content
    })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title = request.POST['new_title']
        content = request.POST['content']
        util.save_entry(title, content)
        markdowner = markdown.Markdown()
        entryPage = util.get_entry(title)
        html_content=markdowner.convert(entryPage)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def randomreq(request):
    if request.method == "GET":
        ls = util.list_entries()
        selector = random.randint(0,len(ls))
        selected = ls[selector]
        markdowner = markdown.Markdown()
        entryPage = util.get_entry(selected)
        html_content=markdowner.convert(entryPage)
        return render(request, "encyclopedia/entry.html", {
            "entryTitle": selected,
            "entry": html_content
        })