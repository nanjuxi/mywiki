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
    if q in entries:
        return redirect('entry', title=q)

    for entry in entries:
        if q in entry:
            results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": results,
            })

        else:
            return render(request, "encyclopedia/error.html")




