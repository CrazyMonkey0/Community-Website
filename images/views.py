from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.conf import settings
import redis
from common.decorators import ajax_required, is_ajax
from actions.utils import create_action
from .forms import ImageCreateForm
from .models import Image

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'Added image', new_image)
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
  
    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # Increment by 1 the total number of displays of a given image.
    total_views = r.incr('image:{}:views'.format(image.id))
    # Increment by 1 the ranking of a given image.
    r.zincrby('image_ranking', 1, image.id)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                  'image': image,
                  'total_views': total_views,})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)

            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})



@login_required
def image_list(request):
    
    images = Image.objects.all()
    paginator = Paginator(images, 10)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if is_ajax(request):
        return render(request,
               'images/image/list_ajax.html',
               {'section': 'images', 'images': images})
    return render(request,
            'images/image/list.html',
            {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # Download image ranking dictionary.
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # Downloading the most frequently displayed images.
    most_viewed = list(Image.objects.filter(
                            id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request,
                  'images/image/ranking.html',
                  {'section': 'images',
                  'most_viewed': most_viewed})