from django.shortcuts import render
from .forms import give_data_form
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from django.http import HttpResponse

# create Home page
def Home_page_view(request):
    if request.method == 'POST':
        data = request.POST
        if data['method'] == 'trybal' and data['types_tower'] == 'sieve tray':
            return redirect('/Home/sieveTray/')
        elif data['method'] == 'trybal' and data['types_tower'] == 'packed tray':
            # return render(request, 'packedTray.html',{data['method']:'trybal', data['types_tower']: 'packed tray' })
            return redirect('/Home/packedtray/')
    return render(request, 'Home.html')



def packedTray_view(request):
    return render(request, 'packedTray/packedTray.html')

# Create your views here.
# create sieve tray page
def sieveTray_view(request):
    if request.method == "POST":
        form = give_data_form(request.POST)
        if form.is_valid() :
            FlowRateVapor = form.cleaned_data['FlowRateVapor']
            FlowRateLiquid = form.cleaned_data['FlowRateLiquid']
            resultt = FlowRateVapor * FlowRateLiquid
            return render(request, 'sieveTray/result.html', {'resultt': resultt})
    else:
        form = give_data_form()
    # return render(request, 'sieveTray.html', {'form': form})
    return render(request, 'sieveTray/sieveTray.html', {'form': form})


