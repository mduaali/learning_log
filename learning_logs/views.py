from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """home page for learning log"""
    return render(request,'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics, optionally filtered by search."""
    query = request.GET.get('q', '')  # grab search term
    topics = Topic.objects.filter(owner=request.user)
    if query:
        topics = topics.filter(text__icontains=query)
    topics = topics.order_by('date_added')
    context = {'topics': topics, 'query': query}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """show single topic and all its entries"""
    topic = Topic.objects.get(id= topic_id)
    entries = topic.entry_set.order_by('-date_added') 
    context = {'topic': topic, 'entries' : entries}
    return render (request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """add a new topic"""
    if request.method != 'POST':
        # means no data was submitted
        form = TopicForm()
    else:
        # POST was submitted so process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    #display blank or invalid form
    context = {'form':form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """add new entry for particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # if no data submitted, create a blank form
        form = EntryForm()
    else:
        #POST was submitted so process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id= topic_id)
    
    #display blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request, entry_id):
    """edit existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #initial request, prefill form with current entry
        form=EntryForm(instance=entry)
    else:
        #post data submitted, process data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """Delete a topic"""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        topic.delete()
        return redirect('learning_logs:topics')

    return render(request, 'learning_logs/delete_topic_confirm.html', {'topic': topic})


@login_required
def delete_entry(request, entry_id):
    """Delete an entry"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method == 'POST':
        entry.delete()
        return redirect('learning_logs:topic', topic_id=topic.id)

    return render(request, 'learning_logs/delete_entry_confirm.html', {'entry': entry})