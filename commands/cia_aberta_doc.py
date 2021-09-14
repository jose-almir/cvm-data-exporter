import json

from api.cvm import cia_aberta_doc
from database.mongo import send_cia_aberta_doc
from utils.create_folder import create_folder


class CiaAbertaDoc:
    def __call__(self, tipo, dem, ano, info, ultimo_periodo=False, export=False):
        data = None

        if ultimo_periodo:
            data = []
            dfp = cia_aberta_doc('DFP', dem, ano, info)
            itr = cia_aberta_doc('ITR', dem, ano, info)
            for r in dfp:
                document = {'tipo': 'ITR',
                            'info': info,
                            'demonstrativo': dem,
                            'ano': ano,
                            'cnpjCia': r['cnpjCia'],
                            'denomCia': r['denomCia'],
                            'cdCvm': r['cdCvm'],
                            'dtRefer': f'{ano}-12-31',
                            'contas': r['contas'].copy()
                            }
                cods = list(map(lambda c: c['cdConta'], document['contas']))
                itrs = list(filter(lambda d: d['cnpjCia'] == r['cnpjCia'], itr))
                for itr_f in itrs:
                    for i in range(len(cods)):
                        current = list(filter(lambda c: c['cdConta'] == cods[i], itr_f['contas']))
                        if len(current) > 0:
                            document['contas'][i]['vlConta'] -= current[0]['vlConta']

                data.append(document)
        else:
            data = cia_aberta_doc(tipo, dem, ano, info)

        if data:
            if export:
                create_folder('out')
                with open(f'out/{tipo.lower()}_cia_aberta_{dem}_{info.lower()}_{ano}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
            else:
                send_cia_aberta_doc(data)
