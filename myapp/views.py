from django.shortcuts import render


def homepage(request):
    """Display homepage."""
    template_name = 'index.html'
    return render(request, template_name)
