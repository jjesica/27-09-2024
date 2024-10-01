import sqlite3

# Conectar ao banco de dados de cursos
conn = sqlite3.connect('cursos.db')
cursor = conn.cursor()

# Criar tabela de cursos se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS Cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    duracao INTEGER NOT NULL
)
''')

conn.commit()
conn.close()
