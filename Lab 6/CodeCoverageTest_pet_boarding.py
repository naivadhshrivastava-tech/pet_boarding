import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# --- boarding_fee tests ---

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
    # premium with rabbit does NOT increase included days (pet_type != "rabbit" is False)
    # rabbit included = 4, days = 4 -> extra = 0 -> 0
    assert boarding_fee("rabbit", 4, True) == 0


def test_boarding_fee_included_days_premium_cat():
    # premium with cat increases included days: 3 + 1 = 4
    # days = 4 -> extra = 0 -> 0
    assert boarding_fee("cat", 4, True) == 0


def test_boarding_fee_cat_normal_rate():
    # cat: included = 3, days = 5 -> extra = 2, rate = 20, extra <= 10 -> 2 * 20 = 40
    assert boarding_fee("cat", 5, False) == 40


def test_boarding_fee_dog_normal_rate():
    # dog: included = 2, days = 5 -> extra = 3, rate = 30, extra <= 10 -> 3 * 30 = 90
    assert boarding_fee("dog", 5, False) == 90


def test_boarding_fee_cat_extended_rate():
    # cat: included = 3, days = 15 -> extra = 12 (> 10) -> rate = 20 + 10 = 30 -> 12 * 30 = 360
    assert boarding_fee("cat", 15, False) == 360


def test_boarding_fee_dog_extended_rate():
    # dog: included = 2, days = 15 -> extra = 13 (> 10) -> rate = 30 + 10 + 5 = 45 -> 13 * 45 = 585
    assert boarding_fee("dog", 15, False) == 585


# --- admission_ok tests ---

def test_admission_senior_pass():
    assert admission_ok(10, 3, True) is True


def test_admission_senior_fail():
    assert admission_ok(10, 2, True) is False


def test_admission_young_pet():
    # pet_age_years < 1 -> False
    assert admission_ok(0.5, 5, False) is False


def test_admission_adult_pet_pass():
    # pet_age_years >= 1 and vaccinations >= 2 -> True
    assert admission_ok(2, 2, False) is True


def test_admission_adult_pet_fail():
    # pet_age_years >= 1 and vaccinations < 2 -> False
    assert admission_ok(2, 1, False) is False


# --- checkout_status tests ---

def test_checkout_status_long_stay_weekend_open():
    # long stay (cutoff=30), weekend (+20 => 50), minutes_left 50 >= 50 -> "open"
    assert checkout_status(50, True, True) == "open"


def test_checkout_status_long_stay_weekday_late():
    # long stay (cutoff=30), weekday (+0 => 30), minutes_left 20 (>= 15, < 30) -> "late"
    assert checkout_status(20, True, False) == "late"


def test_checkout_status_short_stay_weekday_closed():
    # short stay (cutoff=15), weekday (+0 => 15), minutes_left -1 (< 0) -> "closed"
    assert checkout_status(-1, False, False) == "closed"


def test_checkout_status_short_stay_weekend_late():
    # short stay (cutoff=15), weekend (+20 => 35), minutes_left 25 (>= 20, < 35) -> "late"
    assert checkout_status(25, False, True) == "late"
