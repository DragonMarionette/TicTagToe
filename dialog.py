def from_intdict(d: dict[int, any], prompt: str = None):
    if prompt is not None:
        print(prompt)
    for i, v in sorted(d.items()):
        print(f'{i}: {v}')
    selection_num = validate_int(lowest=min(d), highest=max(d))
    return selection_num, d[selection_num]


def validate_int(prompt: str = 'Please select: ', lowest: int = None, highest: int = None):
    if lowest is None:
        lowest = float('-inf')
    if highest is None:
        highest = float('inf')

    result = None
    while result is None:
        try:
            result = int(input(prompt))
            if not lowest <= result <= highest:
                print(f'Input must bee between {lowest} and {highest}. Please try again')
                result = None
        except ValueError:
            print(f'Input must be a number{f" from {lowest} to {highest}"}. Please try again')
    return result
