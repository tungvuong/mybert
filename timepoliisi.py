import requests
import time
import re

while True:
    time.sleep(5)
    
    s = requests.Session()
    suggest = s.get('https://asiointi.poliisi.fi/ajanvaraus-fe')
    #print(s.cookies.get_dict()['JSESSIONID'])
    #print(re.findall("csrf = \"(.*?)\";", suggest.text)[0])
    #print(s.cookies.get_dict())

    JSESSIONID=s.cookies.get_dict()['JSESSIONID']
    CSRF=re.findall("csrf = \"(.*?)\";", suggest.text)[0]

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Cookie': 'pol_init=1; JSESSIONID='+JSESSIONID+';',
        'Origin': 'https://asiointi.poliisi.fi',
        'Referer': 'https://asiointi.poliisi.fi/ajanvaraus-fe/reserve',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': CSRF,
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'participantMultiplier': 3,
        'siteId': '5501',
        'prereserve': False,
        'startDate': '2023-05-05T21:00:00.000Z',
        'endDate': '2023-08-06T20:59:59.999Z',
        'ajanvarausServiceType': {
            'group': {
                'groupCode': '01',
                'groupPrio': '1',
                'nameFi': 'Passit ja henkilökortit',
                'nameSv': 'Pass och identitetskort',
                'nameEn': 'Passports and identity cards',
                'nameSe': 'Opássat ja persovdnagoarttat',
            },
            'typeUICode': '0402',
            'typeSystemCode': 'AV0499',
            'nameFi': 'Passi',
            'nameSv': 'Pass',
            'nameEn': 'Passport',
            'nameSe': 'Pássa',
            'homeDepartmentOnly': False,
            'caseType': 'PASSI',
            'caseSpecificType': None,
        },
        'electronicApplication': False,
    }

    response = requests.post(
        'https://asiointi.poliisi.fi/ajanvaraus-fe/api/timereservation/C52060_5501_2023-06-25',
        headers=headers,
        json=json_data,
    ).json()

    #print(response.json())
    slots = []
    for key,slot in response['slots'].items():
        timeSlots = slot['timeSlots']
        if len(timeSlots)>0:
            slots+=timeSlots
    slots.sort()
    print('- Avail slots: ',slots[:5])
    first = slots[0].split('-')[1]
    latest = None
    if first in ['06','07']:
        latest = slots[0]
    print(latest)
    if (latest == None):
        continue

    cookies = {
        'poliisi_asiointi': '!s250wW+ZtWFxcwnyS0SwIBwO3Lv0ZGO8yQbSxc3HqVY1TXkwjDCY0TKkYYkIoe22ZDP9J19m7fYFooJIM/riz26h7XvZw++CM2zTCv8QXw==',
        'pol_init': '1',
        'JSESSIONID': JSESSIONID,
    #    'TS01805349': '01489080b5bf5dd28cd57ca539b05962bb86418883f9e3d8b7d1754af08060c874bf0e5f0f86f87725391cf3cffa2b48ccfa8e8e00',
    #    'Snoobisession_asiointi_poliisi_fi': '15492437',
    #    'Snoobi30minute_asiointi_poliisi_fi': '15492437',
    #    'SnoobiID': '1505875266-1a6ed80b69c6571322259ef628c7f99e',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://asiointi.poliisi.fi',
        'Referer': 'https://asiointi.poliisi.fi/ajanvaraus-fe/reserve',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': CSRF,
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'participantMultiplier': 3,
        'siteId': '5501',
        'startTime': latest+':00Z',
        'ajanvarausServiceType': {
            'group': {
                'groupCode': '01',
                'groupPrio': '1',
                'nameFi': 'Passit ja henkilökortit',
                'nameSv': 'Pass och identitetskort',
                'nameEn': 'Passports and identity cards',
                'nameSe': 'Opássat ja persovdnagoarttat',
            },
            'typeUICode': '0402',
            'typeSystemCode': 'AV0499',
            'nameFi': 'Passi',
            'nameSv': 'Pass',
            'nameEn': 'Passport',
            'nameSe': 'Pássa',
            'homeDepartmentOnly': False,
            'caseType': 'PASSI',
            'caseSpecificType': None,
        },
    }

    response = requests.post(
        'https://asiointi.poliisi.fi/ajanvaraus-fe/api/prereservation',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )


    reservationId=response.json()['reservationId']
    print('- reservationId: ',reservationId)

    cookies = {
        'pol_init': '1',
        'JSESSIONID': JSESSIONID,
        'poliisi_asiointi': '!uSeLrFjeYuPSIx4+jBcx640NL8GBbs7jwp3hqsPlgQDXqAAbiUqQo1z7bhNtPem18oUt5rPOwOS0Z65MhnqQ2WaZIqCkZc29PG7SF1oNOQ==',
        'Snoobisession_asiointi_poliisi_fi': '15477727',
        'Snoobi30minute_asiointi_poliisi_fi': '15477727',
        'SnoobiID': '1505577995-b58e1cb1f1ae064ca2751c672a905d1c',
        'TS01805349': '01489080b5641ce133d2c927ea091dbecc4868616e57921098c7d8d000b961e418e587088c3457ea9d033621e42086fc7fc3c67f2c',
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://asiointi.poliisi.fi',
        'Referer': 'https://asiointi.poliisi.fi/ajanvaraus-fe/reserve',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'X-CSRF-TOKEN': CSRF,
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    json_data = {
        'principalContact': {
            'contactInfo': {
                'email': 'vuongthanhtung@live.com',
                'emailAgain': 'vuongthanhtung@live.com',
                'phoneNumber': '+358413144891',
                'phoneNumberAgain': '+358413144891',
            },
            'principal': {
                'name': 'Minh Hue Duong',
                'firstName': 'Minh Hue',
                'lastName': 'Duong',
                'birthDay': '150586-300K',
            },
        },
        'appointment': {
            'reservationId': reservationId,
            'topics': [
                {
                    'ajanvarausServiceType': {
                        'group': {
                            'groupCode': '01',
                            'groupPrio': '1',
                            'nameFi': 'Passit ja henkilökortit',
                            'nameSv': 'Pass och identitetskort',
                            'nameEn': 'Passports and identity cards',
                            'nameSe': 'Opássat ja persovdnagoarttat',
                        },
                        'typeUICode': '0402',
                        'typeSystemCode': 'AV0499',
                        'nameFi': 'Passi',
                        'nameSv': 'Pass',
                        'nameEn': 'Passport',
                        'nameSe': 'Pássa',
                        'homeDepartmentOnly': False,
                        'caseType': 'PASSI',
                        'caseSpecificType': None,
                    },
                    'participant': {
                        'name': 'Minh Hue Duong',
                        'birthDay': '150586-300K',
                    },
                    'principal': True,
                },
                {
                    'ajanvarausServiceType': {
                        'group': {
                            'groupCode': '01',
                            'groupPrio': '1',
                            'nameFi': 'Passit ja henkilökortit',
                            'nameSv': 'Pass och identitetskort',
                            'nameEn': 'Passports and identity cards',
                            'nameSe': 'Opássat ja persovdnagoarttat',
                        },
                        'typeUICode': '0402',
                        'typeSystemCode': 'AV0499',
                        'nameFi': 'Passi',
                        'nameSv': 'Pass',
                        'nameEn': 'Passport',
                        'nameSe': 'Pássa',
                        'homeDepartmentOnly': False,
                        'caseType': 'PASSI',
                        'caseSpecificType': None,
                    },
                    'participant': {
                        'name': 'Vuong Kha Nhu',
                        'birthDay': '131116A572U',
                    },
                    'principal': False,
                },
                {
                    'ajanvarausServiceType': {
                        'group': {
                            'groupCode': '01',
                            'groupPrio': '1',
                            'nameFi': 'Passit ja henkilökortit',
                            'nameSv': 'Pass och identitetskort',
                            'nameEn': 'Passports and identity cards',
                            'nameSe': 'Opássat ja persovdnagoarttat',
                        },
                        'typeUICode': '0402',
                        'typeSystemCode': 'AV0499',
                        'nameFi': 'Passi',
                        'nameSv': 'Pass',
                        'nameEn': 'Passport',
                        'nameSe': 'Pássa',
                        'homeDepartmentOnly': False,
                        'caseType': 'PASSI',
                        'caseSpecificType': None,
                    },
                    'participant': {
                        'name': 'Vuong Thanh Tung',
                        'birthDay': '030786-2893',
                    },
                    'principal': False,
                },
            ],
        },
    }

    response = requests.post(
        'https://asiointi.poliisi.fi/ajanvaraus-fe/api/appointment',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )

    print('!!! CONFIRMED !!! ', response.json())
    if 'reservationId' in response.json():
        break
