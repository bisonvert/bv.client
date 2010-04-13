def unicode_to_dict(request):
    return dict([(key.__str__(),value) for key,value in request.items()])
