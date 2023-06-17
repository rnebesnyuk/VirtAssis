from .forms import TagForm, NoteForm
from .models import Tag, Note
from django.shortcuts import render, redirect, get_object_or_404


def main(request):
    notes = Note.objects.all()
    return render(request, 'noteapp/index.html', {"notes": notes})


def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='noteapp:note')
        else:
            return render(request, 'noteapp/tag.html', {'form': form})

    return render(request, 'noteapp/tag.html', {'form': TagForm()})


def note(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/note.html', {"tags": tags, 'form': form})

    return render(request, 'noteapp/note.html', {"tags": tags, 'form': NoteForm()})


def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, 'noteapp/detail.html', {"note": note})



def set_done(request, note_id):
    Note.objects.filter(pk=note_id).update(done=True)
    return redirect(to='noteapp:main')


def delete_note(request, note_id):
    Note.objects.get(pk=note_id).delete()
    return redirect(to='noteapp:main')


def search_note(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        notes = Note.objects.filter(name__icontains=query, author=request.user)
    else:
        notes = []
    return render(request, 'note_app/search_note.html', {'notes': notes})