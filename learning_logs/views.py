from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Entry, Topic
from .forms import EntryForm, TopicForm

def index(request):
    """the homepage for learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html',context)

@login_required
def topic(request, topic_id):
    """show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    # make sure the topic belongs to a current user
    if topic.owner!=request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """add a new topic for user"""
    if request.method!='POST':
        # no data, create empty form
        topic_form = TopicForm()
    else:
        # process data
        topic_form = TopicForm(data=request.POST)
        if topic_form.is_valid():
            new_topic = topic_form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # display a blank or invalid form
    context = {'form':topic_form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """add a new entry to a given topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method!='POST':
        # no data, create empty entry
        entry_form = EntryForm()
    else:
        entry_form = EntryForm(data=request.POST)
        if entry_form.is_valid():
            new_entry = entry_form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)
    # display a blank or invalid form
    context = {'topic':topic, 'form':entry_form}
    return render(request,'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """edit an entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner!=request.user:
        raise Http404
    if request.method!='POST':
        form  = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    context = {'entry':entry, 'topic':topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

