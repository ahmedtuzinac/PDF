from datetime import datetime


def get_placeholders(json_content, language):
    json_content = json_content['invoice_json']

    components = json_content['summary']['components']
    totale = 0
    for item in components:
        totale += components[item]

    totale += float(json_content['summary']['tax']['excise']['total'])
    totale += float(json_content['summary']['tax']['vat'])

    additional_costs = 0
    additional_costs_items = json_content['summary']['additional_cost']
    for additional_cost in additional_costs_items:
        additional_costs += float(additional_costs['amount'])
    totale_da_pagate = totale + additional_costs

    l_first = ''
    l_second = ''
    l_third = ''
    l_fourth = ''
    active = []
    reactive = []
    for item in json_content['summary']['metering']:
        if item['type'] == 'active':
            active.append(format_date(item['date']))
            continue
        elif item['type'] == 'reactive':
            reactive.append(format_date(item['date']))
    tipologia = ''
    if json_content['contract']['domestic']:
        tipologia += 'domestic'

    if tipologia == '':
        tipologia = 'business'

    tensione = ''
    if json_content['contract']['pod']['voltage'] in [230, 220]:
        if language == 'de':
            tensione = f"Einphasig {json_content['contract']['pod']['voltage']}V"
        else:
            tensione = f"Monofase {json_content['contract']['pod']['voltage']}V"
    else:
        if language == 'de':
            tensione = f"Dreiphasig {json_content['contract']['pod']['voltage']}V"
        else:
            tensione = f"Trifase {json_content['contract']['pod']['voltage']}V"

    metering = json_content['summary']['metering']
    active = []
    peak = []
    for item in metering:
        if item['type'] == 'active':
            active.append(item)
        if item['type'] == 'peak':
            peak.append(format_date(item['date']))
    f1 = active[1]['f1'] - active[0]['f1']
    f2 = active[1]['f2'] - active[0]['f2']
    f3 = active[1]['f2'] - active[0]['f3']

    f_total = f1 + f2 + f3
    imp = totale
    periodo = f"{format_date(json_content['invoice_period']['start'])} - {format_date(json_content['invoice_period']['end'])}"
    hist_placeholders = get_hist_placeholders(hist)
    placeholders = {
        'n_d_f': json_content['invoice_number'],
        'd_d_f': format_date(json_content['invoice_date']),
        'client_name': 'John Doe',
        'codice_cliente': '9455',
        'codice_fiscale': '123456789',
        'codice_destinatario': 'New York',
        't': str(json_content['summary']['total_amount']).replace('.', ','),
        'c': str(json_content['summary']['total_consumption_kwh']).replace('.', ','),
        'address': json_content['client']['address'],
        'number': json_content['client']['number'],
        'm': json_content['client']['municipality'],
        'p': json_content['client']['postal_code'],
        'inv_start': format_date(json_content['invoice_period']['start']),
        'inv_end': format_date(json_content['invoice_period']['end']),
        'p_d_d': format_date(json_content['payment']['due_date']),
        'pd': get_info_date(json_content['payment']['due_date'], language).split('-')[0],
        'pm': get_info_date(json_content['payment']['due_date'], language).split('-')[1],
        'py': get_info_date(json_content['payment']['due_date'], language).split('-')[2],
        'pfs': get_info_date(json_content['invoice_period']['start'], language).replace('-', ' '),
        'pfe': get_info_date(json_content['invoice_period']['end'], language).replace('-', ' '),
        'pod_addr': json_content['contract']['pod']['address'],
        'pod_postal': json_content['contract']['pod']['postal_code'],
        'pod_city': json_content['contract']['pod']['municipality'],
        'power_c': str(json_content['contract']['power_committed']).replace('.', ','),
        'power_a': str(json_content['contract']['power_available']).replace('.', ','),
        'c_start': format_date(json_content['contract']['contract_start']),
        'letter2': 'RM',
        'offerta': 'Test Case',
        'codice_offerta': '7777-7777-7777',
        'codice_pod': '888 888 888',
        'tipologia': 'test case',
        'energy': str(json_content['summary']['components']['energy']).replace('.', ','),
        'trans': str(json_content['summary']['components']['transport']).replace('.', ','),
        'system': str(json_content['summary']['components']['system']).replace('.', ','),
        't_b': str(round(totale, 2)).replace('.', ','),
        't_p': str(round(totale_da_pagate, 2)).replace('.', ','),
        'l_first': format_date(active[0]['date']),
        'l_second': format_date(active[1]['date']),
        'l_third': reactive[0],
        'l_fourth': reactive[1],
        't_c': str(additional_costs).replace('.', ','),
        'tipologia': tipologia,
        'contratto': '123',
        'tensione': tensione,
        'telephone': json_content['summary']['network_operator']['tel_number'],
        'f1': f1,
        'f2': f2,
        'f3': f3,
        'ft': f_total,
        'periodo': periodo,
        'inv_date': format_date(json_content['invoice_date']),
        'imp': str(round(imp, 2)).replace('.', ','),
        'name_operator': json_content['summary']['network_operator']['name'],
        'p_first': peak[0],
        'p_second': peak[1]
    }
    placeholders.update(hist_placeholders)
    ...
    return placeholders


date = '2023-12-07'

hist = {"hist_data": {
    "2024-01": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-02": {
        "active": {
            "F1": 1200,
            "F2": 500,
            "F3": 900
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-03": {
        "active": {
            "F1": 500,
            "F2": 501,
            "F3": 900
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-04": {
        "active": {
            "F1": 900,
            "F2": 903,
            "F3": 501
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-05": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-06": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-07": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-08": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-09": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-10": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-11": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-12": {
        "active": {
            "F1": 931,
            "F2": 931,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
}}


def get_hist_placeholders(json_content):
    hist_data = json_content['hist_data']

    current_year = datetime.utcnow().year
    placeholders = {}
    c_t = 0
    f1_t = 0
    f2_t = 0
    f3_t = 0

    for item in hist_data:
        if item.split('-')[0] == str(current_year):
            f1 = hist_data[item]['active']['F1']
            f2 = hist_data[item]['active']['F2']
            f3 = hist_data[item]['active']['F2']
            f1_t += f1
            f2_t += f2
            f3_t += f3
            c_t += f1 + f2 + f3
            placeholders[f'f1_{item.split("-")[1]}'] = f1
            placeholders[f'f2_{item.split("-")[1]}'] = f2
            placeholders[f'f3_{item.split("-")[1]}'] = f3
            placeholders[f'c_{item.split("-")[1]}'] = f1 + f2 + f3

    ...
    placeholders['f1_t'] = f1_t
    placeholders['f2_t'] = f2_t
    placeholders['f3_t'] = f3_t
    placeholders['c_t'] = c_t
    placeholders['y'] = str(current_year)[2:]
    ...
    return placeholders


def get_info_date(date, language):
    date_list = date.split('-')

    day = date_list[2]
    if day[0] == '0':
        day = day[1:]

    month = date_list[1]
    if month[0] == '0':
        month = month[1:]
    months_in_german = [
        'januar',
        'februar',
        'märz',
        'april',
        'mai',
        'juni',
        'juli',
        'august',
        'september',
        'oktober',
        'november',
        'dezember'
    ]
    months_in_italian = [
        'gennaio',
        'febbraio',
        'marzo',
        'aprile',
        'maggio',
        'giugno',
        'luglio',
        'agosto',
        'settembre',
        'ottobre',
        'novembre',
        'dicembre'
    ]
    if language == 'it':
        month = months_in_italian[int(month) - 1]
    else:
        month = months_in_german[int(month) - 1]

    year = date_list[0]

    return f'{day}-{month}-{year}'


def format_date(date):
    from datetime import datetime
    date_object = datetime.strptime(date, "%Y-%m-%d")
    formatted_string = date_object.strftime("%d/%m/%Y")

    return formatted_string
    '''
    client = self.invoice_data['client']
        contract = self.invoice_data['contract']
        summary = self.invoice_data['summary']

        payment_due = self.invoice_data['summary']['payment_due']
        p = str(payment_due).split('-0')
        new_p = []
        for x in p:
            if x[0] == '0':
                new_p.append(x[1::])
                continue
            new_p.append(x)

        months_in_italian = [
            'gennaio',
            'febbraio',
            'marzo',
            'aprile',
            'maggio',
            'giugno',
            'luglio',
            'agosto',
            'settembre',
            'ottobre',
            'novembre',
            'dicembre'
        ]

        total = self.invoice_data['summary']['total_amount']
        inv_d = self.invoice_data['invoice_date']
        inv_d = datetime.strptime(inv_d, '%Y-%m-%d').strftime('%d/%m/%Y')
        c_addr = client['address']
        c_n = client['number']
        pos_c = client['postal_code']
        muni = client['municipality']
        full_name = 'Test Name'
        codice_fiscale = client['tax_number']
        pod_addr = contract['pod']['address']
        pod_muni = contract['pod']['municipality']
        pod_postal = contract['pod']['postal_code']
        pod_number = contract['pod']['number']
        c_domestic = contract['domestic']
        c_p_c = contract['power_commited']
        c_p_a = str(contract['power_available']).replace('.', ',')
        c_start = datetime.strptime(contract['contract_start'], '%Y-%m-%d').strftime('%d/%m/%Y')
        invoice_start = self.invoice_data['invoice_period']['start']
        invoice_start = invoice_start.split('-')
        d_s = invoice_start[2][1::] if invoice_start[2][0] == '0' else invoice_start[2]
        d_m = months_in_italian[int(invoice_start[1][1::] if invoice_start[1][0] == '0' else invoice_start[1]) - 1]
        d_y = invoice_start[0]
        invoice_end = self.invoice_data['invoice_period']['end']
        invoice_end = invoice_end.split('-')
        d_e = invoice_end[2][1::] if invoice_end[2][0] == '0' else invoice_end[2]
        e_m = months_in_italian[int(invoice_end[1][1::] if invoice_end[1][0] == '0' else invoice_end[1]) - 1]
        e_y = invoice_end[0]
        tot_consumption = summary['total_consumption_kwh']
        ...

        placeholders = {
            'tot_consumption': tot_consumption,
            'd_e': d_e,
            'm_e': e_m,
            'y_e': e_y,
            'd_s': d_s,
            'm_s': d_m,
            'y_s': d_y,
            'c_domestic': c_domestic,
            'c_p_c': c_p_c,
            'c_p_a': c_p_a,
            'c_start': c_start,
            'pod_addr': pod_addr,
            'pod_muni': pod_muni,
            'pod_postal': pod_postal,
            'pod_number': pod_number,
            'full_name': full_name,
            'full_name_u': full_name.upper(),
            'codice_cliente': '5432',
            'p_day': new_p[2],
            'p_month': months_in_italian[int(new_p[1]) - 1],
            'p_year': new_p[0],
            'tot': str(total).replace('.', ','),
            'inv_d': inv_d,
            'c_addr': c_addr,
            'c_n': c_n,
            'pos_c': pos_c,
            'muni': muni,
            'space': '  ',
            'codice_fiscale': codice_fiscale,
            'codice_pod': pod_number,

        }
        doc = DocxTemplate(self.docx_temp_filepath)
        doc.render(placeholders)
        doc.save(self.docx_temp_filepath)
    :param json_content: 
    :return: 
    '''
