#!/usr/bin/env python3

import connexion

from imm_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./apispec/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('ImmMatch_API_1_0_0.yaml', arguments={'title': 'ImmunoMatch'}, pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
