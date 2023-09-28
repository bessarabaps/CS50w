from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse

from .forms import NewItemForm
from .models import Item, Comment


def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    current_user = request.user
    item_in_watchlist = current_user in item.watchlist.all()
    comments = Comment.objects.filter(item=item).all()
    bid_by = item.bid_by
    if item.autor == current_user:
        owner = True
    else:
        owner = False
    if item.active == False:
        if bid_by != owner and bid_by == current_user:
            return render(request, 'item/detail.html', {
                'Item': item,
                'item_in_watchlist': item_in_watchlist,
                'owner': owner,
                'comments': comments,
                'message' : "Congratulate!You won this item"
            })
    else:
        return render(request, 'item/detail.html', {
            'Item': item,
            'item_in_watchlist': item_in_watchlist,
            'owner': owner,
            'comments': comments
        })
    return render(request, 'item/detail.html', {
        'Item': item,
        'item_in_watchlist': item_in_watchlist,
        'owner': owner,
        'comments': comments
    })


def add_Watchlist(request, pk):
    item = get_object_or_404(Item, pk=pk)
    current_user = request.user
    item.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("item:detail", args=(item.id,) ))


def remove_Watchlist(request, pk):
    item = get_object_or_404(Item, pk=pk)
    current_user = request.user
    item.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("item:detail", args=(item.id,) ))

def add_bid(request, pk):
    item = get_object_or_404(Item, pk=pk)
    current_price = item.price
    current_user = request.user
    item_in_watchlist = request.user in item.watchlist.all()
    comments = Comment.objects.filter(item=item).all()
    if item.autor == request.user:
        owner = True
    else:
        owner = False

    if request.method =='POST':
        bid = request.POST["bid"]
        if float(current_price) < float(bid):
            item.price = bid
            item.bid_by = current_user
            item.save()
            return HttpResponseRedirect(reverse("item:detail",   args=(item.id,) ))
        else:
            return render(request, 'item/detail.html', {
            'Item': item,
            'item_in_watchlist': item_in_watchlist,
            'owner': owner,
            'comments': comments,
            'message':  "Your bid must be higher than the previous!"
    })

    else:
        return HttpResponseRedirect(reverse("item:detail", args=(item.id,) ))


def close_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method =='POST':
        item.active = False
        item.save()
        return HttpResponseRedirect(reverse("item:detail", args=(item.id,) ))
    else:
        return HttpResponseRedirect(reverse("item:detail", args=(item.id,) ))


def add(request):

    if request.method =='POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.autor = request.user
            item.bid_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/add.html', {
            'form': form
        })


def add_comment(request, pk):
    item = get_object_or_404(Item, pk=pk)
    current_user = request.user
    massege = request.POST["new_comment"]

    if massege != "":
        new_comment = Comment(
            user = current_user,
            item = item,
            message = massege
        )

        new_comment.save()

    return HttpResponseRedirect(reverse("item:detail", args=(item.id,) ))
