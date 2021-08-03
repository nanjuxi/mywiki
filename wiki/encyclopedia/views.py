from django.shortcuts import render
from . import util
import random
import markdown2
from django import forms
from django.urls import reverse
from django.contrib import messages

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
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
    return  render(request, "encyclopedia/index.html", {
        "random": rand
    })

    post_list = Post.objects.fliter(title_icontains = q)
    return render(request, 'encyclopedia/entry.html', {
        'post_list': post_list
    })




