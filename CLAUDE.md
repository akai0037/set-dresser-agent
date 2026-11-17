# Set dresser — rules for the agent

This folder is a Maya tool. Read this before touching anything.

## The app
- Maya 2026 on Windows. Python 3, `import maya.cmds as cmds`. No pymel.
- mayapy is at: E:\MAYA\Maya2026\bin\mayapy.exe
- The shell is PowerShell. Use mayapy for every Python run outside Maya.

## How to run your work
- Live, inside my open Maya: the command port on 7001 does not work on this machine.
  Drop a .py into Documents\maya\claude_bridge\inbox; Maya runs it and writes outbox\<name>.log.
- Headless, without opening Maya (run from this folder):
  & "E:\MAYA\Maya2026\bin\mayapy.exe" -c "import maya.standalone; maya.standalone.initialize(); import set_dresser; set_dresser.scatter(5, 2); import maya.cmds as cmds; print(cmds.ls('rock*', 'tree*'))"
- "Done" means you ran it and looked at what it made. Not that it imported.

## Rules of the tool
- The engine (`set_dresser.py`) has no UI in it. The window (`set_dresser_ui.py`) only reads controls and calls the engine.
- One function per thing it makes: `make_rock`, `make_tree`. One function per rule: `is_clear`.
- Everything scatter makes goes under a group (`rocks`, `trees`). Clear deletes the groups and nothing else. Never `select(all=True)`, never delete by wildcard.
- One scatter = one undo step (`cmds.undoInfo(openChunk=True)` … `closeChunk=True` in a `try/finally`).
- Errors the artist sees are one sentence (`cmds.warning`), not a traceback.
- Keep the names: `rock`, `tree`, `trunk`, `canopy`, `ground`, `path`, `pond`.

## Before you say it's done
- Tell me your plan before you touch anything.
- Run it. Say what appeared and how many.
- Commit after each working step.
