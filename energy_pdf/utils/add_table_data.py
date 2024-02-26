def get_data_for_dettaglio_fiscale(json_content):
    try:
        components = json_content['invoice_json']['summary']['components']
        totale = 0
        for item in components:
            totale += components[item]

        periodo = f"{format_date(json_content['invoice_json']['invoice_period']['start'])} - {format_date(json_content['invoice_json']['invoice_period']['end'])}"
        data = [
            ['TOTALE A+B+C', '', '', '', '', '', str(totale)],
            ['accisa', periodo, '', '€/kWh', json_content['invoice_json']['summary']['tax']['excise']['unit_price'], '', json_content['invoice_json']['summary']['tax']['excise']['total']]
        ]

        return data
    except Exception as e:
        raise Exception('["invoice_json"]["summary"]["components"] data isnt valid.')


def get_data_for_dettaglio_iva(json_content):
    try:
        components = json_content['invoice_json']['summary']['components']
        totale = 0
        for item in components:
            totale += components[item]
        totale += float(json_content['invoice_json']['summary']['tax']['excise']['total'])
        iva = json_content['invoice_json']['summary']['tax']['vat']

        data = [
            ['10 - Iva ? %', str(totale).replace('.', ','), '', iva],
            ['TOTALE IVA', '', '', iva]
        ]

        return data
    except Exception as e:
        raise Exception('["invoice_json"]["summary"]["components"] data isnt valid.')


def get_data_for_sintesi(json_content):
    try:

        data = [
            [
                json_content['invoice_json']['contract']['product'],
                f"{format_date(json_content['invoice_json']['invoice_period']['start'])} - {format_date(json_content['invoice_json']['invoice_period']['end'])}",
                str(json_content['invoice_json']['summary']['total_consumption_kwh']).replace('.', ',') + ' kWh',
                '€ ' + str(json_content['invoice_json']['summary']['total_amount']).replace('.', ','),
            ]
        ]
        return data
    except Exception as e:
        raise Exception('Data for SintesiTable(page1) isnt valid')


def get_data_for_livelo_massimo(json_content):
    try:
        metering = json_content['invoice_json']['summary']['metering']
        data = []
        peak = []
        for item in metering:
            if item['type'] == 'peak':
                peak.append(item)

        f1 = ['kW', 'F1', str(peak[0]['f1']), str(peak[1]['f1'])]
        f2 = ['kW', 'F2', str(peak[0]['f2']), str(peak[1]['f2'])]
        f3 = ['kW', 'F3', str(peak[0]['f3']), str(peak[1]['f3'])]

        return [f1, f2, f3]
    except Exception as e:
        raise Exception("['invoice_json']['summary']['metering'] data isnt valid.")


def get_data_for_letture(json_content):
    try:
        metering = json_content['invoice_json']['summary']['metering']
        data = []
        active = []
        reactive = []
        peak = []
        for item in metering:
            if item['type'] == 'active':
                active.append(item)
                continue
            elif item['type'] == 'reactive':
                reactive.append(item)
            else:
                peak.append(item)
        ...
        f1 = ['kWh', 'F1', str(active[0]['f1']), str(active[1]['f1']), str(reactive[0]['f1']), str(reactive[1]['f1'])]
        f2 = ['kWh', 'F2', str(active[0]['f2']), str(active[1]['f2']), str(reactive[0]['f2']), str(reactive[1]['f2'])]
        f3 = ['kWh', 'F3', str(active[0]['f3']), str(active[1]['f3']), str(reactive[0]['f3']), str(reactive[1]['f3'])]

        # massimo peak

        return [f1, f2, f3]
    except Exception as e:
        raise Exception('Data for LettureTable isnt valid.')


def get_data_for_iva_last_page(json_content):
    try:
        components = json_content['invoice_json']['summary']['components']
        totale = 0
        for item in components:
            totale += components[item]
        totale += float(json_content['invoice_json']['summary']['tax']['excise']['total'])
        iva = json_content['invoice_json']['summary']['tax']['vat']

        data = [['', '', str(round(totale, 2)), '', str(iva), '', '?']]
        return data
    except Exception as e:
        raise Exception('Data for Iva(last_page) isnt valid.')


def format_date(date):
    from datetime import datetime
    date_object = datetime.strptime(date, "%Y-%m-%d")
    formatted_string = date_object.strftime("%d/%m/%Y")

    return formatted_string
