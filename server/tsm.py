from datetime import date, datetime, timedelta

def check_tsm_status(item, params,info):
    period = date.today() - timedelta(1)
    for line in info:
        if line:
            if line[0] != "Executing":
                lineDate = datetime.strptime(line[0], '%d.%m.%Y')
                if lineDate.date() < period:
                    if len(line) > 6 and line[6] == item:
                        if line[2] == "Successful":
                            return 0, "Backup of %s Successful" % item
                        elif "ANS1802E" in line[2]:
                            return 1, "Backup completed with %s Failures" % line[9]
    return 2, "Unkown Error"

def inventory_tsm_status(info):
    today = date.today()
    yesterday = today - timedelta(1)
    for line in info:
        if line:
            if line[0] != "Executing":
                lineDate = datetime.strptime(line[0], '%d.%m.%Y')
                if lineDate.date() == today or lineDate.date() == yesterday:
                    if len(line) > 2 and line[2] == "Incremental":
                        yield line[6], None



check_info["tsm.status"] = {
    'check_function':   check_tsm_status,
    'inventory_function':   inventory_tsm_status,
    'service_description':  'TSM backup %s',
}
