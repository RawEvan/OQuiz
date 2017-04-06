import urllib
import os.path
from os.path import join, dirname


def get_file(url, file_name):
    file_path = join(dirname(dirname(__file__)), 'res', file_name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    else:
        os.makedirs(file_path)
    try:
        f = urllib.urlretrieve(url, file_path)
        return f.read()
    except Exception as e:
        print e

if __name__ == '__main__':
    f = get_file('http://ddragon.leagueoflegends.com/cdn/6.24.1/data/zh_CN/champion.json', 'json/champion.json')
    print f
    # import doctest
    # doctest.testmod(verbose=True)