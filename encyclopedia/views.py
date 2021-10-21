from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from django.contrib import messages
from markdown2 import Markdown
import random

markdowner = Markdown()

# Show entries list
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Add a new page:
def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if not title or not content:
            messages.add_message(request, messages.INFO, 'Must input CONTENT and TITLE.')
        
        elif util.get_entry(title) != None:
            messages.add_message(request, messages.INFO, 'Encyclopedia Entry have already existed. Find and edit content.')
        
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", { 
                "content": markdowner.convert(content),
                "name": title
            })


    return render(request, "encyclopedia/newpage.html")

# Display entry content
def entry(request, name):
    
    # Check path of entry
    if util.get_entry(name) == None:
        messages.add_message(request, messages.INFO, 'REQUESTED PAGE WAS NOT FOUND.')
        return render(request, "encyclopedia/error.html", {
            "messages": messages
        })
    else:
        content = markdowner.convert(util.get_entry(name))

        return render(request, "encyclopedia/entry.html", { 
            "content": content,
            "name": name
        })

# Edit entry
def edit(request, name):

    print(f"edit/{name}")
    content = util.get_entry(name)

    # Check if method is POST
    if request.method == "POST":

        content = request.POST.get("content")
        
        if not content:
            messages.add_message(request, messages.INFO, 'Must input CONTENT')

        else:
            util.save_entry(name, content)

            # Redirect user to home page
            return render(request, "encyclopedia/entry.html", {
                "name": name,
                "content": content
            })

    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "content": content
    })

# Search for entry
def search(request):

    # Check if method is POST
    if request.method == "POST":
        src = request.POST.get("q")

        # Convert search content to lowercase with no spaces
        search = src.lower().replace(" ","")

        # If submitted content is blank
        if not search:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

        else:
            entries = util.list_entries()
            results = []

            # Loop through entries list
            for item in entries:

                # If search content == entry title, render entry page
                if search == item.lower().replace(" ",""):
                    content = markdowner.convert(util.get_entry(item))
                    
                    return render(request, "encyclopedia/entry.html", { 
                        "content": content,
                        "name": item
                    })

                # If not, add title similar entries to new list to display
                elif search in item.lower().replace(" ",""):

                    results.append(item)

            return render(request, "encyclopedia/search.html", {
                "results": results
            })

# Access random entry page
def randompage(request):

    entries = util.list_entries()

    title = random.choice(entries)

    content = markdowner.convert(util.get_entry(title))

    return render(request, "encyclopedia/entry.html", { 
        "content": content,
        "name": title
    })


