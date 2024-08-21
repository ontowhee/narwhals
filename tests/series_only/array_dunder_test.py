from typing import Any

import numpy as np
import pandas as pd
import pyarrow as pa
import pytest

import narwhals.stable.v1 as nw
from narwhals.utils import parse_version
from tests.utils import compare_dicts


def test_array_dunder(request: Any, constructor_eager: Any) -> None:
    if "pyarrow_table" in str(constructor_eager) and parse_version(
        pa.__version__
    ) < parse_version("16.0.0"):  # pragma: no cover
        request.applymarker(pytest.mark.xfail)

    s = nw.from_native(constructor_eager({"a": [1, 2, 3]}), eager_only=True)["a"]
    result = s.__array__()
    np.testing.assert_array_equal(result, np.array([1, 2, 3], dtype="int64"))


def test_array_dunder_with_dtype(request: Any, constructor_eager: Any) -> None:
    if "pyarrow_table" in str(constructor_eager) and parse_version(
        pa.__version__
    ) < parse_version("16.0.0"):  # pragma: no cover
        request.applymarker(pytest.mark.xfail)

    s = nw.from_native(constructor_eager({"a": [1, 2, 3]}), eager_only=True)["a"]
    result = s.__array__(object)
    np.testing.assert_array_equal(result, np.array([1, 2, 3], dtype=object))


def test_array_dunder_with_copy(request: Any, constructor_eager: Any) -> None:
    if "pyarrow_table" in str(constructor_eager) and parse_version(
        pa.__version__
    ) < parse_version("16.0.0"):  # pragma: no cover
        request.applymarker(pytest.mark.xfail)

    s = nw.from_native(constructor_eager({"a": [1, 2, 3]}), eager_only=True)["a"]
    result = s.__array__(copy=True)
    np.testing.assert_array_equal(result, np.array([1, 2, 3], dtype="int64"))
    if "pandas_constructor" in str(constructor_eager) and parse_version(
        pd.__version__
    ) < (3,):
        # If it's pandas, we know that `copy=False` definitely took effect.
        # So, let's check it!
        result = s.__array__(copy=False)
        np.testing.assert_array_equal(result, np.array([1, 2, 3], dtype="int64"))
        result[0] = 999
        compare_dicts({"a": s}, {"a": [999, 2, 3]})
