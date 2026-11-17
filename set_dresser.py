"""set_dresser.py - the engine. No windows in here.

Run from Maya:
    import set_dresser
    set_dresser.build_ground()
    set_dresser.scatter(rocks=30, trees=12, seed=12)
"""

import math
import random

# borrowing Maya's own toolbox, so I can just say cmds.something to make stuff
import maya.cmds as cmds

GROUND_SIZE = 40.0
AREA = 18.0
# half of the path's width - change it here once, not inside every function
PATH_HALF_WIDTH = 2.0
PATH_MARGIN = 1.0
POND_CENTER = (10.0, 10.0)
POND_RADIUS = 6.0
MAX_TRIES_PER_ITEM = 20


def paint(obj, kind, r, g, b):
    """Give obj the flat colour for its kind. One shader per kind, made once."""
    shader = kind + "_mat"
    if not cmds.objExists(shader):
        shader = cmds.shadingNode("lambert", asShader=True, n=shader)
        cmds.setAttr(shader + ".color", r, g, b, type="double3")
        sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, n=shader + "SG")
        cmds.connectAttr(shader + ".outColor", sg + ".surfaceShader")
    cmds.sets(obj, e=True, forceElement=shader + "SG")


# one rock, start to finish: squash a sphere, spin it, drop it at x, z
def make_rock(x, z, size=1.0):
    """A low-poly sphere, squashed and spun so it reads as a rock. Returns its name."""
    rock = cmds.polySphere(r=0.5, sx=6, sy=4, n="rock")[0]
    cmds.scale(size * random.uniform(0.8, 1.6),
               size * random.uniform(0.4, 0.9),
               size * random.uniform(0.8, 1.6), rock)
    cmds.rotate(0, random.uniform(0, 360), 0, rock)
    cmds.move(x, 0, z, rock)
    paint(rock, "rock", 0.42, 0.40, 0.37)
    return rock


def make_tree(x, z, height=3.0):
    """A trunk and a canopy, grouped so the tree moves as one thing. Returns the group."""
    trunk = cmds.polyCylinder(r=height * 0.06, h=height * 0.5, n="trunk")[0]
    cmds.move(0, height * 0.25, 0, trunk)
    canopy = cmds.polyCone(r=height * 0.35, h=height * 0.7, n="canopy")[0]
    cmds.move(0, height * 0.85, 0, canopy)
    paint(trunk, "trunk", 0.36, 0.24, 0.14)
    paint(canopy, "canopy", 0.18, 0.42, 0.20)
    tree = cmds.group(trunk, canopy, n="tree")
    cmds.move(x, 0, z, tree)
    return tree


def is_clear(x, z):
    """True when (x, z) is off the path (plus its margin) and out of the pond."""
    on_path = abs(x) < PATH_HALF_WIDTH + PATH_MARGIN
    in_pond = math.hypot(x - POND_CENTER[0], z - POND_CENTER[1]) < POND_RADIUS
    return not on_path and not in_pond


def group_for(name):
    """The group that holds everything of one kind. Made on first use."""
    if not cmds.objExists(name):
        cmds.group(empty=True, n=name)
    return name


def _place(count, area, keep_clear, kind):
    """Place `count` things of one kind. Returns how many were placed."""
    grp = group_for(kind + "s")
    placed = 0
    tries = 0
    # keep trying spots until there are enough rocks (or trees), with a cap so Maya never hangs
    while placed < count and tries < count * MAX_TRIES_PER_ITEM:
        tries += 1
        x = random.uniform(-area, area)
        z = random.uniform(-area, area)
        # is this spot on the path or in the pond? if yes, skip it and try another
        if keep_clear and not is_clear(x, z):
            continue
        if kind == "rock":
            thing = make_rock(x, z, size=random.uniform(0.5, 1.5))
        else:
            thing = make_tree(x, z, height=random.uniform(2.5, 4.5))
        cmds.parent(thing, grp)
        placed += 1
    return placed


def scatter_rocks(count, area=AREA, keep_clear=True):
    return _place(count, area, keep_clear, "rock")


def scatter_trees(count, area=AREA, keep_clear=True):
    return _place(count, area, keep_clear, "tree")


def scatter(rocks=30, trees=12, area=AREA, keep_clear=True, seed=None):
    """The whole set in one undo step. Same seed + same settings = same set."""
    if seed is not None:
        random.seed(seed)
    cmds.undoInfo(openChunk=True, chunkName="set_dresser_scatter")
    try:
        build_ground()
        r = scatter_rocks(rocks, area, keep_clear)
        t = scatter_trees(trees, area, keep_clear)
    finally:
        cmds.undoInfo(closeChunk=True)
    if r < rocks or t < trees:
        cmds.warning("Only room for %d rocks and %d trees in that area." % (r, t))
    return r, t


def build_ground(size=GROUND_SIZE):
    """The ground, the path and the pond. Skips anything that already exists."""
    if not cmds.objExists("ground"):
        ground = cmds.polyPlane(w=size, h=size, sx=1, sy=1, n="ground")[0]
        paint(ground, "ground", 0.33, 0.38, 0.22)
    if not cmds.objExists("path"):
        path = cmds.polyPlane(w=PATH_HALF_WIDTH * 2, h=size, sx=1, sy=1, n="path")[0]
        cmds.move(0, 0.02, 0, path)
        paint(path, "path", 0.62, 0.55, 0.40)
    if not cmds.objExists("pond"):
        pond = cmds.polyCylinder(r=POND_RADIUS, h=0.04, n="pond")[0]
        cmds.move(POND_CENTER[0], 0.02, POND_CENTER[1], pond)
        paint(pond, "pond", 0.22, 0.36, 0.48)


def clear():
    """Delete only what scatter made: the rocks and trees groups. The ground stays."""
    gone = 0
    for name in ("rocks", "trees"):
        if cmds.objExists(name):
            cmds.delete(name)
            gone += 1
    if gone == 0:
        cmds.warning("Nothing to clear.")
