# coffee_leaderboard/utils.py
import math
from coffee_leaderboard.database import UserProfile, CoffeeEntry


def generate_xp_table(base_level=700, factor=0.85):
    xp_next_level = base_level # baseline of 1 cup a day?
    max_level = 20
    xp_table = []   

    for i in range(1, max_level + 1):
        xp_table.append(xp_next_level)
        xp_next_level = int(xp_next_level * (1 + math.pow(factor, i)))

    return xp_table


XP_TABLE = generate_xp_table()


def calculate_streak_bonus(entry_date, entries):
    bonus = 0
    day = entry_date.day    

    # get last 7 days of entries
    last_days = [entry for entry in entries if 0 < (entry_date - entry.date).days <= 7]
    last_days = sorted(last_days, key=lambda entry: entry.date, reverse=True)    
    for entry in last_days:
        if bonus == 7:
            break
        if entry.date.day == day:
            continue
        elif entry.date.day - day > 1:
            # missing day, streak is over
            break

        # print(entry)

        day = entry.date.day
        bonus += 1

    return bonus


def calculate_xp_history(user_entries):
    """Calculates the total XP value of a series of entries."""
    total_xp = 0

    day_streak_bonus = 5

    for entry in user_entries:
        score = 100        
        was_late_entry = '-y' in entry.text or '--yesterday' in entry.text
        late_modifier = 0.25 if was_late_entry else 1.0        
        score = int(score * late_modifier)
        # late entries don't get any bonuses
        if not was_late_entry:
            cups_today = [en for en in user_entries if entry.date.date() == en.date.date()]
            cups_today = sorted(cups_today, key=lambda en: en.date)            
            was_first_of_date = entry == cups_today[0]
            if was_first_of_date:
                score += 10        

                day_streak = calculate_streak_bonus(entry.date, user_entries)
                streak_bonus = day_streak * day_streak_bonus
                score += streak_bonus


        total_xp += score

    return total_xp


def calculate_user_level(total_xp, xp_table):
    """Given an amount of XP, will calculate the level and prestige level."""
    prestige = 0
    level = 1
    xp_left = total_xp

    max_level_xp = xp_table[len(xp_table)-1]
    xp_next_level = xp_table[0]    

    prestige = math.floor(xp_left / max_level_xp)    
    remaining = xp_left % max_level_xp

    for i in range(0, len(xp_table)):
        if remaining < xp_table[i]:
            xp_next_level = xp_table[i]
            break
        level = i + 2

    return {
        'total_xp': total_xp,
        'level': level,        
        'current': remaining,
        'prestige': prestige
    }


def calculate_new_entry_xp(entry, user_entries):
    """Returns the XP earned for a new entry."""
    day_streak_bonus = 5
    score = 100
    was_late_entry = '-y' in entry.text or '--yesterday' in entry.text
    late_modifier = 0.25 if was_late_entry else 1.0
    score = int(score * late_modifier)
    # late entries don't get any bonuses
    if not was_late_entry:
        cups_today = [en for en in user_entries if entry.date.date() == en.date.date()]
        cups_today = sorted(cups_today, key=lambda en: en.date)
        was_first_of_date = len(cups_today) == 0 or entry == cups_today[0]
        if was_first_of_date:
            score += 10

            day_streak = calculate_streak_bonus(entry.date, user_entries)
            streak_bonus = day_streak * day_streak_bonus
            score += streak_bonus    

    return score
