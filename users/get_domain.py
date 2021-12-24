def get_web_url(request):
    protocol = 'https://' if request.is_secure() else 'http://'
    return protocol + request.get_host()