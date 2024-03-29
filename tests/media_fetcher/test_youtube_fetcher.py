from contextlib import nullcontext as does_not_raise
from pathlib import Path

from services.media_manager.modules.youtube import ContentDownloader
from services.media_manager.core.settings import get_settings

import pytest

settings = get_settings()


@pytest.fixture(scope='session', autouse=True)
def run_around_tests():
    yield
    for p in Path(settings.path_to_download).glob(f"*.{settings.source_file_ext}"):  # noqa
        p.unlink()


@pytest.mark.parametrize(
    "link,expectation",
    [
        ("https://www.youtube.com/watch?v=tK7uXkZ-EFM", does_not_raise()),
        ("https://www.youtube.com/watch?v=UBS52IgUDZ0", does_not_raise()),
        ("https://www.youtube.com/watch?v=W9RCD7gML8o", does_not_raise()),
        ("https://www.youtube.com/watch?v=CTwiB1uw9sQ", does_not_raise()),
    ],
)
def test_download_success(link, expectation):
    f = ContentDownloader(settings=settings)
    with expectation as e:
        f.download(link)

    assert e is None
