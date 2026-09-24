from logic_utils import check_guess, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# --- check_guess: hint messages ---

def test_winning_guess_message():
    outcome, message = check_guess(50, 50)
    assert message == "🎉 Correct!"

def test_guess_too_high_message():
    outcome, message = check_guess(60, 50)
    assert message == "📉 Go LOWER!"

def test_guess_too_low_message():
    outcome, message = check_guess(40, 50)
    assert message == "📈 Go HIGHER!"


# --- check_guess: edge cases ---

def test_guess_one_above_secret():
    # Off-by-one above should still read as "Too High"
    outcome, message = check_guess(51, 50)
    assert outcome == "Too High"

def test_guess_one_below_secret():
    # Off-by-one below should still read as "Too Low"
    outcome, message = check_guess(49, 50)
    assert outcome == "Too Low"

def test_guess_at_range_boundary_low():
    # Guessing the minimum possible value, when it's also the secret
    outcome, message = check_guess(1, 1)
    assert outcome == "Win"

# --- parse_guess: valid input ---

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("50", 1, 100)
    assert ok is True
    assert value == 50
    assert err is None

def test_parse_guess_valid_boundary_values():
    ok_low, value_low, err_low = parse_guess("1", 1, 100)
    ok_high, value_high, err_high = parse_guess("100", 1, 100)
    assert (ok_low, value_low) == (True, 1)
    assert (ok_high, value_high) == (True, 100)

def test_parse_guess_truncates_decimal_input():
    # "." branch runs int(float(raw)), which truncates rather than rounds
    ok, value, err = parse_guess("50.9", 1, 100)
    assert ok is True
    assert value == 50


# --- parse_guess: invalid input ---

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_none_input():
    ok, value, err = parse_guess(None, 1, 100)
    assert ok is False
    assert err == "Enter a guess."

def test_parse_guess_non_numeric_string():
    ok, value, err = parse_guess("abc", 1, 100)
    assert ok is False
    assert value is None
    assert err == "That is not a number."

def test_parse_guess_below_range():
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert err == "Enter a number between 1 and 100."

def test_parse_guess_above_range():
    ok, value, err = parse_guess("101", 1, 100)
    assert ok is False
    assert value is None
    assert err == "Enter a number between 1 and 100."

def test_parse_guess_respects_custom_range():
    # Difficulty-specific ranges (e.g. Easy = 1-20) should be enforced too
    ok, value, err = parse_guess("21", 1, 20)
    assert ok is False
    assert err == "Enter a number between 1 and 20."


# --- update_score: parity regression (planted bug alternated behavior on attempt_number % 2) ---

def test_update_score_too_high_on_odd_attempt():
    assert update_score(100, "Too High", 1) == 95

def test_update_score_too_high_on_even_attempt():
    # Previously, even attempt numbers incorrectly added points instead of deducting them
    assert update_score(100, "Too High", 2) == 95

def test_update_score_too_low_on_odd_attempt():
    assert update_score(100, "Too Low", 1) == 95

def test_update_score_too_low_on_even_attempt():
    assert update_score(100, "Too Low", 2) == 95

def test_update_score_too_high_consistent_across_many_attempts():
    # Guard against any reintroduced even/odd branching: every attempt number,
    # regardless of parity, should deduct the same 5 points.
    for attempt_number in range(10):
        assert update_score(100, "Too High", attempt_number) == 95

def test_update_score_alternating_wrong_guesses_only_ever_lose_points():
    # Simulate a run of alternating "Too High"/"Too Low" guesses across
    # several attempts and confirm the score strictly decreases each time.
    score = 100
    outcomes = ["Too High", "Too Low", "Too High", "Too Low", "Too High"]
    for attempt_number, outcome in enumerate(outcomes):
        previous_score = score
        score = update_score(score, outcome, attempt_number)
        assert score == previous_score - 5

def test_update_score_win_ignores_attempt_parity_for_point_formula():
    # The win-scoring formula depends on attempt_number by design (more attempts,
    # fewer points), not on its parity - odd and even attempts with the same
    # attempt_number should behave identically to their counterparts.
    assert update_score(0, "Win", 0) == 90
    assert update_score(0, "Win", 1) == 80
    assert update_score(0, "Win", 2) == 70
    assert update_score(0, "Win", 3) == 60
