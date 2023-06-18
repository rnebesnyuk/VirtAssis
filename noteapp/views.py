from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from .forms import *
from .models import *
from .utils import *


@login_required
def main(request):
    notes = Note.objects.filter(user=request.user)
    tags = Tag.objects.filter(user=request.user)
    title = "Notes"
    return render(request, 'noteapp/index.html', {"notes": notes, 'tags': tags, 'title': title, 'menu': menu})

@login_required
def sort_by_done(request):
    notes = Note.objects.filter(user=request.user).order_by('-done')
    tags = Tag.objects.filter(user=request.user)
    title = "Notes"
    return render(request, 'noteapp/index.html', {"notes": notes, 'tags': tags, 'title': title, 'menu': menu})

@login_required
def sort_by_undone(request):
    notes = Note.objects.filter(user=request.user).order_by('done')
    tags = Tag.objects.filter(user=request.user)
    title = "Notes"
    return render(request, 'noteapp/index.html', {"notes": notes, 'tags': tags, 'title': title, 'menu': menu})

@login_required
def sort_by_priority(request):
    notes = Note.objects.filter(user=request.user).order_by('-importance')
    tags = Tag.objects.filter(user=request.user)
    title = "Notes"
    return render(request, 'noteapp/index.html', {"notes": notes, 'tags': tags, 'title': title, 'menu': menu})

@login_required
def sort_by_priority_rev(request):
    notes = Note.objects.filter(user=request.user).order_by('importance')
    tags = Tag.objects.filter(user=request.user)
    title = "Notes"
    return render(request, 'noteapp/index.html', {"notes": notes, 'tags': tags, 'title': title, 'menu': menu})

@login_required
def add_tag(request):
    title = "Add tag"

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            form.save()
            return redirect(to='add_note')
        else:
            return render(request, 'noteapp/tag.html', {'form': form, 'menu': menu, 'title': title})

    return render(request, 'noteapp/tag.html', {'form': TagForm(), 'menu': menu, 'title': title})

@login_required
def add_note(request):
    title = "Add note"
    tags = Tag.objects.filter(user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note = form.save()

            choice_tags = Tag.objects.filter(user=request.user, name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='notes')
        else:
            return render(request, 'noteapp/note.html', {"tags": tags, 'form': form, 'menu': menu, 'title': title})

    return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm(), 'menu': menu, 'title': title})

@login_required
def edit_note(request, note_id):
    title = "Edit note"

    note = Note.objects.get(pk=note_id)
    tags = Tag.objects.filter(user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.tags.set([])
            choice_tags = Tag.objects.filter(user=request.user, name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                note.tags.add(tag)

            note.save()
            messages.success(request, "Note updated successfully!")
            return redirect('detail', note_id=note_id)
    else:
        form = NoteForm(instance=note)

    context = {
        'form': form,
        'menu': menu, 
        'title': title,
        'tags': tags,
    }

    return render(request, 'noteapp/edit_note.html', context)

@login_required
def detail(request, note_id):
    title = "Note"

    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/detail.html', {"note": note, 'menu': menu, 'title': title})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def set_undone(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=False)
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to='notes')

@login_required
def search_note(request):
    title= "Search"

    search_query = request.GET.get("search")

    if search_query:
        notes_by_name = Note.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query), user=request.user)

        tags = Tag.objects.filter(name__icontains=search_query)
        notes_by_tags = Note.objects.filter(tags__in=tags, user=request.user)

        notes = notes_by_name.union(notes_by_tags)

        if notes:
            return render(request, 'noteapp/search_note.html', {'notes': notes, 'title': title, 'menu': menu})
        else:
            return render(request, 'noteapp/search_note.html', {'message': 'Nothing found', 'title': title, 'menu': menu})
    else:
        return render(request, 'noteapp/search_note.html', {'title': title})
    
@login_required
def get_notes_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    notes = tag.note_set.filter(user=request.user)

    context = {
        'title': 'Notes by tag',
        'tag': tag,
        'notes': notes,
        'menu': menu
    }
    return render(request, 'noteapp/notes_by_tag.html', context)