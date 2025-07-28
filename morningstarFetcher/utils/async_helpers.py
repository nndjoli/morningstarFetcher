"""Utility helpers for running asynchronous coroutines."""

from __future__ import annotations

import asyncio


def run_async(coro):
    """Execute an async coroutine synchronously.

    This helper enables calling asynchronous functions from synchronous code
    by applying :func:`nest_asyncio.apply` and then using :func:`asyncio.run`.
    """
    import nest_asyncio

    nest_asyncio.apply()
    return asyncio.run(coro)


__all__ = ["run_async"]
