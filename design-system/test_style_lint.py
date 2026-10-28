"""Contract samples: run with unittest discover; no third-party dependencies."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest

spec = importlib.util.spec_from_file_location('editorial_style_lint', Path(__file__).with_name('style-lint.py'))
lint = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lint
spec.loader.exec_module(lint)


class StyleContract(unittest.TestCase):
    def test_positive_print_primitives(self):
        css = '''/* ignored: border-radius:9px; color:red; */
:root { --k-color-paper:#f3ebdd; --k-font-display:'Barlow Condensed',sans-serif; }
@font-face {font-family:'IBM Plex Mono';src:url(font.woff2);}
@media (min-width:320px) {.tile:hover {border-radius:0 0px / 0% !important;
color:var(--k-color-ink);border:2px solid currentColor;
box-shadow:6px 6px 0 var(--k-color-ink), -2px 3px 0 4px #c8442b;
background:transparent;filter:brightness(0);font:800 2rem/1.1 var(--k-font-display);}}
.band::after {content:'';background:#eea23a;transform:rotate(-10deg);}
'''
        self.assertEqual(lint.lint_css(css), [])
        self.assertEqual(lint.lint_html('<head><title>🌈</title><style>a{color:#171b1a}</style></head><p hidden>🌈</p><p>PLAYER ↗ ⌘O © 2026</p>'), [])

    def test_each_forbidden_property(self):
        values = ['border-radius:1px', '-webkit-border-radius:4px', 'color:CanvasText', 'border-top-left-radius:var(--radius)',
                  'border-start-start-radius:50%', 'box-shadow:0 2px 8px #171b1a',
                  'box-shadow:var(--shadow)', 'box-shadow:0 0 var(--blur) var(--k-color-ink)',
                  'text-shadow:0 0 3px #171b1a', 'font:400 1rem var(--k-font-body), Arial', 'background:linear-gradient(#f3ebdd,#171b1a)',
                  'background:repeating-conic-gradient(#f3ebdd,#171b1a)',
                  'backdrop-filter:none', '-webkit-backdrop-filter:blur(2px)',
                  'filter:blur(0px)', 'filter:drop-shadow(0 0 2px #171b1a)', 'filter:url(filters.svg#blur)',
                  'color:#ffffff', 'border:1px solid red', 'color:rgb(23,27,26)',
                  'background:hsl(0 0% 0%)', 'font-family:Arial, sans-serif',
                  'font:16px/1.4 Arial', '--k-font-body:Sora', 'content:"🔥"']
        for value in values:
            with self.subTest(value=value):
                self.assertTrue(lint.lint_css('.x {' + value + '}'))

    def test_later_declaration_and_nested_rule_not_skipped(self):
        issues = lint.lint_css('/* two\nlines */\n@media print {\n.x:hover {color:#fff8ed;\n border-radius:5px;}\n}')
        self.assertEqual([(i.line, i.message.split()[0]) for i in issues], [(5, 'border-radius')])

    def test_html_styles_and_visible_emoji_lines(self):
        html = '<head>\n<style>\na {color:pink}\n</style></head>\n<p style="border-radius:3px">🚀</p>\n<script>"🚀"</script><p aria-hidden="true">🔥</p>'
        issues = lint.lint_html(html, 'sample.html')
        self.assertEqual([i.line for i in issues], [3, 5, 5, 6])
        self.assertTrue(all(str(i).startswith('sample.html:') for i in issues))

    def test_strings_urls_and_multiple_shadows(self):
        self.assertEqual(lint.lint_css('a{background:url("red.svg#fff");content:"red; blue: pink";}'), [])
        self.assertTrue(lint.lint_css('a{box-shadow:1px 1px 0 #171b1a,0 0 2px #171b1a;}'))
        self.assertTrue(lint.lint_css('a{color:var(--color, #fff);}'))

    def test_cli_scans_nested_and_inline_files_and_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); (root/'nested').mkdir()
            (root/'good.css').write_text('a{color:#171b1a}')
            (root/'nested'/'bad.html').write_text('<p style="color:red">x</p>')
            run = subprocess.run([sys.executable, str(Path(lint.__file__)), str(root)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertIn('bad.html:1:', run.stdout)
            self.assertIn('2 files, 1 violations', run.stdout)


if __name__ == '__main__':
    unittest.main()
