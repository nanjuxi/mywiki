from django.shortcuts import render
from . import util
import random
import markdown2
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect



class EntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    entries = util.list_entries()
    # rand1 = random.choice(entries)
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        # "random": rand1
    })

def entry(request, title):
    entries = util.list_entries()
    # rand = random.choice(entries)
    try:
        content = util.get_entry(title)
        output = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "content": output,
            "title": title
            # "random": rand
        })

    except TypeError:
        return render(request, "encyclopedia/error.html", {
            "random": rand
        })

def search(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    q = request.GET.get('q', '')
    results = []

    if (q == ''):
        return render(request, "encyclopedia/error.html")

    elif q in entries:
        return redirect('entry', title=q)

    else:
         for entry in entries:
             if q.upper() in entry.upper():
                 results.append(entry)

         return render(request, "encyclopedia/search.html", {
             "results": results,
             "q": q
         })

def NewEntry(request):
    return render(request, "encyclopedia/NewEntry.html",)

def NewPage(request):
    entries = util.list_entries()
    page_title = request.POST.get('PageTitle')
    if page_title in entries:
        return render(request, "encyclopedia/error.html")
    else:
        page_title = request.POST.get('PageTitle')
        content = request.POST.get('PageContent')
        util.save_entry(title=page_title, content=content)
        return render(request, "encyclopedia/NewEntry.html", {
            "page_title": page_title,
        })

def get(request, pagetitle):
        content = util.get_entry(pagetitle)
        output = markdown2.markdown(content)
        return render(request, "encyclopedia/get.html", {
            "content": content,
            "title": pagetitle
    })


def edit(request, title):
    content = request.POST.get('edit')
    util.save_entry(title=title, content=content)
    # entries = util.list_entries()
    # if title in entries:
    #     content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })


def rand(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    content = util.get_entry(rand)
    output = markdown2.markdown(content)
    return render(request, "encyclopedia/rand.html", {
        "rand": rand,
        "content": output
    })

