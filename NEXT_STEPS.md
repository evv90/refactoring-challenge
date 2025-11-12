# Notes and next steps

## What I finished

- I organized the files in a python package that is installable with poetry
- I fixed two bugs that caused the original tests to fail
- I added a regression test to ensure that the refactoring would not change any behavior
- I added a github workflow to run the linters and tests
- I added a CLI and a nice way to read and write all the tabular input/output
- I refactored the main calculation loop

## What I would do next if I had more time

- I would expand the README
- I would continue with the "performance" task, I was pretty excited for that one, but I did not get to it
- I would add more unit tests to get full coverage
- I would add test coverage to the CI artifacts

## Risks/assumptions

- I assumed that the only two bugs in the code were the two annotated ones

## Notes

Github repo is at https://github.com/evv90/refactoring-challenge

I named the package `waqupy` and only read at the very end it should have been named `deltares_model`. My apologies!

I am not happy with the fact that there are two `Reach` objects: `Reach`, which gets updated by the calculation,
and `ReachRow` which is specifically for input/output. If I could use pydantic, or had more time, I could probably
make a more elegant solution.
