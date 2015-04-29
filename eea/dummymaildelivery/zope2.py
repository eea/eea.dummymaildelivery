import logging
import importlib

log = logging.getLogger('eea.dummymaildelivery')


def patched_createDataManager(self, fromaddr, toaddrs, message):
    import pdb; pdb.set_trace()
    return self.old_createDataManager(fromaddr, toaddrs, message)


def initialize(context):
    """ Patch zope.sendmail and repoze.sendmail """

    for source in ['zope.sendmail.delivery', 'repoze.sendmail.delivery']:
        try:
            mod = importlib.import_module(source)
            qmd = mod.QueuedMailDelivery
            qmd.old_createDataManager = qmd.createDataManager
            qmd.createDataManager = patched_createDataManager
            log.info("Patched %s.QueuedMailDelivery delivery with dummy delivery",
                    source)
        except ImportError:
            continue
