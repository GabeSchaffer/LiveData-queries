import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Parenthesis, TokenList
from sqlparse.tokens import Keyword, DML

def extract_tables_and_joins_from_token_list(token_list):
    tables = set()
    joins = set()
    from_seen = False
    join_seen = False
    for token in token_list.tokens:
        if token.ttype is Keyword and token.value.upper() == 'FROM':
            from_seen = True
        elif token.ttype is Keyword and 'JOIN' in token.value.upper():
            join_seen = True
        elif from_seen and isinstance(token, Identifier):
            tables.add(token.get_real_name())
            from_seen = False  # Reset the flag after capturing a table name
        elif join_seen and isinstance(token, Identifier):
            joins.add(token.get_real_name())
            join_seen = False  # Reset the flag after capturing a join
        elif isinstance(token, TokenList):
            # Recursively process the token list, collecting tables and joins
            sub_tables, sub_joins = extract_tables_and_joins_from_token_list(token)
            tables.update(sub_tables)
            joins.update(sub_joins)
            # Reset the flags after processing a nested structure
            from_seen = False
            join_seen = False
    return tables, joins

def extract_table_names_and_joins(sql):
    parsed = sqlparse.parse(sql)[0]
    return extract_tables_and_joins_from_token_list(parsed)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]) or not sys.argv[1].endswith('.sql'):
        print('Usage: python script.py <path to SQL file>')
        sys.exit(1)

    path = sys.argv[1]
    with open(path, 'r') as f:
        sql = f.read()

    tables, joins = extract_table_names_and_joins(sql)
    print('Tables:', ', '.join(tables))
    print('Joins:', ', '.join(joins))
