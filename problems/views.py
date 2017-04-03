from django.shortcuts import render, redirect, get_object_or_404
from problems.models import Problems, Runs, Subs_code
from problems.judge import runjudge
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        context = {'user' : request.user}
        p = Problems.objects.all()
        context['problems'] = p
        return render(request,'problems/index.html', context);
    else:
        return redirect('users:login')

def add_problem_form(request):

    if request.user.is_authenticated:

        user = request.user

        if request.method == "POST":
            languages = ['c','cpp','c#','java','python','python3']
            selected_languages = list(set(languages) & set(request.POST.keys()))
            display_languages = []

            for x in selected_languages:
                display_languages.insert(0,request.POST[x])

            language = ','.join(display_languages)

            p = Problems()
            p.author = user
            p.language = language
            p.statement = request.POST['statement']
            p.name = request.POST['name']
            p.input = request.POST['input']
            p.output = request.POST['output']
            p.timelimit = request.POST['timelimit']
            p.type = request.POST['type']
            p.status = request.POST['status']
            p.score = 10
            p.save()

            return redirect('problems:home')

        return render(request,'problems/add_problem.html');

    return redirect('users:login')

def display_problem(request,problem_id):
    try:
        p = get_object_or_404(Problems, pk=problem_id)
        p.language = p.language.split(',')
        context = {'p': p}
        return render(request,'problems/problem_detail.html',context)
    except (KeyError, Problems.DoesNotExist):
        context = {'error_message' : 'Problem does not exist'}
        return render(request, 'problems/problem_detail.html', context)

def submit_problem(request,problem_id):
    try:
        p = get_object_or_404(Problems, pk=problem_id)
        p.language = p.language.split(',')

        if request.method == "POST":
            run = Runs()
            run.user = request.user
            run.problem = p
            run.tid = 1
            run.language = request.POST['language']
            run.access = 'public'
            run.save()

            p.total += 1

            sub = Subs_code()
            sub.run = run
            sub.name = "Main"
            sub.code = request.POST['code']

            sub.save()

            runjudge(sub.pk)

            return HttpResponseRedirect(reverse('problems:display_results',kwargs={'problem_id':p.id, 'run_id':run.pk}))
    except (KeyError, Problems.DoesNotExist):
        context = {'error_message' : 'Problem does not exist'}

        return HttpResponse('<html>Hello World</html>')

def display_problem_run(request,problem_id,run_id):
    try:
        p = get_object_or_404(Problems, pk=problem_id)
        run = get_object_or_404(Runs, pk=run_id)
        sub = get_object_or_404(Subs_code, run=run)
        p.language = p.language.split(',')
        context = {'p': p,'sub':sub}
        return render(request,'problems/problem_detail.html',context)
    except (KeyError, Problems.DoesNotExist):
        context = {'error_message' : 'Problem does not exist'}
        return render(request, 'problems/problem_detail.html', context)


def trial(request):
    runjudge(1)
    return HttpResponse(request)

def display_results(request,problem_id,run_id):
    run = Runs.objects.get(pk=run_id)
    sub = Subs_code.objects.get(run=run)
    my_runs = Runs.objects.all().filter(user=run.user, problem=run.problem)
    context = { 'sub' : sub, 'my_runs' : my_runs}


    return render(request,'problems/display_results.html',context)

def display_submissions(request,problem_id):
    p = Problems.objects.get(pk=problem_id)
    runs = Runs.objects.all().filter(problem=p)
    context = {
        'runs' : runs,
        'problem' : p,
    }
    return render(request,'problems/display_submissions.html',context)
