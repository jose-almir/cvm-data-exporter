import io
import json
import os
import zipfile

import pandas as pd
import requests

from api.endpoints import endpoints
from utils.create_folder import create_folder
from utils.transform_data import camel_case, scale_monetary


def cia_aberta_cad():
    create_folder('.cache')
    if not os.path.exists(f'.cache/cad_cia_aberta.csv'):
        url = endpoints['CIA_ABERTA']['CAD']
        response = requests.get(url)

        assert response.status_code == 200, "Failed request"

        with open('.cache/cad_cia_aberta.csv', 'w', encoding='utf-8') as f:
            f.write(response.text)

    df = pd.read_csv('.cache/cad_cia_aberta.csv', sep=';', encoding='utf-8')
    df = df.rename(columns={k: camel_case(k) for k in df.columns.values})

    return json.loads(df.to_json(orient='records'))


def cia_aberta_doc(tipo, dem, ano, info):
    create_folder('.cache')

    def transform(name):
        df = pd.read_csv(f'.cache/{name}', sep=';', encoding='iso-8859-15')
        df = df.infer_objects()
        df = df.rename(columns={k: camel_case(k) for k in df.columns.values})
        df = df.drop_duplicates(['cnpjCia', 'denomCia', 'cdCvm', 'dtRefer', 'cdConta'], keep='last')
        df = df[df.ordemExerc == 'ÚLTIMO']
        df = df[~(df.cdConta.str.startswith('3.99'))]
        df = df[(df.cdConta.str.len() <= 13)]
        df['vlConta'] = df.apply(scale_monetary, axis=1)
        df = df.drop(
            ['moeda', 'grupoDfp', 'versao', 'ordemExerc', 'stContaFixa', 'escalaMoeda', 'dtIniExerc', 'dtFimExerc',
             ], axis=1, errors='ignore')
        indices = df.groupby(['cnpjCia', 'denomCia', 'cdCvm', 'dtRefer']).indices

        data = []

        for key in indices:
            cnpj, denom_cia, cd_cvm, dt_refer = key
            accounts_indices = indices[key]

            document = {'tipo': tipo,
                        'info': info,
                        'demonstrativo': dem.replace('_', ' '),
                        'ano': ano,
                        'cnpjCia': cnpj,
                        'denomCia': denom_cia,
                        'cdCvm': int(cd_cvm),
                        'dtRefer': dt_refer,
                        'contas': []
                        }

            for i in accounts_indices:
                row = df.iloc[i]
                cd_conta, ds_conta, vl_conta = row[4:]
                document['contas'].append({'cdConta': cd_conta, 'dsConta': ds_conta, 'vlConta': vl_conta})

            data.append(document)

        return data

    filename = None

    for file in os.listdir('.cache'):
        if dem in file and info.lower() and tipo.lower() in file and ano in file:
            filename = file

    if filename:
        return transform(filename)
    else:
        url = endpoints['CIA_ABERTA']['DOC'][tipo][ano]

        response = requests.get(url)

        assert response.status_code == 200, "Failed request"

        raw = io.BytesIO(response.content)

        zip_file = zipfile.ZipFile(raw)

        for file in zip_file.filelist:
            if dem in file.filename and info.lower() in file.filename:
                zip_file.extract(file.filename, path='.cache')
                return transform(file.filename)
