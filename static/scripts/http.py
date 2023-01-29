# http request processing for Goatt algorithm

def process_request(request):
    if request.method == 'GET':
        data = {
            "age": request.args.get('age', type=str),
            "injury": request.args.get('injury', default=False, type=bool),
            "play_freq": request.args.get('play_freq', type=str),
            "break_freq": request.args.get('break_freq', type=str),
            "goal": request.args.get('goal', type=str)
        }

    elif request.method == 'POST':
        data = {
            "age": request.form.get('age', type=str),
            "injury": request.form.get('injury', default=False, type=bool),
            "play_freq": request.form.get('play_freq', type=str),
            "break_freq": request.form.get('break_freq', type=str),
            "goal": request.form.get('goal', type=str)
        }

    return data