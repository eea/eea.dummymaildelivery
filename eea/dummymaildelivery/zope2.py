import logging
import importlib
import urllib

log = logging.getLogger('eea.dummymaildelivery')


def patched_createDataManager(self, fromaddr, toaddrs, message):
    to = urllib.quote(message['To'])
    destination = 'eionet.testing+%s@gmail.com' % to
    message.replace_header('To', destination)
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
