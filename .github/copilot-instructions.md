<!-- Copilot / AI agent instructions for the BMI Calculator repo -->
# Repository snapshot

- This is a small Python GUI app (Tkinter) implementing a BMI calculator. The main UI and behavior live in [Python-Task2-BMICalculator/main.py](Python-Task2-BMICalculator/main.py#L1-L100).
- There are no external dependencies beyond the Python standard library (Tkinter).

# Primary goal for agents

- Make targeted, minimal changes that preserve the single-file GUI structure unless the user asks to refactor.
- Prefer adding clear input validation, wiring the `Calculate` button callback, and providing user feedback (label or messagebox).

# Key files and patterns

- `Python-Task2-BMICalculator/main.py` — single-window Tkinter UI using `pack()` layout. Example actionable places:
  - Add the compute logic by binding a callback to `calculate_button` (currently created without a `command`). See lines creating `calculate_button`.
  - Validate `weight_entry` and `height_entry` for numeric input and sensible ranges before computing BMI.
  - Display results in a new `Label` or use `tkinter.messagebox.showinfo()`.

- Root-level READMEs are empty; do not assume additional project scaffolding or CI workflows.

# How to run locally (developer workflow)

- Run with the system Python that includes Tkinter: `python3 Python-Task2-BMICalculator/main.py` from the repo root.
- macOS note: ensure Python's Tkinter is available (system Python usually has it; Homebrew Pythons may need `brew install tcl-tk` and appropriate env).

# Coding conventions and expectations

- Keep changes minimal and explicit. This repo aims to be educational/demo-sized — avoid adding heavy frameworks or tests unless requested.
- Use clear, defensive parsing for inputs (float conversion with try/except). Return user-facing error messages rather than crashing.
- UI changes should keep existing geometry and visual hierarchy unless the user requests a redesign.

# Examples of recommended edits

- Wire button:

  - Add a function `def calculate_bmi():` that reads `weight_entry.get()` and `height_entry.get()`, validates them, computes BMI, and updates a `result_label`.
  - Attach: `calculate_button.config(command=calculate_bmi)`.

- Input validation snippet (conceptual):
  - If height <= 0 or weight <= 0: show a messagebox with an error.

# Tests, CI, and packaging

- There are no unit tests or CI configs. If asked to add tests, suggest isolating logic (move BMI computation into a small pure function) and adding a simple `tests/` folder with pytest.

# When to refactor

- Refactor into modules only when adding features that expand logic beyond simple UI (e.g., persistence, REST APIs, or multiple windows).
- If asked to refactor, split UI from logic: keep `ui.py` for Tk code and `bmi.py` for pure computation and validation.

# Integration points / external considerations

- No external services configured. Any integration (DB, API) will require adding dependency declarations (e.g., `requirements.txt`) and update to the README with run instructions.

# If you are an agent making a PR

- Keep PRs focused and small (1 feature/fix per PR).
- In the PR description, reference the exact lines changed in `main.py` and explain how input validation and error handling were addressed.

# Questions for the human

- Should results show in-place (`Label`) or pop up via `messagebox`?
- Do you want input units to be flexible (cm vs m) or fixed to meters?

-- End
