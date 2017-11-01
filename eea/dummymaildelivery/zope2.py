import logging
import importlib
import urllib

log = logging.getLogger('eea.dummymaildelivery')


def patched_createDataManager(self, fromaddr, toaddrs, message):
    to = urllib.quote(message.get('To', 'empty_email'))
    destination = 'eionet.testing+%s@gmail.com' % to
    message.replace_header('To', destination)
    cc = urllib.quote(message.get('Cc', ''))
    if cc:
        patched_cc = 'eionet.testing+%s@gmail.com' % cc
        message.replace_header('Cc', patched_cc)
    return self.old_createDataManager(fromaddr, [destination], message)


def initialize(context):
    """ Patch zope.sendmail and repoze.sendmail """

    for source in ['zope.sendmail.delivery', 'repoze.sendmail.delivery']:
        try:
            mod = importlib.import_module(source)
            qmd = mod.QueuedMailDelivery
            qmd.old_createDataManager = qmd.createDataManager
            qmd.createDataManager = patched_createDataManager
            log.info(
                "Patched %s.QueuedMailDelivery delivery with dummy delivery",
                source)
        except ImportError:
            continue
