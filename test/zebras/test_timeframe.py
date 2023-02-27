# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

import pytest

import numpy as np

from gluonts import zebras as zb


target = np.arange(10)
feat = np.arange(20).reshape(2, 10)
static = np.arange(3)
index = zb.periods("2020", "D", 10)

tf = zb.time_frame(
    {"target": target, "feat": feat},
    static={"static": static},
    index=index,
    metadata={"x": 42},
)


def test_time_frame():
    assert len(tf) == 10
    assert len(tf[:4]) == 4
    assert len(tf[-4:]) == 4

    assert np.array_equal(tf["target"], target)
    assert np.array_equal(tf["feat"], feat)

    assert tf.metadata == {"x": 42}

    tf2 = tf.stack(["target", "feat"], "stacked")
    assert tf2.columns["stacked"].shape == (3, 10)
    assert tf2.columns["stacked"].shape == (3, 10)
    assert "target" not in tf2.columns
    assert "feat" not in tf2.columns
    assert tf2.metadata == {"x": 42}

    tf3 = tf.like({"foo": np.full(10, 7)})
    assert tf3.columns["foo"].shape == (10,)
    assert "target" not in tf3.columns
    assert "feat" not in tf3.columns
    assert tf3.metadata == {"x": 42}


@pytest.mark.parametrize("split_index", [4, -6, index[4]])
def test_time_frame_split(split_index):
    sf = tf.split(split_index)
    assert len(sf) == 10
    assert len(sf.past) == 4
    assert len(sf.future) == 6
    assert sf.metadata == {"x": 42}

    sf = tf.split(split_index, past_length=2, future_length=2)
    assert len(sf) == 4
    assert len(sf.past) == 2
    assert len(sf.future) == 2
    assert np.array_equal(tf.static, sf.static)
    assert sf.metadata == {"x": 42}

    sf = tf.split(split_index, past_length=5, future_length=8)
    assert len(sf.past) == 5
    assert len(sf.future) == 8
    assert np.array_equal(tf.static, sf.static)
    assert sf.metadata == {"x": 42}