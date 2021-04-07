""" Implementation of histogram-based data population method. """
import numpy as np

def generate_rand_from_pdf(pdf, x_grid, count):
    """ Populates data based on the given distribution (histogram).

    Example:
    ```
    hists, bins = np.histogram(orig_data, bins=50)
    bin_midpoints = bins[:-1] + [np.diff(bins[:-1])[0]/2] * 50
    popu_data = generate_rand_from_pdf(hists, bin_midpoints, count)
    ```

    Args:
        pdf: given data distribution.
        x_grid: location of the bar to draw from.
        count: number of data points to populate.
    Returns:
        A list of populated data.
    """
    cdf = np.cumsum(pdf)
    cdf = cdf / cdf[-1]
    values = np.random.rand(count)
    value_bins = np.searchsorted(cdf, values)

    random_from_cdf = x_grid[value_bins]

    return random_from_cdf
