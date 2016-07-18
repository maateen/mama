import gi

gi.require_version('Notify', '0.7')
import os
import sys
import time
from gi.repository import Notify

RESULT = False
path = os.path.dirname(os.path.abspath(__file__))
path += 'resources'

if len(sys.argv) >= 2:
    PID = sys.argv[1]
    # name of files
    start = '/tmp/mama/mama_start_' + PID
    stop = '/tmp/mama/mama_stop_' + PID
    result = '/tmp/mama/mama_result_' + PID
    cmd = '/tmp/mama/mama_cmd_' + PID
    error = '/tmp/mama/mama_error_' + PID
    display = '/tmp/mama/mama_display_' + PID
    record_complete = '/tmp/mama/mama_record_complete_' + PID

    # initialization
    Notify.init("Mama")
    n = Notify.Notification.new('Mama', 'Ready', path + "/icons.png")
    n.set_urgency(Notify.Urgency.CRITICAL)
    n.show()

    while not os.path.exists(start):
        n.update('mama', 'Ready', path + "/icons.png")
        n.show()

    i = 0
    while not os.path.exists(stop):
        if os.path.exists(error):
            f = open(error, "r")
            title = 'Error'
            body = f.readline().rstrip('\n')
            f.close
            n.update(title, body, icon=path + "/error.png")
            n.show()
            n.close()
            Notify.uninit()
            os.system('rm /tmp/mama/mama_*_' + PID + ' 2>/dev/null')
            sys.exit(1)

        if os.path.exists(result) and not RESULT:
            f = open(result, "r")
            title = 'Recognition result'
            body = f.readline().rstrip('\n')
            icon = path + "/success.png"
            f.close()
            RESULT = True
        elif os.path.exists(cmd) and RESULT:
            f = open(cmd, "r")
            title = 'Calling command'
            body = f.readline().rstrip('\n')
            icon = path + "/command.png"
            f.close()
        elif os.path.exists(display):
            f = open(display, "r")
            title = 'Information'
            body = f.readline().rstrip('\n')
            f.close
            icon = path + "/icons.png"
        elif os.path.exists(record_complete):
            title = 'Great! Got it.'
            body = 'Processing ...'
            icon = path + "/process.png"
        else:
            title = 'Hearing ...'
            body = 'Please speak'
            icon = path + "/Waiting/wait-" + str(i) + ".png"
            time.sleep(0.1)

        n.update(title, body, icon)
        n.show()
        i += 1
        if i > 17:
            i = 0

    n.update("Mama", 'Task completed!', path + "/icons.png")
    n.show()
    n.close()
    Notify.uninit()
    os.system('rm /tmp/mama/* 2>/dev/null')
