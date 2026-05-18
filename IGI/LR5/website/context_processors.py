import datetime
import requests
from django.utils import timezone

def global_footer_context(request):
    local_now = timezone.now() 
    utc_now = datetime.datetime.now(datetime.timezone.utc)
    tz_name = timezone.get_current_timezone_name()

    # Погода на русском (wttr.in)
    footer_weather = {'temp': '?', 'desc': 'Нет данных'}
    try:
        # lang=ru возвращает описание на русском
        response = requests.get('https://wttr.in/Minsk?format=j1&lang=ru', timeout=3)
        if response.status_code == 200:
            res = response.json()
            footer_weather['temp'] = res['current_condition'][0]['temp_C']
            # Берем именно русское описание
            footer_weather['desc'] = res['current_condition'][0]['lang_ru'][0]['value']
    except:
        pass

    # Курс НБРБ
    footer_usd = "Недоступно"
    try:
        res = requests.get('https://api.nbrb.by/exrates/rates/431', timeout=3)
        if res.status_code == 200:
            footer_usd = res.json().get('Cur_OfficialRate')
    except:
        pass

    return {
        'footer_local_time': local_now,
        'footer_utc_time': utc_now,
        'footer_tz_name': tz_name,
        'footer_usd': footer_usd,
        'footer_weather': footer_weather,
    }