
from urllib.request import urlopen
import json



def contact(mid,flds,types):
    url = "https://api.406registration.com/poc/bymid/{}".format(str(mid))
    contact={}
    for type in types:
        contact[type]={}
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        eltcontact=data["POCELT"]
        epirbcontact = data["POCEPIRB"]
        plbcontact = data["POCPLB"]
        alldata = data["references"]
        for type in types:
            for d in alldata:
                #contact[type] = {}
                if "_id" in d and d["_id"]==data[type] :
                    contact[type] = {}
                    for fld in flds:
                        if fld in d:
                            try:
                                contact[type][fld]=d[fld]
                            except:
                                contact[type][fld] = 'n/a'


    except:
        for type in types:
            contact[type]={}


    return contact
