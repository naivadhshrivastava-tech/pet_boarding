import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ==============================================================================
# 1. Tests for boarding_fee(pet_type, days, is_premium)
# ==============================================================================

def test_boarding_fee_unknown_pet():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("bird", 3, False)


def test_boarding_fee_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("dog", -1, False)


def test_boarding_fee_within_included_days():
    # included for dog is 2; days = 1 -> extra <= 0 -> 0
    assert boarding_fee("dog", 1, False) == 0


def test_boarding_fee_included_days_premium_rabbit():
    # premium with rabbit does not increase included days
    assert boarding_fee("rabbit", 4, True) == 0


def test_boarding_fee_included_days_premium_cat():
    # premium with cat increases included days: 3 + 1 = 4
    assert boarding_fee("cat", 4, True) == 0


def test_boarding_fee_cat_normal_rate():
    # cat: included = 3, days = 5 -> extra = 2, rate = 20 -> 40
    assert boarding_fee("cat", 5, False) == 40


def test_boarding_fee_dog_normal_rate():
    # dog: included = 2, days = 5 -> extra = 3, rate = 30 -> 90
    assert boarding_fee("dog", 5, False) == 90


def test_boarding_fee_cat_extended_rate():
    # cat: included = 3, days = 15 -> extra = 12 (> 10) -> rate = 20 + 10 = 30 -> 360
    assert boarding_fee("cat", 15, False) == 360


def test_boarding_fee_dog_extended_rate():
    # dog: included = 2, days = 15 -> extra = 13 (> 10) -> rate = 30 + 10 + 5 = 45 -> 585
    assert boarding_fee("dog", 15, False) == 585


# ==============================================================================
# 2. Tests for admission_ok(pet_age_years, vaccinations, is_senior)
# ==============================================================================

def test_admission_senior_pass():
    assert admission_ok(10, 3, True) is True


def test_admission_senior_fail():
    assert admission_ok(10, 2, True) is False


def test_admission_young_pet():
    assert admission_ok(0.5, 5, False) is False


def test_admission_adult_pet_pass():
    assert admission_ok(2, 2, False) is True


def test_admission_adult_pet_fail():
    assert admission_ok(2, 1, False) is False


# ==============================================================================
# 3. Tests for checkout_status(minutes_left, is_long_stay, is_weekend)
# ==============================================================================

def test_checkout_status_long_stay_weekend_open():
    assert checkout_status(50, True, True) == "open"


def test_checkout_status_long_stay_weekend_late():
    assert checkout_status(40, True, True) == "late"


def test_checkout_status_long_stay_weekend_closed():
    assert checkout_status(34, True, True) == "closed"


def test_checkout_status_short_stay_weekday_open():
    assert checkout_status(15, False, False) == "open"


def test_checkout_status_short_stay_weekday_late():
    assert checkout_status(5, False, False) == "late"


def test_checkout_status_short_stay_weekday_closed():
    assert checkout_status(-1, False, False) == "closed"
