# Set Dresser

A Maya tool that scatters rocks and trees across a 40x40 ground, keeping them
off the path (4 wide along Z, plus a 1-unit margin on each side) and out of the
pond (radius 6 at x=10, z=10). A window has sliders for rock count, tree count,
area and seed, a "keep clear" checkbox, and Scatter / Clear buttons.

- One Scatter is one undo (Ctrl+Z removes the whole set).
- Clear deletes only the `rocks` and `trees` groups.
- Same seed + same settings = the same set every time.

Built for HSG-5232 Programming for Animators (Trees & Rocks tutorial, Chapter 10).

## Maya version

Maya 2026 (tested in 2026.3 on Windows). Python 3, `maya.cmds`, no pymel.

## Run it

Copy `set_dresser.py` and `set_dresser_ui.py` into your Maya scripts folder
(find it with `print(cmds.internalVar(userScriptDir=True))`), then in the
Script Editor (Python tab):

```python
import set_dresser_ui
set_dresser_ui.show()
```

From code, without the window:

```python
import set_dresser
set_dresser.scatter(rocks=30, trees=12, seed=12)
```

## Files

- `set_dresser.py` — the engine (no UI).
- `set_dresser_ui.py` — the window; reads controls and calls the engine.
- `CLAUDE.md` — rules given to the agent that built it.
- `send_to_maya.py` — sends one line of Python to Maya's command port.
