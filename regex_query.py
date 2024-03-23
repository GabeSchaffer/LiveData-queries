import sqlparse
from sqlparse.sql import Identifier, TokenList, Parenthesis
from sqlparse.tokens import Keyword

def extract_tables_and_joins(token_list, within_join=False):
    tables = set()
    joins = set()

    for token in token_list.tokens:
        if token.ttype is Keyword and 'JOIN' in token.value.upper():
            within_join = True
        elif within_join and isinstance(token, Identifier):
            # Capture the table name following the JOIN keyword
            joins.add(token.get_real_name())
            within_join = False  # Reset after capturing the join table
        elif isinstance(token, Identifier):
            # Capture tables from the FROM clause
            tables.add(token.get_real_name())
        elif isinstance(token, Parenthesis) or isinstance(token, TokenList):
            # Recursively process nested tokens
            nested_tables, nested_joins = extract_tables_and_joins(token, within_join)
            tables.update(nested_tables)
            joins.update(nested_joins)

    return tables, joins

def extract_table_names_and_joins(sql):
    parsed = sqlparse.parse(sql)[0]
    return extract_tables_and_joins(parsed)

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
