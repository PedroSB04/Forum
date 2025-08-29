from website.database import execute_sql

def popular_banco():
    # Inserindo usuários'kijux
    execute_sql("""
        INSERT INTO usuario (
            nome,
            username,
            email,
            senha,
            foto_perfil,
            data_criacao,
            biografia
        ) VALUES
        (
            'João Silva',
            'joaosilva',
            'joao.silva@email.com',
            'senha123',
            'joao_perfil.jpg',
            '2024-05-10 10:00:00',
            'Entusiasta de tecnologia e programador iniciante.'
        ),
        (
            'Maria Souza',
            'mariasouza',
            'maria.souza@email.com',
            'maria123',
            'maria_perfil.png',
            '2024-05-11 11:30:00',
            'Designer gráfica e apaixonada por arte digital.'
        ),
        (
            'Pedro Lima',
            'pedrolima',
            'pedro.lima@email.com',
            'pedro123',
            'pedro_perfil.jpg',
            '2024-05-12 12:45:00',
            'Professor de história e amante de literatura.'
        ),
        (
            'Ana Costa',
            'anacosta',
            'ana.costa@email.com',
            'anacosta456',
            'ana_perfil.png',
            '2024-05-13 13:00:00',
            'Desenvolvedora full-stack e entusiasta de código aberto.'
        ),
        (
            'Carlos Oliveira',
            'carlosoliver',
            'carlos.o@email.com',
            'carlitos',
            'carlos_perfil.jpg',
            '2024-05-14 14:20:00',
            'Cientista de dados, focado em machine learning.'
        );
    """)

    # Inserindo categorias
    execute_sql("""
        INSERT INTO categoria (nome) VALUES
        ('Python'),
        ('JavaScript'),
        ('C#'),
        ('Java'),
        ('Banco de Dados'),
        ('DevOps'),
        ('Segurança'),
        ('IA'),
        ('Mobile'),
        ('Web');
    """)

    # Inserindo posts
    execute_sql("""
        INSERT INTO post (titulo, conteudo, likes, dislikes, id_usuario) VALUES
        ('Introdução a APIs REST com Flask', 'Compartilhando boas práticas para criar APIs REST em Flask.', 3, 1, 1),
        ('Por que React ainda domina o mercado?', 'Discussão sobre vantagens e desvantagens do React em 2025.', 4, 0, 2),
        ('Flutter vs React Native em 2025', 'Comparação atualizada entre Flutter e RN.', 2, 1, 3),
        ('Melhores práticas de CI/CD', 'Como aplicar CI/CD em projetos usando GitHub Actions.', 5, 2, 4),
        ('Meu setup de desenvolvimento Python', 'Ferramentas que uso diariamente para ser produtiva.', 1, 0, 1),
        ('Introdução ao Kubernetes', 'Passo a passo para rodar aplicações no Kubernetes.', 3, 2, 4),
        ('Banco de Dados Relacional vs NoSQL', 'Quando escolher cada um.', 2, 1, 8),
        ('Introdução ao Machine Learning', 'Explicando ML para iniciantes.', 5, 1, 6),
        ('Boas práticas em UX para devs', 'Pequenos ajustes que melhoram muito a experiência.', 3, 0, 9),
        ('C# para jogos com Unity', 'Compartilho um pouco da minha experiência criando jogos.', 4, 2, 7);
    """)

    # Relacionando posts com categorias
    execute_sql("""
        INSERT INTO post_categoria (id_post, id_categoria) VALUES
        (1, 1), (1, 10),
        (2, 2), (2, 10),
        (3, 9), (3, 2),
        (4, 6), (4, 5),
        (5, 1),
        (6, 6),
        (7, 5),
        (8, 8), (8, 1),
        (9, 10),
        (10, 3);
    """)

if __name__ == "__main__":
    popular_banco()
    print("Banco de dados populado com sucesso!")