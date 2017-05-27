# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import Http404

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, Flow, Tag, TagGroup


def postList(request, flow=None, tag=None, group=None, group_tag=None):
    ''' Логика страницы со списком статей '''

    if flow:
        query_list = Article.objects.filter(flow__sys_name=flow)
        page_title = Flow.objects.get(sys_name = flow).name

    elif tag:
        query_list = Article.objects.filter(tags__sys_name=tag)
        page_title = Tag.objects.get(sys_name = tag).name

    elif group:
        query_list = Article.objects.filter(group__sys_name=group)
        page_title = TagGroup.objects.get(sys_name = group).name

    elif group_tag:
        filterList = group_tag.split('-')
        query_list = Article.objects.filter(group__sys_name=filterList[0], tags__sys_name=filterList[1])
        page_title = u'Последние статьи'

    else:
        query_list = Article.objects.all()
        page_title = u'Последние статьи'

    #filter non-publisher articles and sort data by date publish
    query_list = query_list.filter(published_date__isnull=False).order_by('-published_date')

    paginator = Paginator(query_list, 15)
    page = request.GET.get('page')

    try:
        postObj_list = paginator.page(page)
    except PageNotAnInteger:
        postObj_list = paginator.page(1)
    except EmptyPage:
        postObj_list = paginator.page(paginator.num_pages)

    return render(request, 'pages/cards.html', {
        'postObj_list': postObj_list,
        'page_title'  : page_title,
    })


def postArticle(request, post=None):
    ''' Логика страницы с открытой статьей '''

    postObj = get_object_or_404(Article, pk=post)
    if not postObj.published_date: raise Http404()

    return render(request, 'pages/post.html', {
        'postObj': postObj,
    })


def flowList(request):
    ''' Логика страницы со списком тегов и рубрик '''

    flowObj_list  = Flow.objects.all()
    groupObj_list = TagGroup.objects.all()
    page_title    = u'Рубрики'

    return render(request, 'pages/hubs.html', {
        'flowObj_list' : flowObj_list,
        'groupObj_list': groupObj_list,
        'page_title'   : page_title,
    })
