import json


class WikiUrlGenerator:
    def __init__(self, json_file, output_file):
        with open(json_file, 'r', encoding='utf8') as fp:
            json_data = json.load(fp)
            self.countries = (country['name']['common'] for country in json_data)
        self.output_file = open(output_file, 'w+', encoding='utf8')

    def __iter__(self):
        return self

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
