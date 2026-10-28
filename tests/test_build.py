"""Build real content and check generated output using only Python's standard library."""
import os
from pathlib import Path
import subprocess
import tempfile
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlparse

THEME = Path(__file__).resolve().parents[1]
HUGO = os.environ.get('HUGO', 'hugo')
BASE = 'https://example.org/cinnastyx/'


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.elements = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    def select(self, tag):
        return [attrs for name, attrs in self.elements if name == tag]


with tempfile.TemporaryDirectory(prefix='cinnastyx-test-') as temp:
    work = Path(temp)
    for scheme in ('dark', 'light', 'gray', 'preference'):
        override = work / 'override.toml'
        override.write_text(f'[params]\nscheme = "{scheme}"\n[pagination]\npagerSize = 2\n')
        output = work / scheme
        subprocess.run([
            HUGO, '--source', str(THEME / 'exampleSite'),
            '--config', f'{THEME / "exampleSite/config.toml"},{override}',
            '--baseURL', BASE, '--destination', str(output),
            '--cacheDir', str(work / 'cache'), '--minify', '--panicOnWarning',
            '--printPathWarnings',
        ], check=True, stdout=subprocess.DEVNULL)
        home = Document((output / 'index.html').read_text())
        assert home.select('html')[0]['data-scheme'] == scheme
        assert home.select('html')[0]['lang'] == 'en-US'
        assert home.select('h1')
        assert (output / '404.html').exists()
        assert (output / 'page/2/index.html').exists()
        assert (output / 'index.xml').exists()
        assert (output / 'sitemap.xml').exists()
        assert (output / 'robots.txt').exists()
        cards = [a for a in home.select('a') if a.get('class') == 'post-card-content-link']
        assert len(cards) == 2 and all('/posts/' in a['href'] for a in cards)
        for file in output.rglob('*.html'):
            source = file.read_text()
            doc = Document(source)
            # Alias redirect documents intentionally have no site layout.
            if not doc.select('main'):
                continue
            assert len(doc.select('main')) == 1, file
            assert any(a.get('rel') == 'canonical' and a['href'].startswith(BASE) for a in doc.select('link')), file
            assert any(a.get('name') == 'description' for a in doc.select('meta')), file
            for img in doc.select('img'):
                assert 'alt' in img, file
                if 'srcset' in img:
                    assert img.get('sizes') and img.get('width') and img.get('height'), file
                    assert '<nil>' not in img['sizes'], file
            page_url = urljoin(BASE, str(file.relative_to(output)))
            for tag, attrs in doc.elements:
                for attr in ('href', 'src'):
                    value = attrs.get(attr, '')
                    if not value or value.startswith('#'):
                        continue
                    url = urlparse(urljoin(page_url, value))
                    if url.netloc != 'example.org' or url.scheme not in ('http', 'https'):
                        continue
                    assert url.path.startswith('/cinnastyx/'), (file, value)
                    target = output / unquote(url.path.removeprefix('/cinnastyx/'))
                    assert target.is_file() or (target / 'index.html').is_file(), (file, value)
        image_page = Document((output / 'posts/image-test/index.html').read_text())
        assert any(i.get('alt') == 'Cactus flower' and i['sizes'] == '(min-width: 1400px) 1400px, 92vw' for i in image_page.select('img'))
        math = (output / 'posts/math-typesetting/index.html').read_text()
        assert math.count('/dist/katex.min.js') == 1
        assert 'math.inline' not in math
        print(f'{scheme}: build, pagination, metadata, images, and local links passed')
