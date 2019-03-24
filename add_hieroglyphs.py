from sqlalchemy import create_engine, MetaData, Table
import pandas as pd
import json


def make_json(serries):
    for i, val in enumerate(serries[:-2]):
        if ' / ' in val:
            serries[i] = json.dumps(val.split(' / '))
        elif ', ' in val:
            serries[i] = json.dumps(val.split(', '))
        elif '; ' in val:
            serries[i] = json.dumps(val.split(', '))
        else:
            serries[i] = json.dumps([val])
    return serries


if __name__ == '__main__':
    meta = MetaData()
    table = pd.read_html('http://www.study-languages-online.com/ru/jp/kanji_01.html')[0]
    table = table.drop('Начертание', 1)
    table['Кун'] = make_json(table['Кун'])
    table['Он'] = make_json(table['Он'])
    table['Перевод'] = make_json(table['Перевод'])
    engine = create_engine('postgresql://shvaindahder:x-user123@localhost:5432/japanese_flask')
    conn = engine.connect()
    t = Table('hieroglyph', meta, autoload=True, autoload_with=engine)
    ins = t.insert()
    for index, row in table.iterrows():
        print(index)
        conn.execute(ins.values(hieroglyph=row["Иероглиф"], translation=row["Перевод"],
                                onyomi=row["Он"], kunyomi=row["Кун"]))