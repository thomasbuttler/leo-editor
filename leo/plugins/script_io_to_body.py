#@+leo-ver=5-thin
#@+node:edream.110203113231.925: * @file ../plugins/script_io_to_body.py
"""Sends output from the Execute Script command to the end of the body pane."""

#@+<< imports >>
#@+node:ekr.20050101090207.4: ** << imports >>
from leo.core import leoGlobals as g
#@-<< imports >>

#@+others
#@+node:ekr.20071025195133: ** init
def init():
    """Return True if the plugin has loaded successfully."""
    g.registerHandler('after-create-leo-frame', onCreate)
    g.plugin_signon(__name__)
    return True
#@+node:ekr.20071212092332: ** onCreate
def onCreate(tag, keys):

    c = keys.get('c')
    if c and c.frame.log:

        g.pr('overriding c.executeScript')

        # Inject ivars.
        log = c.frame.log
        c.script_io_to_body_oldexec = c.executeScript
        c.script_io_to_body_oldput = log.put
        c.script_io_to_body_oldputnl = log.putnl

        # Override c.executeScript.
        g.funcToMethod(newExecuteScript, c.__class__, 'executeScript')
        c.k.overrideCommand('execute-script', c.executeScript)
#@+node:edream.110203113231.928: ** newPut and newPutNl (script_io_to_body.py)
# Same as frame.put except sends output to the end of the body text.
def newPut(self, s, *args, **keys):

    p, u = self.c.p, self.c.undoer
    body = self.frame.body
    w = body.wrapper
    if w:
        bunch = u.beforeChangeBody(p)
        w.insert("end", s)
        p.v.b = w.getAllText()
        u.afterChangeBody(p, 'put-to-body-text', bunch)

# Same as frame.putnl except sends output to the end of the body text.
def newPutNl(self, s, *args, **keys):
    newPut(self, '\n')
#@+node:ekr.20071212091008.1: ** newExecuteScript & helpers
def newExecuteScript(self,
    event=None, p=None, script=None,
    useSelectedText=True, define_g=True,
    define_name='__main__', silent=False
):

    c = self
    log = c.frame.log
    redirect(c)

    # Use silent to suppress 'end of script message'
    c.script_io_to_body_oldexec(event, p, script, useSelectedText, define_g, define_name, silent=True)
    undirect(c)

    # Now issue the 'end of script' message'
    if not silent:
        tabName = log and hasattr(log, 'tabName') and log.tabName or 'Log'
        g.ecnl()
        g.es("end of script", color="purple", tabName=tabName)
#@+node:ekr.20071212090128: *3* redirect
def redirect(c):

    log = c.frame.log.__class__

    g.funcToMethod(newPut, log, "put")
    g.funcToMethod(newPutNl, log, "putnl")
#@+node:ekr.20071212091008: *3* undirect
def undirect(c):

    log = c.frame.log.__class__

    g.funcToMethod(c.script_io_to_body_oldput, log, "put")
    g.funcToMethod(c.script_io_to_body_oldputnl, log, "putnl")
#@-others
#@@language python
#@@tabwidth -4

#@-leo
