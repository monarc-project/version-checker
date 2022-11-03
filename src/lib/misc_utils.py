#! /usr/bin/env python
import logging
from io import BytesIO
from io import StringIO
from urllib.parse import urljoin
from urllib.parse import urlparse

from csvalidate import ValidatedWriter
from flask import request
from flask import send_file


logger = logging.getLogger(__name__)


def is_safe_url(target):
    """
    Ensures that a redirect target will lead to the same server.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def get_redirect_target():
    """
    Looks at various hints to find the redirect target.
    """
    for target in request.args.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def send_csv(
    iterable,
    filename,
    fields=None,
    schema=None,
    delimiter=",",
    encoding="utf-8",
    writer_kwargs=None,
    **kwargs
):
    buf = StringIO()
    writer_cls = ValidatedWriter
    if schema:
        writer_cls = ValidatedWriter.from_schema(schema)
    writer_kwargs = writer_kwargs or {}
    writer = writer_cls(buf, fields, delimiter=delimiter, **writer_kwargs)
    writer.writeheader()
    for line in iterable:
        writer.writerow(line)
    buf.seek(0)
    buf = BytesIO(buf.read().encode(encoding))
    mimetype = "Content-Type: text/csv; charset=" + encoding

    return send_file(
        buf, download_name=filename, as_attachment=True, mimetype=mimetype, **kwargs
    )
