import re
import sys
from urllib.request import urlopen
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
import requests

def url_hook(base_url):
    if not base_url.startswith(("http", "https")):
        raise ImportError
    try:
        response = requests.get(base_url)
        data = response.text
    except Exception as e:
        print(f"Не удалось получить данные с URL: {base_url}, ошибка: {e}")
        return None

    filenames = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*\.py", data)
    modnames = {filename[:-3] for filename in filenames}
    return URLFinder(base_url, modnames)


class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader()
            return spec_from_loader(name, loader, origin=origin)

        else:
            return None


class URLLoader:
    def create_module(self, target):
        return None

    def exec_module(self, module):
        with urlopen(module.__spec__.origin) as page:
            source = page.read()
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)


sys.path_hooks.append(url_hook)
sys.path.append("http://192.168.1.59:8000")
