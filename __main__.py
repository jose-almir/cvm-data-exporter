"""Comissão de Valores Mobiliários - CLI

Usage:
  cvm-cli --CIA_ABERTA --CAD [--exportar]
  cvm-cli --CIA_ABERTA --DOC <tipo> <demonstrativo> <ano> <info> [--ultimo-periodo] [--exportar]

Options:
  -h --help          Mostra ajuda de comandos do CLI.
  -v                 Versão atual do CLI.
  --ultimo-periodo   Calcula as demonstrações do período 31/12
  --exportar         Salva localmente os dados, ao invés de enviar para base remota.
"""

import docopt

from commands.cia_aberta_cad import CiaAbertaCad
from commands.cia_aberta_doc import CiaAbertaDoc

commands = {'CIA_ABERTA': {
    'CAD': CiaAbertaCad(),
    'DOC': CiaAbertaDoc()
    }
}

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version='cvm-cli v.1.1')
    if args['--CIA_ABERTA']:
        if args['--CAD']:
            command = commands['CIA_ABERTA']['CAD']
            command(export=args['--exportar'])
        else:
            command = commands['CIA_ABERTA']['DOC']
            command(args['<tipo>'], args['<demonstrativo>'], args['<ano>'], args['<info>'],
                    ultimo_periodo=args['--ultimo-periodo'], export=args['--exportar'])
