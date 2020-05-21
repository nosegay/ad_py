import hashlib


def md5_generator(file_path):
    fp = open(file_path, 'r')
    while True:
        try:
            current_line = fp.__next__()
        except StopIteration:
            fp.close()
            break

        yield hashlib.md5(current_line.encode()).hexdigest()


if __name__ == '__main__':
    for ctr, md5_hash in enumerate(md5_generator('wiki_urls.txt')):
        print(f'Hash #{ctr+1}: {md5_hash}')
