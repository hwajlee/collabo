from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Article, Reply
from .forms import ArtForm, ReplyForm

@require_safe
def art_index(request):
    articles = Article.objects.order_by('-pk')
    context = {'title': 'Home', 'articles': articles}
    return render(request, 'board/index.html', context)
@require_safe
def art_detail(request, artpk):
    article = get_object_or_404(Article, pk=artpk)
    repform = ReplyForm()
    context = {'title': article.title, 'article': article, 'repform': repform}
    return render(request, 'board/detail.html', context)
@login_required
@require_http_methods(['GET', 'POST'])
def create_art(request):
    if request.method == 'POST':
        artform = ArtForm(request.POST)
        if artform.is_valid():
            article = artform.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('board:art_detail', article.pk)
    else:
        artform = ArtForm()
    context = {'title': 'Writing', 'btn': '등록', 'artform': artform}
    return render(request, 'board/form.html', context)
@login_required
@require_http_methods(['GET', 'POST'])
def update_art(request, artpk):
    article = get_object_or_404(Article, pk=artpk)
    if request.method == 'POST':
        artform = ArtForm(request.POST, instance=article)
        if artform.is_valid():
            article = artform.save()
            return redirect('board:art_detail', article.pk)
    elif request.user == article.user:
        artform = ArtForm(instance=article)
        context = {'title': 'Editting', 'btn': '수정', 'artform': artform}
        return render(request, 'board/form.html', context)
    else:
        return HttpResponseForbidden('잘못된 요청입니다.')
@login_required
@require_POST
def delete_art(request, artpk):
    article = get_object_or_404(Article, pk=artpk)
    if request.user == article.user:
        article.delete()
    return redirect('board:art_index')
@login_required
@require_POST
def vote_art(request, artpk):
    article = get_object_or_404(Article, pk=artpk)
    user = request.user
    if user == article.user:
        return HttpResponseForbidden('해당 글의 작성자는 추천을 할 수 없습니다.')
    elif article.is_voted(user):
        article.vote.remove(user)
    else:
        article.vote.add(user)
    return redirect('board:art_detail', article.pk)

@login_required
@require_POST
def create_com(request, artpk):
    article = get_object_or_404(Article, pk=artpk)
    reply_form = ReplyForm(request.POST)
    if reply_form.is_valid():
        reply = reply_form.save(commit=False)
        reply.article = article
        reply.user = request.user
        reply.save()
    return redirect('board:art_detail', article.pk)
@login_required
@require_POST
def delete_com(request, artpk, reppk):
    article = get_object_or_404(Article, pk=artpk)
    reply = get_object_or_404(Reply, pk=reppk)
    if reply.user != request.user:
        return HttpResponseForbidden('권한이 없는 요청입니다.')
    else:
        reply.delete()
    return redirect('board:art_detail', article.pk)
@login_required
@require_POST
def vote_com(request, artpk, reppk):
    article = get_object_or_404(Article, pk=artpk)
    reply = get_object_or_404(Reply, pk=reppk)
    user = request.user
    if user == reply.user:
        return HttpResponseForbidden('해당 댓글의 작성자는 추천을 할 수 없습니다.')
    elif reply.is_voted(user):
        reply.vote.remove(user)
    else:
        reply.vote.add(user)
    return redirect('board:art_detail', article.pk)
