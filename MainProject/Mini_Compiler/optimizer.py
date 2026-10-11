# optimizer.py

def optimize_icode(icode):
    """
    Simple optimizer:
    - Constant folding
    - Remove useless initializations
    """

    values = {}
    optimized = []

    for line in icode:

        # Skip lines without assignment
        if '=' not in line:
            optimized.append(line)
            continue

        left, right = line.split('=', 1)
        left = left.strip()
        right = right.strip()

        # Replace known constants
        for var, val in values.items():
            right = right.replace(var, str(val))

        try:
            # Evaluate if possible
            result = eval(right)
            values[left] = result
            optimized.append(f"{left} = {result}")
        except:
            optimized.append(f"{left} = {right}")

    # Remove useless initializations (x = 0 if reassigned later)
    final_code = []
    assigned_again = set()
    for line in optimized[::-1]:
        left = line.split('=')[0].strip()
        if left in assigned_again and line.endswith("= 0"):
            continue
        assigned_again.add(left)
        final_code.append(line)
    final_code.reverse()
    return final_code