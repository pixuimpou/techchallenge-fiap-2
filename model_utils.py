import numpy as np


def split_x_y(data, timesteps):
    return data[:, : timesteps - 1], data[:, [timesteps - 1]]


def aggregate_data_in_timesteps(data, timesteps):
    return np.array(
        [
            [j for j in data[i : i + timesteps]]
            for i in range(0, len(data) - timesteps + 1)
        ]
    )
