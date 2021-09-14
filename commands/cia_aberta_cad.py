from api.cvm import cia_aberta_cad
from database.mongo import send_cia_aberta_cad
import json

from utils.create_folder import create_folder


class CiaAbertaCad:
    def __call__(self, export=False):
        data = cia_aberta_cad()
        if export:
            create_folder('out')
            with open('out/cad_cia_aberta.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        else:
            send_cia_aberta_cad(data)
