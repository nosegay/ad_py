def adv_print(*args, **kwargs):
    if 'start' in kwargs.keys():
        args = (kwargs['start'],) + args
        kwargs.pop('start')

    if 'max_line' in kwargs.keys():
        max_len = kwargs['max_line']
        kwargs.pop('max_line')

        sep = kwargs['sep'] if 'sep' in kwargs.keys() else ' '
        output_str = sep.join(str(arg) for arg in args)

        parts = (s.strip() for s in output_str.split('\n'))
        new_args = list()
        for part in parts:
            new_args.extend([part[x:x + max_len] for x in range(0, len(part), max_len)])
        args = new_args
        kwargs['sep'] = '\n'

    if 'in_file' in kwargs.keys():
        new_kwargs = kwargs.copy()
        new_kwargs['file'] = open(kwargs['in_file'], 'w+')
        kwargs.pop('in_file')
        new_kwargs.pop('in_file')
        print(*args, **new_kwargs)

    print(*args, **kwargs)


adv_print('Данный вывод может обработать "строку", число', 7888344, ' и даже список', [1, 2, 3],
          start='Новый вывод:\n', in_file='output.txt', max_line=9)

adv_print(f'Данный вывод может обработать "строку", число {7888344} и даже список {[1, 2, 3]}',
          start='Новый вывод:\n', in_file='output.txt', max_line=9)
