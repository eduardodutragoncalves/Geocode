import pycep_correios
from geopy.geocoders import Nominatim
import urllib3, json
import time



urlgetCeps = "http://covidbot.com.br/covidapi/paciente/ceps/"
urlpostCeps = 'http://covidbot.com.br/covidapi/paciente/ceps/'
geolocator = Nominatim(user_agent="CovidBot")
http = urllib3.PoolManager()
r = http.request('GET', urlgetCeps)
loaded_json = json.loads(r.data)
contaupdates = 1
for cepitem in loaded_json:
    print('*************Atualizando covidbot para cep: '+cepitem['cep']+' ***** '+str(contaupdates)+' de '+str(len(loaded_json))+' *****************')
    try:
        contaupdates = contaupdates + 1
        endereco = pycep_correios.get_address_from_cep(cepitem['cep_corrigido'])
        enderecoreq = endereco['logradouro']+','+endereco['bairro']+','+endereco['cidade'] 
        logradouro  = endereco['logradouro']
        bairro      = endereco['bairro']
        cidade      = endereco['cidade']
        cep         = cepitem['cep']
        uf          = endereco['uf']
        cep_cor     = cepitem['cep_corrigido']
        print('Logradouro: '+logradouro)
        print('Bairro: '    +bairro)
        print('Cidade: '    +cidade)
        print('uf: '        +uf)
        print('Cep: '       +cep)
        print('Cep Corrigido: ' +cep_cor)
        try:
            print('Buscando dados de latlong....')
            print('Endereço de Busca: '+enderecoreq)
            location = geolocator.geocode(enderecoreq,True,5)
            #caso não encontre com rua, bairro e cidade, verifica apenas com bairro e cidade
            if(location == None):
                time.sleep(3)
                enderecoreq = endereco['bairro']+','+endereco['cidade'] 
                location = geolocator.geocode(enderecoreq,True,5)
                
        except:
            print('Não foi possível encontrar latlong desse endereço')            
        
        try:
            #jsonUpdateCep = '{\"cidade\":\"'+cidade+'\",'
            #jsonUpdateCep = jsonUpdateCep+'\"cep\":\"'+cep+'\",'
            #jsonUpdateCep = jsonUpdateCep+'\"cep_corrigido\":\"'+cep_cor+'\",'
            #jsonUpdateCep = jsonUpdateCep+'\"bairro\":\"'+bairro+'\",'
            #jsonUpdateCep = jsonUpdateCep+'\"logradouro\":\"'+logradouro+'\",'
            #jsonUpdateCep = jsonUpdateCep+'\"uf\":\"'+uf+'\",'
            if(location != None):
                #jsonUpdateCep = jsonUpdateCep+'\"latitude\":'+str(location.latitude)+','
                #jsonUpdateCep = jsonUpdateCep+'\"longitude\":'+str(location.longitude)+'}'
                dictCepUpdate = {'cidade':cidade,'cep':cep,'cep_corrigido':cep_cor,'bairro':bairro,'logradouro':logradouro,'uf':uf,'latitude':location.latitude,'longitude':location.longitude}
            else:
                #jsonUpdateCep = jsonUpdateCep+'\"latitude\":'+str(0.0)+','
                #jsonUpdateCep = jsonUpdateCep+'\"longitude\":'+str(0.0)+'}'
                dictCepUpdate = {'cidade':cidade,'cep':cep,'cep_corrigido':cep_cor,'bairro':bairro,'logradouro':logradouro,'uf':uf,'latitude':0,'longitude':0}

            jsonUpdateCepDump = json.dumps(dictCepUpdate)
            print('\n'+jsonUpdateCepDump)
            r = http.request('POST', urlpostCeps,headers={'Content-Type': 'application/json'},body=jsonUpdateCepDump)
            print(r.data)
        except:
            print('Erro ao enviar os dados para o covidbot.com')                        
        
    except:
        print('Não foi possível encontrar o endereço desse CEP')

    print('********Fim***********')
    print('\n')        
    time.sleep(5)


      
      

