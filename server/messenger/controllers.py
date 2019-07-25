from protocol import make_response


def send_message(request):
    print('send_message controller call')
    return make_response(request, 200)

