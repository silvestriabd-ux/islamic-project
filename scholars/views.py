from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Scholar
from django.shortcuts import render, redirect
from .forms import ScholarSubmissionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


from django.contrib import messages


@login_required
# def submit_scholar(request):
def submit_scholar(request):
    if not is_contributor(request.user):
        raise PermissionDenied
    # submitted = False

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
    scholars = Scholar.objects.filter(
        status='published').order_by('-created_at')
    return render(request, 'scholar_list.html', {'scholars': scholars})


def scholar_detail(request, slug):
    scholar = get_object_or_404(Scholar, slug=slug)

    if scholar.status != 'published':
        if not request.user.is_authenticated:
            raise Http404()

        if scholar.author != request.user:
            raise Http404()

    return render(request, 'scholar_detail.html', {'scholar': scholar})


def home(request):
    featured_scholars = Scholar.objects.filter(
        status='published'
    ).order_by('-created_at')[:3]

    return render(request, 'home.html', {
        'featured_scholars': featured_scholars
    })


def author_profile(request, username):
    user = get_object_or_404(User, username=username)

    scholars = Scholar.objects.filter(
        author=user,
        status='published'
    ).order_by('-created_at')

    return render(request, "author_profile.html", {
        "author_user": user,
        "scholars": scholars
    })


def is_contributor(user):
    return user.groups.filter(name="Contributor").exists() or user.is_superuser


@login_required
def profile(request):
    scholars = Scholar.objects.filter(
        author=request.user).order_by('-created_at')
    return render(request, "profile.html", {"scholars": scholars})


@login_required
@permission_required("scholars.can_publish", raise_exception=True)
def editor_review(request):
    drafts = Scholar.objects.filter(status="draft").order_by("-created_at")
    return render(request, "editor_review.html", {"drafts": drafts})


@login_required
@permission_required("scholars.can_publish", raise_exception=True)
@require_POST
def editor_publish(request, pk):
    scholar = get_object_or_404(Scholar, pk=pk, status="draft")
    scholar.status = "published"
    scholar.save()
    return redirect("editor_review")
