from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from models import CatForm
from PIL import Image
from align import CropFace
from eigencats import cuteOrNot
import numpy


def index(request):
    form = CatForm()
    if request.method == 'POST':
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the data in form.cleaned_data
            form_data = form.cleaned_data
            picture = form_data['picture']
            left_eye_x = form_data['left_eye_x']
            left_eye_y = form_data['left_eye_y']
            right_eye_x = form_data['right_eye_x']
            right_eye_y = form_data['right_eye_y']

            image = Image.open(picture).convert("L")
            aligned_face = CropFace(image,
                                    eye_left=(left_eye_x, left_eye_y),
                                    eye_right=(right_eye_x, right_eye_y),
                                    offset_pct=(0.1, 0.3),
                                    dest_sz=(200, 300))
            np_face = numpy.asarray(aligned_face, dtype=numpy.uint8)
            is_cute = cuteOrNot(np_face)
            cuteness = "...not cute. Sorry"
            if is_cute:
                cuteness = "adorable!"
            return render(request, 'catness/result.html', {
                'is_cute': str(cuteness)
            })

    return render(request, 'catness/index.html', {
        'form': form,
    })


def result(request):
    return render(request, 'catness/result.html', {'is_cute': 'unkown'})


def explanation(request):
    return render(request, 'catness/explanation.html', {'data': 'data'})
