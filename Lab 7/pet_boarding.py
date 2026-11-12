import math

def parse_booking(text):
    if not isinstance(text, str):
        return None, 0.0
    text = text.strip()
    if not text:
        return None, 0.0
    parts = text.split(':')
    if len(parts) != 2:
        return None, 0.0
    pet_str, days_str = parts[0].strip(), parts[1].strip()
    if not pet_str:
        return None, 0.0
    try:
        days = float(days_str)
        if math.isnan(days) or math.isinf(days) or days < 0:
            return None, 0.0
    except (ValueError, TypeError):
        return None, 0.0
    return pet_str.title(), days


def stay_average(days_csv):
    if not isinstance(days_csv, str):
        return 0
    days_csv = days_csv.strip()
    if not days_csv:
        return 0
    parts = [p.strip() for p in days_csv.split(',') if p.strip()]
    if not parts:
        return 0
    valid_nums = []
    for r in parts:
        try:
            val = int(r)
            if val >= 0:
                valid_nums.append(val)
        except (ValueError, TypeError):
            continue
    if not valid_nums:
        return 0
    return sum(valid_nums) // len(valid_nums)


def payable_fee(text):
    if not isinstance(text, str):
        return 0.0
    text = text.strip()
    if not text:
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    fee_str, discount_str = parts[0].strip(), parts[1].strip()
    try:
        fee = float(fee_str)
        discount = float(discount_str)
        if math.isnan(fee) or math.isinf(fee) or fee < 0:
            return 0.0
        if math.isnan(discount) or math.isinf(discount) or discount < 0:
            discount = 0.0
        total = fee * 1.18 - discount
        return round(max(total, 0.0), 2)
    except (ValueError, TypeError):
        return 0.0


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result)

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
