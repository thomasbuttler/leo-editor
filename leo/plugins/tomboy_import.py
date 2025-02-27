#@+leo-ver=5-thin
#@+node:ville.20090503124249.1: * @file ../plugins/tomboy_import.py
""" Allows imports of notes created in Tomboy / gnote.

Usage:

* Create a node with the headline 'tomboy'
* Select the node, and do alt+x act-on-node
* The notes will appear as children of 'tomboy' node
* The next time you do act-on-node, existing notes will be updated (they don't need to
  be under 'tomboy' node anymore) and new notes added.

"""
# By Ville M. Vainio

#@+<< imports >>
#@+node:ville.20090503124249.4: ** << imports >>
import html.parser as HTMLParser
import xml.etree.ElementTree as ET
from leo.core import leoGlobals as g
from leo.core import leoPlugins
    # Uses leoPlugins.TryNext
#@-<< imports >>
#@+others
#@+node:ville.20090503124249.5: ** init
def init():
    """Return True if the plugin has loaded successfully."""
    g.registerHandler('after-create-leo-frame', onCreate)
    g.plugin_signon(__name__)
    return True
#@+node:ville.20090503124249.6: ** onCreate
def onCreate(tag, keys):

    c = keys.get('c')
    if not c:
        return

    # c not needed

    tomboy_install()
#@+node:ville.20090503124249.7: ** the code
class MLStripper(HTMLParser.HTMLParser):
    # pylint: disable=super-init-not-called
    # pylint: disable=abstract-method
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, data):
        self.fed.append(data)
    def get_fed_data(self):
        return ''.join(self.fed)

def strip_tags(cont):
    x = MLStripper()
    x.feed(cont)
    return x.get_fed_data()

def parsenote(cont):
    tree = ET.parse(cont)
    title = tree.findtext('{http://beatniksoftware.com/tomboy}title')
    # EKR: I'm not sure that finditer is correct, but geiterator no longer exists.
    # body  = tree.getiterator('{http://beatniksoftware.com/tomboy}note-content')[0]
    body = tree.iterfind('{http://beatniksoftware.com/tomboy}note-content')[0]
    b = ET.tostring(body)
    b = strip_tags(b)
    return title, b

def pos_for_gnx(c, gnx):
    for pos in c.all_positions():
        pos = pos.copy()
        if pos.gnx == gnx:
            return pos.copy()
    return None

def capturenotes(c, pos):
    import glob
    import os
    notes = glob.glob(os.path.expanduser('~/.tomboy/*.note'))

    # map tomboy file name => gnx
    old_nodes = c.db.get('tomboy_notes', {})

    for no in notes:
        fname = os.path.basename(no)
        title, body = parsenote(open(no))

        po = None
        if fname in old_nodes:

            po = pos_for_gnx(c, old_nodes[fname])
            if po is not None:
                g.es('tomboy: Updating note "%s"' % title)

        if po is None:
            g.es('tomboy: Creating note "%s"' % title)
            po = pos.insertAsLastChild()

        po.h = title
        po.b = body
        old_nodes[fname] = po.gnx
    c.db['tomboy_notes'] = old_nodes

def tomboy_act_on_node(c, p, event):
    if not p.h == 'tomboy':
        raise leoPlugins.TryNext

    capturenotes(c, p)
    c.redraw()

def tomboy_install():
    g.act_on_node.add(tomboy_act_on_node, 99)
#@-others
#@@language python
#@@tabwidth -4
#@-leo
