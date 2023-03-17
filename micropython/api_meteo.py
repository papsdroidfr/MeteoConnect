import urequests as requests
import json

TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
INSEE_TEST = '78015'

class Meteo():
    '''recup donnees API meto https://api.meteo-concept.com/ 
    '''
    def __init__(self, insee=None):
        ''' constructeur '''
        self.insee = insee       # code INSEE de la ville a recuperer sous https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/table/
        self.forecast = None     # previsions meteo forecast des 12 prochaines heures
        
        #Token a obtenir sur API meto https://api.meteo-concept.com/ 
        self.mytoken = TOKEN
        
        self.URLAPI   = 'https://api.meteo-concept.com/api'
        self.GETHOURS = '/forecast/nextHours'
        self.HOURLY   = '&hourly=true' #GET forecast every  hour
        self.TOKEN  = '?token='+self.mytoken
        self.SEARCH = '&insee='+self.insee
        self.api_meteo_url = self.URLAPI+self.GETHOURS+self.TOKEN+self.HOURLY+self.SEARCH
        
        #--dictionnaire des codes retours API
        self.dic_STATUS= {
            200: "ok",
            400: "parametre manquant ou valeur incorrecte: verifier le token",
            401: "Echec de l'authentification: token absent ou invalide",
            403: "action non autorisee",
            404: "URL inconnue",
            500: "Erreur interne au serveur",
            503: "API momentanement indisponible",
            }
        
        #--dicctionnaire des buletins meteo de l'api meteo-concept
        self.dic_WEATHER = {
            0: "Soleil",
            1: "Peu nuageux",
            2: "Ciel voile",
            3: "Nuageux",
            4: "Tres nuageux",
            5: "Couvert",
            6: "Brouillard",
            7: "Brouillard givrant",
            10: "Pluie faible",
            11: "Pluie moderee",
            12: "Pluie forte",
            13: "Pluie faible verglacante",
            14: "Pluie moderee verglacante",
            15: "Pluie forte verglacante",
            16: "Bruine",
            20: "Neige faible",
            21: "Neige moderee",
            22: "Neige forte",
            30: "Pluie et neige melees faibles",
            31: "Pluie et neige melees moderees",
            32: "Pluie et neige melees fortes",
            40: "Averses de pluie locales et faibles",
            41: "Averses de pluie locales",
            42: "Averses locales et fortes",
            43: "Averses de pluie faibles",
            44: "Averses de pluie",
            45: "Averses de pluie fortes",
            46: "Averses de pluie faibles et frequentes",
            47: "Averses de pluie frequentes",
            48: "Averses de pluie fortes et frequentes",
            60: "Averses de neige localisees et faibles",
            61: "Averses de neige localisees",
            62: "Averses de neige localisees et fortes",
            63: "Averses de neige faibles",
            64: "Averses de neige",
            65: "Averses de neige fortes",
            66: "Averses de neige faibles et frequentes",
            67: "Averses de neige frequentes",
            68: "Averses de neige fortes et frequentes",
            70: "Averses de pluie et neige melees localisees et faibles",
            71: "Averses de pluie et neige melees localisees",
            72: "Averses de pluie et neige melees localisees et fortes",
            73: "Averses de pluie et neige melees faibles",
            74: "Averses de pluie et neige melees",
            75: "Averses de pluie et neige melees fortes",
            76: "Averses de pluie et neige melees faibles et nombreuses",
            77: "Averses de pluie et neige melees frequentes",
            78: "Averses de pluie et neige melees fortes et frequentes",
            100: "Orages faibles et locaux",
            101: "Orages locaux",
            102: "Orages fort et locaux",
            103: "Orages faibles",
            104: "Orages",
            105: "Orages forts",
            106: "Orages faibles et frequents",
            107: "Orages frequents",
            108: "Orages forts et frequents",
            120: "Orages faibles et locaux de neige ou gresil",
            121: "Orages locaux de neige ou gresil",
            122: "Orages locaux de neige ou gresil",
            123: "Orages faibles de neige ou gresil",
            124: "Orages de neige ou gresil",
            125: "Orages de neige ou gresil",
            126: "Orages faibles et frequents de neige ou gresil",
            127: "Orages frequents de neige ou gresil",
            128: "Orages frequents de neige ou gresil",
            130: "Orages faibles et locaux de pluie et neige melees ou gresil",
            131: "Orages locaux de pluie et neige melees ou gresil",
            132: "Orages fort et locaux de pluie et neige melees ou gresil",
            133: "Orages faibles de pluie et neige melees ou gresil",
            134: "Orages de pluie et neige melees ou gresil",
            135: "Orages forts de pluie et neige melees ou gresil",
            136: "Orages faibles et frequents de pluie et neige melees ou gresil",
            137: "Orages frequents de pluie et neige melees ou gresil",
            138: "Orages forts et frequents de pluie et neige melees ou gresil",
            140: "Pluies orageuses",
            141: "Pluie et neige melees a caractere orageux",
            142: "Neige a caractere orageux",
            210: "Pluie faible intermittente",
            211: "Pluie moderee intermittente",
            212: "Pluie forte intermittente",
            220: "Neige faible intermittente",
            221: "Neige moderee intermittente",
            222: "Neige forte intermittente",
            230: "Pluie et neige melees",
            231: "Pluie et neige melees",
            232: "Pluie et neige melees",
            235: "Averses de grele",
            }

    def get_forecast(self):
        ''' appel API: fourni le forecast des 12 prochaines heures sur un code insee
        '''
        #appel API
        self.forecast, status = None, None
        try:
            weather_data = requests.get(self.api_meteo_url)
        except:
            print('Pas de connexion WIFI')
            return status

        #code retour appel API
        status = weather_data.status_code
        if (status != 200):
            print('code retour API:', status, self.dic_STATUS[status])
            print('Pb connexion API: verifier le token ou la connexion WIFI:')
        else:
            self.forecast = weather_data.json()['forecast']
            self.city = weather_data.json()['city']['name']
        return status
    
    def decode_detail_meteo(self, id_forecast=0):
        ''' decode les donnees meteo des forecast obtenus
            id_forecast=0: heure en cours
        '''
        h, buletin, temp, hum , probarain, wind = None, None, None, None, None, None
        #on verifie que l'id-forecast ne depasse pas le nombre de forecast retournes.
        if (id_forecast >= len(self.forecast)):
            id_forecast = 0
        h = self.forecast[id_forecast]['datetime']          # heure prevision
        cbuletin = self.forecast[id_forecast]['weather']    # code buletin
        buletin = self.dic_WEATHER[cbuletin]                # buletin meteo
        temp = self.forecast[id_forecast]['temp2m']         # temperature
        hum = self.forecast[id_forecast]['rh2m']            # humidite
        probarain = self.forecast[id_forecast]['probarain'] # probabilite pluie
        wind = self.forecast[id_forecast]['wind10m']        # vitesse moyenne du vent
        return h, buletin, temp, hum, probarain, wind

if __name__ == "__main__":
    meteo = Meteo(insee=INSEE_TEST)
    while True:
        status = meteo.get_forecast(); # obtention du forecast pour les 12 prochaines heures
        if (status == 200) :           # retour API 200 =  ok
            h, buletin, temp, hum, probarain, wind = meteo.decode_detail_meteo(id_forecast=0)
            print('prevision meteo', h, 'a', meteo.city, ':', buletin, ',',
                  temp, '°C, humidite', hum,'%, proba pluie',probarain,'% , vent moyen', wind,'km/h' )
        time.sleep(10)  # wait 
