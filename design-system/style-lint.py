#!/usr/bin/env python3
"""Editorial Reference v2 checks. Python stdlib only; no style exceptions.

Scan every public CSS file and HTML style block/attribute plus visible text.
CSS checks include inactive rules. Flat diagonal bands use solid transformed
planes, so no gradient function is exempt. See REFERENCE.md for the contract.
"""
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
import argparse
import re
import sys

TOKENS = {'#f3ebdd', '#171b1a', '#fff8ed', '#c8442b', '#eea23a',
          '#aab7a2', '#2b5756', '#204a59', '#0065ff'}
FAMILIES = {'barlow condensed', 'ibm plex mono', 'sans-serif', 'monospace'}
# CSS named-color vocabulary is used to catch colors in shorthand declarations.
NAMED_COLORS = set('''aliceblue antiquewhite aqua aquamarine azure beige bisque
black blanchedalmond blue blueviolet brown burlywood cadetblue chartreuse
chocolate coral cornflowerblue cornsilk crimson cyan darkblue darkcyan
darkgoldenrod darkgray darkgrey darkgreen darkkhaki darkmagenta darkolivegreen
darkorange darkorchid darkred darksalmon darkseagreen darkslateblue darkslategray
darkslategrey darkturquoise darkviolet deeppink deepskyblue dimgray dimgrey
dodgerblue firebrick floralwhite forestgreen fuchsia gainsboro ghostwhite gold
goldenrod gray grey green greenyellow honeydew hotpink indianred indigo ivory
khaki lavender lavenderblush lawngreen lemonchiffon lightblue lightcoral
lightcyan lightgoldenrodyellow lightgray lightgrey lightgreen lightpink
lightsalmon lightseagreen lightskyblue lightslategray lightslategrey lightsteelblue
lightyellow lime limegreen linen magenta maroon mediumaquamarine mediumblue
mediumorchid mediumpurple mediumseagreen mediumslateblue mediumspringgreen
mediumturquoise mediumvioletred midnightblue mintcream mistyrose moccasin
navajowhite navy oldlace olive olivedrab orange orangered orchid palegoldenrod
palegreen paleturquoise palevioletred papayawhip peachpuff peru pink plum
powderblue purple rebeccapurple red rosybrown royalblue saddlebrown salmon
sandybrown seagreen seashell sienna silver skyblue slateblue slategray slategrey
snow springgreen steelblue tan teal thistle tomato turquoise violet wheat white
whitesmoke yellow yellowgreen accentcolor accentcolortext activetext buttonborder
buttonface buttontext canvas canvastext field fieldtext graytext highlight
highlighttext linktext mark marktext selecteditem selecteditemtext visitedtext'''.split())
# Scalars, no blur tokens, dynamic radii or dynamic shadows.
LENGTH = re.compile(r'(?<![\w-])[-+]?(?:\d*\.)?\d+(?:[a-z%]+)?', re.I)
COLOR_FUNCTION = re.compile(r'\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color|color-mix|light-dark)\s*\(', re.I)
EMOJI = re.compile('[\U0001f000-\U0001faff\u2600-\u27bf\u20e3\ufe0f]')
INHERIT = {'inherit', 'initial', 'unset', 'revert', 'revert-layer'}

@dataclass(frozen=True)
class Violation:
    file: str
    line: int
    message: str

    def __str__(self):
        return f'{self.file}:{self.line}: {self.message}'


def blank(match):
    """Remove comments while preserving offsets and line numbers."""
    return ''.join('\n' if c == '\n' else ' ' for c in match[0])


def split_top(text, delimiter):
    """Split outside strings and functions, returning text and source offset."""
    start = depth = 0
    quote = None
    escaped = False
    for i, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
        elif char == '(':
            depth += 1
        elif char == ')':
            depth = max(0, depth - 1)
        elif depth == 0 and char in delimiter:
            yield text[start:i], start
            start = i + 1
    yield text[start:], start


def literal_color(color):
    color = color.lower()
    if len(color) == 4:
        color = '#' + ''.join(c * 2 for c in color[1:])
    return color


def check_declaration(prop, value):
    """Yield messages for one declaration; variable fallbacks are checked too."""
    value = re.sub(r'\s*!important\s*$', '', value, flags=re.I)
    low = value.lower().strip()
    radius_prop = prop.removeprefix('-webkit-').removeprefix('-moz-')
    if radius_prop in ('border-radius', 'border-start-start-radius', 'border-start-end-radius',
                'border-end-start-radius', 'border-end-end-radius') or re.fullmatch(r'border-(top|bottom)-(left|right)-radius', radius_prop):
        parts = low.replace('/', ' ').split()
        if not parts or not all(re.fullmatch(r'[-+]?0(?:\.0+)?(?:[a-z%]+)?', p) for p in parts):
            yield 'border-radius must be literal 0 (no exceptions)'
    if prop in ('box-shadow', 'text-shadow') and low != 'none':
        for shadow, _ in split_top(low, ','):
            # Remove colors before collecting offset / blur / spread lengths.
            numbers = re.sub(r'#[\da-f]{3,8}\b|var\([^)]*\)|(?:rgb|hsl)a?\([^)]*\)', '', shadow)
            lengths = LENGTH.findall(numbers)
            if len(lengths) < 2 or (len(lengths) >= 3 and float(re.match(r'[-+]?[\d.]+', lengths[2])[0]) != 0):
                yield 'box-shadow must use a hard offset block with zero blur'
            if re.search(r'\b(?:var|calc|env)\(', re.sub(r'var\(--k-color-[a-z]+\)', '', shadow)):
                yield 'dynamic box-shadow cannot establish zero blur'
    if re.search(r'\b(?:repeating-)?(?:linear|radial|conic)-gradient\s*\(', low):
        yield 'gradients forbidden; diagonal band uses a rotated solid plane'
    if prop in ('backdrop-filter', '-webkit-backdrop-filter'):
        yield 'backdrop-filter forbidden'
    if prop in ('filter', '-webkit-filter') and low not in {'none', 'brightness(0)'}:
        yield 'filter forbidden; only brightness(0) for the complete wordmark is allowed'
    # URLs and quoted content are not color declarations. Font strings are checked below.
    colors = re.sub(r'url\([^)]*\)|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '', low)
    for color in re.findall(r'#[\da-f]{3,8}\b', colors):
        if literal_color(color) not in TOKENS:
            yield f'non-token color {color}'
    if COLOR_FUNCTION.search(colors):
        yield 'color functions forbidden; use exact palette tokens'
    # Ignore variable names so --k-color-blue does not count as named blue.
    words = re.findall(r'(?<![\w-])[a-z]+(?![\w-])', colors)
    for color in sorted(set(words) & NAMED_COLORS):
        yield f'non-token named color {color}'
    if prop == 'font-family':
        if re.fullmatch(r'var\(--k-font-(display|body|mono)\)', low) or low in INHERIT:
            return
        for family, _ in split_top(value, ','):
            if family.strip().strip('"\'').lower() not in FAMILIES:
                yield f'font family not allowed: {family.strip()}'
    if prop == 'font' and low not in INHERIT:
        if not re.fullmatch(r'(?:.+\s)?var\(--k-font-(display|body|mono)\)', low):
            # Locate the family after a CSS size and optional line-height.
            family = re.search(r'(?:\d*\.)?\d+(?:px|rem|em|%|pt)(?:\s*/\s*(?:\d*\.)?\d+(?:px|rem|em|%)?)?\s+(.+)$', value, re.I)
            if not family:
                yield 'font shorthand must use an approved font variable or family'
            else:
                yield from check_declaration('font-family', family[1])
    if prop.startswith('--k-font-'):
        yield from check_declaration('font-family', value)
    if prop == 'content' and EMOJI.search(value):
        yield 'emoji in generated visible text'


def lint_css(source, file='<css>', start_line=1, declarations=False):
    source = re.sub(r'/\*.*?\*/', blank, source, flags=re.S)
    issues = []
    # Braces and semicolons delimit declarations; nesting/media rules are handled
    # without treating selector pseudo-classes or strings as declarations.
    for chunk, offset in split_top(source, ';{}' if not declarations else ';'):
        match = re.match(r'\s*([\w-]+)\s*:\s*(.*?)\s*$', chunk, re.S)
        if not match:
            continue
        prop, value = match[1].lower(), match[2]
        line = start_line + source.count('\n', 0, offset + match.start(1))
        issues.extend(Violation(file, line, message) for message in check_declaration(prop, value))
    return issues


class PublicHTML(HTMLParser):
    VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, source, file):
        super().__init__(convert_charrefs=True)
        self.file = file
        self.stack = []
        self.issues = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        line = self.getpos()[0]
        if 'style' in attrs:
            # Attribute offsets, including multiline opening tags.
            raw = self.get_starttag_text()
            attr = re.search(r'\bstyle\s*=', raw, re.I)
            self.issues.extend(lint_css(attrs['style'], self.file,
                line + raw[:attr.start()].count('\n'), declarations=True))
        hidden = 'hidden' in attrs or tag in {'head', 'script', 'template'} or bool(self.stack and self.stack[-1][1])
        if re.search(r'\b(?:display\s*:\s*none|visibility\s*:\s*hidden)\b', attrs.get('style', ''), re.I):
            hidden = True
        if tag not in self.VOID:
            self.stack.append((tag, hidden))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        line = self.getpos()[0]
        if self.stack and self.stack[-1][0] == 'style':
            self.issues.extend(lint_css(data, self.file, line))
        elif not (self.stack and self.stack[-1][1]):
            for n, text in enumerate(data.splitlines()):
                if EMOJI.search(text):
                    self.issues.append(Violation(self.file, line+n, 'emoji in visible text'))


def lint_html(source, file='<html>'):
    return PublicHTML(source, file).issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1] / 'docs', help='public source tree (default: docs/)')
    root = parser.parse_args().root
    issues = []
    files = sorted(p for p in root.rglob('*') if p.suffix in {'.css', '.html'})
    if not files:
        print(f'{root}:1: no public CSS/HTML files found')
        return 1
    for path in files:
        file = str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path)
        source = path.read_text(encoding='utf-8')
        issues.extend((lint_css if path.suffix == '.css' else lint_html)(source, file))
    for issue in issues:
        print(issue)
    print(f'Editorial style lint: {len(files)} files, {len(issues)} violations')
    return bool(issues)


if __name__ == '__main__':
    sys.exit(main())
