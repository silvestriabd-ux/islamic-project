from django.shortcuts import get_object_or_404
from .models import Scholar
from django.shortcuts import render, redirect
from .forms import ScholarSubmissionForm
# Create your views here.


def submit_scholar(request):
    if request.method == 'POST':
        form = ScholarSubmissionForm(request.POST)
        if form.is_valid():
            scholar = form.save(commit=False)
            scholar.status = 'draft'
            scholar.save()
            return redirect('submission_success')
    else:
        form = ScholarSubmissionForm()

    return render(request, 'submit_scholar.html', {'form': form})


def submission_success(request):
    return render(request, 'submission_success.html')


def scholar_list(request):
    scholars = Scholar.objects.filter(status='published')
    return render(request, 'scholar_list.html', {'scholars': scholars})


def scholar_detail(request, slug):
    scholar = get_object_or_404(
        Scholar,
        slug=slug,
        status='published'
    )
    return render(request, 'scholar_detail.html', {'scholar': scholar})


def home(request):
    featured_scholars = Scholar.objects.filter(
        status='published'
    ).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'featured_scholars': featured_scholars
    })
