"""Small shared helpers."""
from datetime import datetime, timezone

import bleach


def utcnow():
    """Return the current UTC time as a naive datetime.

    Behaviour-identical to the deprecated ``datetime.utcnow()`` (naive UTC), but
    built on the non-deprecated ``datetime.now(timezone.utc)``. Kept naive so it
    stays consistent with the naive ``DateTime`` columns stored by SQLAlchemy.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


# Tags/attributes permitted in authored module content. Covers the markup used
# by the seeded modules (sections, headings, lists, code blocks, tables) while
# stripping anything script-capable (script, style, iframe, event handlers).
ALLOWED_TAGS = [
    'section', 'article', 'div', 'span', 'p', 'br', 'hr',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'strong', 'b', 'em', 'i', 'u', 'small', 'mark', 'sub', 'sup',
    'code', 'pre', 'kbd', 'samp', 'blockquote', 'a',
    'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td', 'caption',
    'figure', 'figcaption', 'img',
]
ALLOWED_ATTRS = {
    '*': ['class', 'id', 'title'],
    'a': ['href', 'target', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
    'td': ['colspan', 'rowspan'],
    'th': ['colspan', 'rowspan', 'scope'],
}
ALLOWED_PROTOCOLS = ['http', 'https', 'mailto', 'data']


def sanitize_html(raw):
    """Sanitize authored module HTML, stripping script-capable markup.

    Returns clean HTML safe to render with Jinja's ``| safe``. Disallowed tags
    are removed entirely (``strip=True``) rather than escaped, so trusted
    formatting survives while ``<script>``/event handlers do not.
    """
    if not raw:
        return ''
    return bleach.clean(
        raw,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
