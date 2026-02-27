from django.shortcuts import get_object_or_404
from .models import Scholar
from django.shortcuts import render, redirect
from .forms import ScholarSubmissionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


from django.contrib import messages


def submit_scholar(request):
    submitted = False

    if request.method == 'POST':
        form = ScholarSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            scholar = form.save(commit=False)
            scholar.author = request.user
            scholar.status = 'draft'
            scholar.save()

            messages.success(
                request,
                "Thank you. Your submission is under review."
            )

            submitted = True
            form = ScholarSubmissionForm()  # reset form

    else:
        form = ScholarSubmissionForm()

    return render(
        request,
        'submit_scholar.html',
        {'form': form, 'submitted': submitted}
    )


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


@login_required
def profile(request):
    scholars = Scholar.objects.filter(
        author=request.user).order_by('-created_at')
    return render(request, "profile.html", {"scholars": scholars})
