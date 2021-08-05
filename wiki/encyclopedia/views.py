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
    rand = random.choice(entries)
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "random": rand
    })

def entry(request, title):
    entries = util.list_entries()
    rand = random.choice(entries)
    try:
        content = util.get_entry(title)
        output = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": output,
            "random": rand
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
    entries = util.list_entries()
    rand = random.choice(entries)

    if request.method == "POST":
        form = EntryForm(request.POST)
        title = request.POST('title')

        if title in entries:
            return render(request, "encyclopedia/NewEntry.html", {
                "message": "Page already exists.",
                "form": EntryForm(),
                "random": rand
            })

        else:
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]

                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=(title,)))


            else:
                title = request.POST['title']
                content = request.POST['content']
                if not title:
                    return render(request, "encyclopedia/create.html", {
                        "no_title": "Title is required.",
                        "form": EntryForm(),
                        "random": rand
                    })

                elif not content:
                    return render(request, "encyclopedia/create.html", {
                        "no_title": "Content is required.",
                        "form": EntryForm(),
                        "random": rand
                    })










