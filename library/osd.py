import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from localehelper import LocaleHelper
import time, os, gettext, sys

path = os.path.dirname(os.path.abspath(__file__)).strip('library')
localeHelper = LocaleHelper()
lang = localeHelper.getLocale()
t=gettext.translation('mama',path+'i18n/',languages=[lang])
t.install()

#keep the old way for the moment
#gettext.install('mama',path+'/i18n/')
RESULT = False
path += 'resources'


if len(sys.argv) >= 2:
    PID = sys.argv[1]
    # nom des fichiers
    start='/tmp/mama/mama_start_'+PID
    stop='/tmp/mama/mama_stop_'+PID
    result='/tmp/mama/mama_result_'+PID
    cmd='/tmp/mama/mama_cmd_'+PID
    error='/tmp/mama/mama_error_'+PID
    display='/tmp/mama/mama_display_'+PID


    # initialisation
    Notify.init("mama")
    n = Notify.Notification.new('mama',_('Ready'),path+"/icons.png")
    n.set_urgency(Notify.Urgency.CRITICAL)
    n.show()

    while os.path.exists(start) == False:
        n.update('mama',_('Ready'), path+"/icons.png")
        n.show()
        time.sleep(0.5)

    i = 0
    delay=0.1
    while os.path.exists(stop) == False:
        if os.path.exists(error):
            f = open(error,"r")
            title = _('Error')
            body = f.readline().rstrip('\n')
            f.close
            n.update(title, body,icon = path+"/error.png")
            n.show()
            time.sleep(2)
            n.close()
            os.system('rm /tmp/mama/mama_*_'+PID+' 2>/dev/null')
            sys.exit(1)

        if os.path.exists(result) and RESULT == False:
            f = open(result,"r")
            title=_('Recognition result')
            body = f.readline().rstrip('\n')
            icon = path+"/icons.png"
            f.close()
            delay = 2
            RESULT = True
        elif os.path.exists(cmd) and RESULT == True:
            if os.path.exists(result):
                os.system('rm '+result)
            f = open(cmd,"r")
            title = _('Calling command')
            body = f.readline().rstrip('\n')
            icon = path+"/icons.png"
            delay = 2
            f.close()
        elif os.path.exists(display):
            f = open(display,"r")
            title = _('Information')
            body = f.readline().rstrip('\n')
            f.close
            icon = path+"/icons.png"
            delay=3
        else:
            title = _('Performing recording')
            body = _('Please speak')
            icon = path+"/Waiting/wait-"+str(i)+".png"

        n.update(title, body, icon)
        n.show()
        time.sleep(delay)
        i += 1;
        if i > 17:
            i = 0

    n.update("mama",_('Done'),path+"/icons.png")
    n.show()
    time.sleep(1)
    n.close()
    os.system('rm /tmp/mama/mama_*_'+PID+' 2>/dev/null')
