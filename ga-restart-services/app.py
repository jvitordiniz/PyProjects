import win32service
import win32con
import win32serviceutil


def ListServices():
    resume = 0
    accessSCM = win32con.GENERIC_READ
    accessSrv = win32service.SC_MANAGER_ALL_ACCESS

    # Open Service Control Manager
    hscm = win32service.OpenSCManager(None, None, accessSCM)

    # Enumerate Service Control Manager DB
    typeFilter = win32service.SERVICE_WIN32
    stateFilter = win32service.SERVICE_STATE_ALL

    statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)

    servicesList = []

    for (short_name, desc, status) in statuses:
        service = (short_name, desc, status)
        servicesList.append(service)
    return servicesList


def GetServiceStatus(service, machine):
    return win32serviceutil.QueryServiceStatus(service, machine)[1] == 4


def RestartServices(service, machine):
    running = GetServiceStatus(service, machine)
    if not running:
        print("Can't restart, %s not running" % service)
        return 0
    win32serviceutil.RestartService(service, machine)
    running = GetServiceStatus(service, machine)
    print('%s restarted successfully' % service)


if __name__ == '__main__':
    servicos = ListServices()
    # index 0 == short_name
    loadbalancers = filter(lambda servicos: 'AnyDesk' in servicos[0], servicos)
    # print(list(loadbalancers))

    for loadbalancer in loadbalancers:
        RestartServices(loadbalancer[0], None)
