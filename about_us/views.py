from django.shortcuts import render

# story view
def our_story(request):
    return render(request, 'about_us/our_story.html')

# career view
def career(request):
    return render(request, 'about_us/careers.html')

# press view
def press(request):
    return render(request, 'about_us/press.html')