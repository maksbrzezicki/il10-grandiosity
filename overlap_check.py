"""Report pairs of text elements whose drawn boxes intersect."""
import sys, json, itertools
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text

def run(nbfile, cells, figvar="fig"):
    nb=json.load(open(nbfile)); ns={}
    for i in cells:
        exec("".join(nb["cells"][i]["source"]), ns)
    return ns[figvar]

def texts(fig):
    """Visible text that is actually drawn: artists owned by an Axes, plus
    figure-level text such as the suptitle. Matplotlib keeps a few detached
    Text artists (the unused second tick labels, for example) that report
    themselves visible but are never rendered; those are skipped."""
    figlevel = set(map(id, fig.texts))
    out = []
    for t in fig.findobj(Text):
        if not t.get_text().strip() or not t.get_visible():
            continue
        if t.axes is None and id(t) not in figlevel:
            continue
        out.append(t)
    return out

def report(fig, tol=0.0):
    fig.canvas.draw()
    r=fig.canvas.get_renderer()
    items=[]
    for t in texts(fig):
        try: bb=t.get_window_extent(renderer=r)
        except Exception: continue
        if bb.width<=0 or bb.height<=0: continue
        items.append((t.get_text().replace("\n"," / ")[:38], bb, t))
    bad=[]
    for (s1,b1,t1),(s2,b2,t2) in itertools.combinations(items,2):
        if s1==s2 and abs(b1.x0-b2.x0)<40 and abs(b1.y0-b2.y0)<40: continue
        if t1.axes is not None and t1.axes is t2.axes and t1.get_position()==t2.get_position(): continue
        ov=b1.intersection(b1,b2)
        if ov is None: continue
        a=ov.width*ov.height
        if a>tol and ov.width>1 and ov.height>1:
            bad.append((round(a), f"{s1} @({b1.x0:.0f},{b1.y0:.0f})", f"{s2} @({b2.x0:.0f},{b2.y0:.0f})"))
    bad.sort(reverse=True)
    return bad

if __name__=="__main__":
    nbf=sys.argv[1]; cells=[int(x) for x in sys.argv[2].split(",")]
    fig=run(nbf,cells)
    b=report(fig)
    print(f"{len(b)} overlapping text pairs")
    for a,s1,s2 in b[:40]: print(f"  {a:>7} px2  '{s1}'  <->  '{s2}'")
