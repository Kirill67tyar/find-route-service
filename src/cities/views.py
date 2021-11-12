from django.shortcuts import render



def home(request):
    value = 'очконул'
    return render(request=request,
                  template_name='base.html',
                  context={'value': value, })

