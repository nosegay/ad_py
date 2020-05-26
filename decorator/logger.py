from datetime import datetime
import json


def get_logger(log_file):
    def logger(old_function):
        def new_function(*args, **kwargs):
            with open(log_file, 'a') as fp:
                fp.write(f'Момент вызова функции: {datetime.utcnow()}\n')
                fp.write(f'Имя функции: {old_function.__name__}\n')
                fp.write(f'Переданные аргументы:\n')
                fp.write(f'\t{args}\n')
                fp.write(f'\t{kwargs}\n')

                try:
                    result = old_function(*args, **kwargs)
                except Exception as e:
                    fp.write(f'При выполнении функции возникла ошибка {e.__class__.__name__}\n')
                    fp.write('----------------------\n\n')
                    raise e
                fp.write(f'Возвращаемое значение: {result}\n')
                fp.write('----------------------\n\n')

            return result
        return new_function
    return logger


class WikiUrlGenerator:
    @get_logger('test.log')
    def __init__(self, json_file, output_file):
        with open(json_file, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            self.countries = (country['name']['common'] for country in json_data)
        self.output_file = open(output_file, 'w+', encoding='utf8')

    @get_logger('test.log')
    def __iter__(self):
        return self

    @get_logger('test.log')
    def __next__(self):
        try:
            current_country = self.countries.__next__()
        except StopIteration:
            self.output_file.close()
            raise StopIteration
        current_country = current_country.replace(' ', '_')
        write_count = self.output_file.write(f'{current_country} - https://en.wikipedia.org/wiki/{current_country}\n')
        return write_count


if __name__ == '__main__':
    my_iterator = WikiUrlGenerator('countries.json', 'wiki_urls.txt')
    for ctr, x in enumerate(my_iterator):
        print(f'#{ctr+1} В файл записано {x} байт')
