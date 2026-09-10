# Blackjack

A console blackjack game in Python. Started from a basic tutorial
implementation and extended it with split logic and a proper
betting system, since the base version didn't have either.

## What it does

- Real 52-card deck, no replacement, reshuffles automatically when it runs out
- Correct handling of soft/hard totals (multiple aces demote properly)
- Splitting on any pair, including split aces (which get exactly one
  card each and can't be hit further - that one tripped me up initially,
  since it's easy to forget aces are a special case)
- 3:2 blackjack payout, with the rule that a blackjack from a split
  hand doesn't get the bonus payout
- Betting with min/max limits and balance tracking across rounds
- Input validation everywhere so bad input doesn't crash the game

## How I built it

I started with a plain hit-or-stand blackjack skeleton and added the
split and betting logic myself. I used AI assistance along the way -
mainly to help restructure the code more cleanly and to pressure-test
the split/ace edge cases, since those are easy to get subtly wrong
(e.g. what happens if you split aces and then bust, or what happens
to blackjack payout eligibility after a split). The rules and payout
decisions are mine; I ran through a bunch of manual test rounds to
check dealer bust cases, pushes, and split outcomes before calling
it done.


## What's not in here yet

No double down, insurance, surrender, or re-splitting. Wanted to get
the core rules solid first before adding more.
