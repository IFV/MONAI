# Copyright 2020 MONAI Consortium
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import numpy as np
import torch
from parameterized import parameterized

from monai.transforms import Rand3DElastic

TEST_CASES = [
    [
        {
            "magnitude_range": (0.3, 2.3),
            "sigma_range": (1.0, 20.0),
            "prob": 0.0,
            "as_tensor_output": False,
            "device": None,
            "spatial_size": -1,
        },
        {"img": torch.arange(72).reshape((2, 3, 3, 4))},
        np.arange(72).reshape((2, 3, 3, 4)),
    ],
    [
        {
            "magnitude_range": (0.3, 2.3),
            "sigma_range": (1.0, 20.0),
            "prob": 0.0,
            "as_tensor_output": False,
            "device": None,
        },
        {"img": torch.ones((2, 3, 3, 3)), "spatial_size": (2, 2, 2)},
        np.ones((2, 2, 2, 2)),
    ],
    [
        {
            "magnitude_range": (0.3, 0.3),
            "sigma_range": (1.0, 2.0),
            "prob": 0.9,
            "as_tensor_output": False,
            "device": None,
        },
        {"img": torch.arange(27).reshape((1, 3, 3, 3)), "spatial_size": (2, 2, 2)},
        np.array([[[[6.492354, 7.5022864], [9.519528, 10.524366]], [[15.51277, 16.525297], [18.533852, 19.539217]]]]),
    ],
    [
        {
            "magnitude_range": (0.3, 0.3),
            "sigma_range": (1.0, 2.0),
            "prob": 0.9,
            "rotate_range": [1, 1, 1],
            "as_tensor_output": False,
            "device": None,
            "spatial_size": (2, 2, 2),
        },
        {"img": torch.arange(27).reshape((1, 3, 3, 3)), "mode": "bilinear"},
        np.array([[[[5.005563, 9.463698], [9.289501, 13.741863]], [[12.320587, 16.779654], [16.597677, 21.049414]]]]),
    ],
]


class TestRand3DElastic(unittest.TestCase):
    @parameterized.expand(TEST_CASES)
    def test_rand_3d_elastic(self, input_param, input_data, expected_val):
        g = Rand3DElastic(**input_param)
        g.set_random_state(123)
        result = g(**input_data)
        self.assertEqual(torch.is_tensor(result), torch.is_tensor(expected_val))
        if torch.is_tensor(result):
            np.testing.assert_allclose(result.cpu().numpy(), expected_val.cpu().numpy(), rtol=1e-4, atol=1e-4)
        else:
            np.testing.assert_allclose(result, expected_val, rtol=1e-4, atol=1e-4)


if __name__ == "__main__":
    unittest.main()
