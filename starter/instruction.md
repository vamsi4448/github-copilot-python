# Sudoku Project Instructions

## Project Goal

Refactor the legacy Python Flask Sudoku application into a modern,
maintainable, responsive, and accessible Sudoku game.

## Technology

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- Browser localStorage
- pytest for testing

## Code Style

- Use clean, readable, and maintainable Python code.
- Follow PEP 8 conventions.
- Use descriptive variable and function names.
- Keep functions small and focused on one responsibility.
- Avoid duplicated code.
- Use reusable helper functions.
- Add comments only when they provide useful context.
- Handle errors gracefully.

## Application Structure

Keep Sudoku game logic separate from Flask routes and presentation.

Prefer a structure similar to:

app.py
sudoku_logic.py
templates/
static/
tests/
Screenshots/

## Sudoku Requirements

The application must:

- Generate valid Sudoku puzzles.
- Ensure every generated puzzle has exactly one solution.
- Support Easy, Medium, and Hard difficulty levels.
- Lock all prefilled cells.
- Detect invalid user entries.
- Provide immediate feedback for invalid moves.
- Detect successful puzzle completion.

## Game Features

Implement:

- Difficulty selector
- New Game button
- Check button
- Hint button
- Timer
- Top 10 leaderboard
- Player name
- Difficulty display
- Hint count
- Dark/light mode toggle

## Leaderboard

Use browser localStorage to persist the Top 10 scores.

Each score should contain:

- Player name
- Completion time
- Difficulty
- Number of hints

Only keep the best 10 scores.

## UI Requirements

The interface should:

- Work in light and dark modes.
- Work on desktop and mobile.
- Have responsive sizing.
- Keep controls readable.
- Use alternating styling for the 3x3 Sudoku boxes.
- Provide clear visual feedback.
- Support keyboard navigation where practical.
- Use accessible labels and buttons.

## Testing

Use pytest for backend and Sudoku logic tests.

Run tests with:

pytest

All existing tests should pass before and after refactoring.

New functionality should be tested where practical.

## Git Practices

Make focused commits.

Do not overwrite working functionality unnecessarily.

Before making major changes:

1. Understand the existing implementation.
2. Run the tests.
3. Make the smallest reasonable change.
4. Run the tests again.
5. Review the result.

## GitHub Copilot Usage

Use GitHub Copilot as an assistant rather than blindly accepting suggestions.

For generated code:

- Review the suggestion.
- Check whether it meets the requirements.
- Reject or modify suggestions that are incorrect.
- Ask Copilot to explain unfamiliar code.
- Prefer simple and maintainable solutions.

Do not introduce unnecessary frameworks or dependencies.

## Important Project Rule

Preserve existing functionality while adding new functionality.

Run tests after every major change.