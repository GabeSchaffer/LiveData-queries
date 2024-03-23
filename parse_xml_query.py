import os
import sqlparse
from sqlparse.sql import Identifier, Parenthesis, TokenList
from sqlparse.tokens import Keyword, Name


def is_valid_table_name(identifier):
    # Add more SQL functions or keywords here as needed
    invalid_names = {"XMLElement", "XMLAttribute", "XMLAgg", "GetClobVal"}
    return identifier.get_real_name() not in invalid_names


def extract_tables_from_token_list(token_list, within_from=False):
    tables = set()
    for token in token_list.tokens:
        if token.ttype is Keyword and token.value.upper() == 'FROM':
            within_from = True
        elif within_from and isinstance(token, Identifier) and is_valid_table_name(token):
            tables.add(token.get_real_name())
            within_from = False  # Reset after capturing a table
        elif isinstance(token, Parenthesis) or isinstance(token, TokenList):
            tables.update(extract_tables_from_token_list(token, within_from))
        elif token.is_group:
            tables.update(extract_tables_from_token_list(token, within_from))
    return tables


def extract_table_names(sql):
    parsed = sqlparse.parse(sql)[0]
    return extract_tables_from_token_list(parsed)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]) or not sys.argv[1].endswith('.sql'):
        print(f'Usage: python {sys.argv[0]} <path to SQL file>')
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r') as f:
        sql = f.read()

    tables = extract_table_names(sql)
    print('Tables:', ', '.join(tables))
