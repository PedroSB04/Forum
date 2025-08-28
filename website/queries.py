from flask import current_app, request
from flask_login import current_user
from forms import Formlogin, Formsignup
import db

from website.database import execute_sql

"""
# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df# Subquery para métricas básicas de produtos
    subquery_produtos = session.query(
        Produto.id_produto,
        Produto.nome_produto,
        Categoria.nome_categoria,
        Produto.preco_unitario,
        Produto.custo_producao,
        func.coalesce(func.sum(Venda.quantidade), 0).label('total_vendido'),
        func.coalesce(func.sum(Venda.valor_total), 0).label('receita_total'),
        func.coalesce(func.count(Venda.id_venda), 0).label('vendas_count')
    ).join(Categoria, Produto.id_categoria == Categoria.id_categoria)\
     .outerjoin(Venda, Produto.id_produto == Venda.id_produto)\
     .group_by(Produto.id_produto, Produto.nome_produto, Categoria.nome_categoria, 
               Produto.preco_unitario, Produto.custo_producao)\
     .subquery()
    
    # Query principal com cálculos de rentabilidade
    resultados = session.query(
        subquery_produtos.c.id_produto,
        subquery_produtos.c.nome_produto,
        subquery_produtos.c.nome_categoria,
        subquery_produtos.c.preco_unitario,
        subquery_produtos.c.custo_producao,
        subquery_produtos.c.total_vendido,
        subquery_produtos.c.receita_total,
        subquery_produtos.c.vendas_count,
        (subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).label('lucro_total'),
        ((subquery_produtos.c.preco_unitario - subquery_produtos.c.custo_producao) / subquery_produtos.c.preco_unitario * 100).label('margem_contribuicao_percent'),
        (subquery_produtos.c.receita_total / subquery_produtos.c.vendas_count).label('ticket_medio'),
        func.rank().over(
            order_by=(subquery_produtos.c.receita_total - (subquery_produtos.c.custo_producao * subquery_produtos.c.total_vendido)).desc()
        ).label('ranking_lucratividade'),
        func.rank().over(
            order_by=subquery_produtos.c.total_vendido.desc()
        ).label('ranking_vendas')
    ).all()
    
    # Processamento dos resultados
    df = pd.DataFrame([{
        'id_produto': r.id_produto,
        'nome_produto': r.nome_produto,
        'categoria': r.nome_categoria,
        'preco_unitario': float(r.preco_unitario) if r.preco_unitario else 0,
        'custo_producao': float(r.custo_producao) if r.custo_producao else 0,
        'total_vendido': r.total_vendido,
        'receita_total': float(r.receita_total) if r.receita_total else 0,
        'vendas_count': r.vendas_count,
        'lucro_total': float(r.lucro_total) if r.lucro_total else 0,
        'margem_contribuicao': float(r.margem_contribuicao_percent) if r.margem_contribuicao_percent else 0,
        'ticket_medio': float(r.ticket_medio) if r.ticket_medio else 0,
        'ranking_lucratividade': r.ranking_lucratividade,
        'ranking_vendas': r.ranking_vendas
    } for r in resultados])
    
    # Cálculos adicionais
    df['lucro_por_unidade'] = df['lucro_total'] / df['total_vendido'].replace(0, 1)
    df['rotatividade'] = df['total_vendido'] / df['vendas_count'].replace(0, 1)
    
    return df
"""

#implementar na barra de busca
def barra_de_busca(palavra):
    query = """
        SELECT
            username,
            conteudo,
            titulo
        FROM
            usuario
        JOIN
            post
        WHERE 
            username ILIKE %s OR
            conteudo ILIKE %s OR
            titulo ILIKE %s
    """
    params = (f"%{palavra}%", f"%{palavra}%", f"%{palavra}%")
    resultados = execute_sql(query, params, fetch=True)
    return resultados


#funções de interação com posts
def like(post_id):
    query = """
        UPDATE post
        SET likes = likes + 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def retirar_like(post_id):
    query = """
        UPDATE post
        SET likes = likes - 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def dislike(post_id):
    query = """
        UPDATE post
        SET dislikes = dislikes + 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def retirar_dislike(post_id):
    query = """
        UPDATE post
        SET dislikes = dislikes - 1
        WHERE id = %s
    """
    params = (post_id,)
    execute_sql(query, params)

def seguir(usuario_id):
    if usuario_id == current_user.id:
        raise ValueError("Você não pode seguir a si mesmo.")
    query = """
        INSERT INTO segue (seguidor_id, seguido_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """
    params = (current_user.id, usuario_id)
    execute_sql(query, params)

def deixar_seguir(usuario_id):
    if usuario_id == current_user.id:
        raise ValueError("Você não pode deixar de seguir a si mesmo.")
    query = """
        DELETE FROM segue
        WHERE seguidor_id = %s AND seguido_id = %s
    """
    params = (current_user.id, usuario_id)
    execute_sql(query, params)

#retorna as informações do perfil do usuário
def informacoes_perfil(usuario_id):
    query = """
        SELECT
            nome,
            username,
            email,
            foto_perfil,
            (SELECT COUNT(*) FROM segue WHERE seguido_id = %s) AS seguidores,
            (SELECT COUNT(*) FROM segue WHERE seguidor_id = %s) AS seguindo
        FROM
            usuario
        WHERE
            id = %s
    """
    params = (usuario_id, usuario_id, usuario_id)
    return execute_sql(query, params, fetch=True)

#funções de ordenação
def ordena_por_likes():
    query = "SELECT * FROM post ORDER BY likes DESC"
    return execute_sql(query, fetch=True)

def ordena_por_dislikes():
    query = "SELECT * FROM post ORDER BY dislikes DESC"
    return execute_sql(query, fetch=True)

def ordena_por_data_decrescente():
    query = "SELECT * FROM post ORDER BY data_post DESC"
    return execute_sql(query, fetch=True)

def ordena_por_data_crescente():
    query = "SELECT * FROM post ORDER BY data_post ASC"
    return execute_sql(query, fetch=True)

def filtrar_categoria(categoria):
    query = """
        SELECT * FROM post
        WHERE categoria = %s
    """
    params = (categoria,)
    return execute_sql(query, params, fetch=True)
