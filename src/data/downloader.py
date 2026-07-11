from __future__ import annotations

import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


# ==============================================================================
# Exceptions
# ==============================================================================

class DownloadError(Exception):
    """Base exception for download-related errors."""


class DownloadFailedError(DownloadError):
    """Raised when a download fails."""


class InvalidURLError(DownloadError):
    """Raised when an invalid URL is provided."""


# ==============================================================================
# Downloader
# ==============================================================================

class Downloader:
    """
    Generic file downloader.

    Responsibilities
    ----------------
    - Download files from HTTP/HTTPS URLs.
    - Save files to disk.
    - Create destination directories if necessary.

    This class intentionally does NOT:
        - Verify checksums
        - Read configuration
        - Read dataset contents
    """

    DEFAULT_TIMEOUT = 30

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self._timeout = timeout

    def download(
        self,
        url: str,
        destination: str | Path,
        overwrite: bool = False,
    ) -> Path:
        """
        Download a file.

        Parameters
        ----------
        url:
            Remote HTTP/HTTPS URL.

        destination:
            Local file path.

        overwrite:
            If False and the file exists, skip download.

        Returns
        -------
        Path
            Path to downloaded file.
        """

        destination = Path(destination)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if destination.exists() and not overwrite:
            logger.info(
                "File already exists: %s",
                destination,
            )
            return destination

        logger.info("Downloading %s", url)

        try:
            response = requests.get(
                url,
                stream=True,
                timeout=self._timeout,
            )

            response.raise_for_status()

        except requests.exceptions.MissingSchema as exc:
            raise InvalidURLError(url) from exc

        except requests.exceptions.RequestException as exc:
            raise DownloadFailedError(
                f"Failed to download '{url}'."
            ) from exc

        try:
            with destination.open("wb") as fp:
                for chunk in response.iter_content(
                    chunk_size=8192
                ):
                    if chunk:
                        fp.write(chunk)

        except OSError as exc:
            raise DownloadFailedError(
                f"Failed writing '{destination}'."
            ) from exc

        logger.info(
            "Download completed: %s",
            destination,
        )

        return destination