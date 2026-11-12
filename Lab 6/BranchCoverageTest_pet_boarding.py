import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status

# ==============================================================================
# 1. Tests for boarding_fee(pet_type, days, is_premium)
# ==============================================================================

# Branch: if pet_type not in INCLUDED_DAYS (True / False)
def test_boarding_fee_pet_type_invalid():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("parrot", 5, False)

# Branch: if days < 0 (True / False)
def test_boarding_fee_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -2, False)

# Branch: if is_premium and pet_type != "rabbit"
# Sub-case A: is_premium=True, pet_type="dog" (True and True -> True: included becomes 3)
def test_boarding_fee_premium_non_rabbit():
    # Dog included: 2 + 1 = 3. days = 3 -> extra = 0
    assert boarding_fee("dog", 3, True) == 0

# Sub-case B: is_premium=True, pet_type="rabbit" (True and False -> False: included stays 4)
def test_boarding_fee_premium_rabbit():
    # Rabbit included stays 4. days = 4 -> extra = 0
    assert boarding_fee("rabbit", 4, True) == 0

# Sub-case C: is_premium=False, pet_type="cat" (False and True -> False: included stays 3)
def test_boarding_fee_standard_cat():
    # Cat included stays 3. days = 3 -> extra = 0
    assert boarding_fee("cat", 3, False) == 0

# Branch: if extra <= 0 (True / False)
def test_boarding_fee_within_included_days():
    # extra < 0: cat (included 3), days = 2 -> extra = -1 <= 0 -> 0
    assert boarding_fee("cat", 2, False) == 0

# Branch: if pet_type == "dog" -> rate = 30 else rate = 20
# and Branch: if extra > 10 (False)
def test_boarding_fee_dog_standard_extra():
    # dog (included 2), days = 5 -> extra = 3 (<= 10), rate = 30 -> 3 * 30 = 90
    assert boarding_fee("dog", 5, False) == 90

def test_boarding_fee_cat_standard_extra():
    # cat (included 3), days = 5 -> extra = 2 (<= 10), rate = 20 -> 2 * 20 = 40
    assert boarding_fee("cat", 5, False) == 40

# Branch: if extra > 10 (True) with pet_type == "dog" (True) -> rate + 10 + 5
def test_boarding_fee_dog_extended_stay():
    # dog (included 2), days = 14 -> extra = 12 (> 10), rate = 30 + 10 + 5 = 45 -> 12 * 45 = 540
    assert boarding_fee("dog", 14, False) == 540

# Branch: if extra > 10 (True) with pet_type != "dog" (False) -> rate + 10
def test_boarding_fee_rabbit_extended_stay():
    # rabbit (included 4), days = 15 -> extra = 11 (> 10), rate = 20 + 10 = 30 -> 11 * 30 = 330
    assert boarding_fee("rabbit", 15, False) == 330


# ==============================================================================
# 2. Tests for admission_ok(pet_age_years, vaccinations, is_senior)
# ==============================================================================

# Branch: if is_senior (True) -> return vaccinations >= 3 (True / False)
def test_admission_senior_vaccinated():
    assert admission_ok(10, 3, True) is True

def test_admission_senior_under_vaccinated():
    assert admission_ok(10, 2, True) is False

# Branch: if is_senior (False) -> if pet_age_years < 1 (True / False)
def test_admission_non_senior_infant():
    assert admission_ok(0.8, 4, False) is False

# Branch: non-senior, age >= 1 -> return vaccinations >= 2 (True / False)
def test_admission_non_senior_adult_vaccinated():
    assert admission_ok(3, 2, False) is True

def test_admission_non_senior_adult_under_vaccinated():
    assert admission_ok(3, 1, False) is False


# ==============================================================================
# 3. Tests for checkout_status(minutes_left, is_long_stay, is_weekend)
# ==============================================================================

# Branch: if is_long_stay (True -> cutoff = 30; False -> cutoff = 15)
# Branch: if is_weekend (True -> cutoff += 20; False -> no change)
# Branch: if minutes_left >= cutoff (True -> "open")
# Branch: elif minutes_left >= cutoff - 15 (True -> "late"; False -> "closed")

def test_checkout_long_stay_weekend_open():
    # cutoff = 30 + 20 = 50. minutes_left = 50 >= 50 -> "open"
    assert checkout_status(50, True, True) == "open"

def test_checkout_long_stay_weekend_late():
    # cutoff = 50. minutes_left = 40 (>= 35 and < 50) -> "late"
    assert checkout_status(40, True, True) == "late"

def test_checkout_long_stay_weekend_closed():
    # cutoff = 50. minutes_left = 34 (< 35) -> "closed"
    assert checkout_status(34, True, True) == "closed"

def test_checkout_short_stay_weekday_open():
    # cutoff = 15 + 0 = 15. minutes_left = 15 >= 15 -> "open"
    assert checkout_status(15, False, False) == "open"

def test_checkout_short_stay_weekday_late():
    # cutoff = 15. minutes_left = 0 (>= 0 and < 15) -> "late"
    assert checkout_status(0, False, False) == "late"

def test_checkout_short_stay_weekday_closed():
    # cutoff = 15. minutes_left = -1 (< 0) -> "closed"
    assert checkout_status(-1, False, False) == "closed"
