import pathlib
import yaml
import json
import time
from datetime import datetime


def open_placeholders_yaml_file(yaml_file_path: str):
    try:
        with open(yaml_file_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
                return data
            except yaml.YAMLError as e:
                raise
                print("Error loading YAML file:", e)
    except Exception as e:
        raise
    return None


def open_invoice_json_file(invoice_json_file_path: str):
    try:
        with open(invoice_json_file_path, 'r') as file:
            try:
                data = json.load(file)
                return data
            except json.JSONDecodeError as e:
                print("Error loading JSON file:", e)
    except Exception as e:
        raise
    return None


def get_placeholders_from_invoice(invoice_json: dict, yaml_file_path: str, language: str):
    yaml_data = open_placeholders_yaml_file(yaml_file_path=yaml_file_path)
    json_data = invoice_json
    placeholders_map = {}

    for placeholder_type in yaml_data:
        values = yaml_data[placeholder_type]
        if values:

            for placeholder in values:
                value = values[placeholder]
                keys = [key.strip(']["') for key in value.split('"]["')]
                result = json_data

                for key in keys:
                    try:
                        result = result[key]
                    except Exception as e:
                        Exception(f'{placeholder} not found at json{value}, problematic key is ["{key}"]')
                        result = None

                if result:
                    if placeholder_type == 'dates':
                        result = format_date(result)
                    elif placeholder_type == 'floats':
                        result = str(round(float(result), 2)).replace('.', ',')
                    placeholders_map[placeholder] = result

    specified_placeholders_map = get_specified_placeholders_map(json_data, language)
    hist_placeholders_map = get_hist_placeholders(json_data)
    return {**placeholders_map, **specified_placeholders_map, **hist_placeholders_map}


def get_hist_placeholders(json_content: dict) -> dict:
    try:
        hist_data = json_content['invoice_json']['hist_data']
    except Exception as e:
        print('Hist data not found at json["invoice_json"]["hist_data"]')
        return {}
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


def get_specified_placeholders_map(json_data: dict, language: str) -> dict:
    try:
        json_content = json_data['invoice_json']
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
    except Exception as e:
        print("Key not found in json: Key: ", e)
        raise
    return {
        'pd': get_info_date(json_content['payment']['due_date'], language).split('-')[0],
        'pm': get_info_date(json_content['payment']['due_date'], language).split('-')[1],
        'py': get_info_date(json_content['payment']['due_date'], language).split('-')[2],
        'pfs': get_info_date(json_content['invoice_period']['start'], language).replace('-', ' '),
        'pfe': get_info_date(json_content['invoice_period']['end'], language).replace('-', ' '),
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
        'f1': f1,
        'f2': f2,
        'f3': f3,
        'ft': f_total,
        'periodo': periodo,
        'p_first': peak[0],
        'p_second': peak[1],
        'imp': str(round(imp, 2)).replace('.', ','),
    }


def get_info_date(date: str, language: str) -> str:
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
