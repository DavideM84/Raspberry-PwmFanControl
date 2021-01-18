#! /bin/sh

### BEGIN INIT INFO
# Provides:          fan_by_temp.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting fancontroy"
    /usr/bin/python3.7 /home/pi/fancontrol/fan_by_temp.py &
    ;;
  stop)
    echo "Stopping fancontrol.py"
    pkill -f /home/pi/fancontrol/fan_by_temp.py
    ;;
  restart)
    echo "Stopping ..."
    pkill -f /home/pi/fancontrol/fan_by_temp.py
    echo "Starting ..."
    /usr/bin/python3.7 /home/pi/fancontrol/fan_by_temp.py &
    ;;
  status)
    cat /home/pi/fancontrol/fancontrol.log
    ;;
  *)
    echo "Usage: /etc/init.d/fancontrol.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
