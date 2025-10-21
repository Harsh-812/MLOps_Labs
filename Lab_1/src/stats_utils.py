def mean(numbers):
    """
    Calculates the mean (average) of a list of numbers.
    Args:
        numbers (list of int/float): Input numbers.
    Returns:
        float: The mean of the numbers.
    Raises:
        ValueError: If the input is empty or contains non-numeric values.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All elements must be numbers.")
    return sum(numbers) / len(numbers)


def median(numbers):
    """
    Calculates the median of a list of numbers.
    Args:
        numbers (list of int/float): Input numbers.
    Returns:
        float: The median of the numbers.
    Raises:
        ValueError: If the input is empty or contains non-numeric values.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All elements must be numbers.")
    
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        return sorted_nums[mid]


def mode(numbers):
    """
    Calculates the mode of a list of numbers.
    Args:
        numbers (list of int/float): Input numbers.
    Returns:
        int/float: The mode (most frequent element).
    Raises:
        ValueError: If the input is empty or contains non-numeric values.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All elements must be numbers.")
    
    freq = {}
    for n in numbers:
        freq[n] = freq.get(n, 0) + 1
    max_count = max(freq.values())
    for k, v in freq.items():
        if v == max_count:
            return k


def variance(numbers):
    """
    Calculates the variance of a list of numbers.
    Args:
        numbers (list of int/float): Input numbers.
    Returns:
        float: The variance of the numbers.
    Raises:
        ValueError: If the input is empty or contains non-numeric values.
    """
    if not numbers:
        raise ValueError("Input list cannot be empty.")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise ValueError("All elements must be numbers.")

    m = mean(numbers)
    return sum((x - m) ** 2 for x in numbers) / len(numbers)

