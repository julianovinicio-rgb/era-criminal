#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cálculos penais da Trilha Criminal.

Faz a aritmética de datas, frações e penas e devolve uma memória de cálculo
conferível. Não escolhe prazo, fração, marco, feriado nem lei aplicável: tudo
isso entra como dado, com a fonte conferida por quem executa.

Uso:
  python calculos.py modelo <comando>             imprime um modelo de entrada
  python calculos.py <comando> --entrada arq.json
  python calculos.py <comando> --json "{...}"
  python calculos.py <comando> < arq.json
  python calculos.py autoteste

Comandos: prazo, prescricao, pena, execucao, remicao, periodos.
Somente biblioteca padrão. Python 3.8 ou superior.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import date, timedelta
from fractions import Fraction

VERSAO = "1.0.0"
UM = timedelta(days=1)
SEMANA = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
          "sexta-feira", "sábado", "domingo"]
COMANDOS = ["prazo", "prescricao", "pena", "execucao", "remicao", "periodos"]


class ErroEntrada(Exception):
    """Entrada ausente, ambígua ou incoerente. Nunca é corrigida em silêncio."""


# --------------------------------------------------------------------------
# Leitura e validação
# --------------------------------------------------------------------------

def conferir_campos(obj, aceitos, contexto):
    if not isinstance(obj, dict):
        raise ErroEntrada(f"{contexto}: esperado um objeto com campos nomeados")
    extras = sorted(set(obj) - set(aceitos))
    if extras:
        raise ErroEntrada(
            f"{contexto}: campo não reconhecido: {', '.join(extras)}. "
            f"Campos aceitos: {', '.join(sorted(aceitos))}")


def exigir(obj, campo, contexto):
    if not isinstance(obj, dict) or obj.get(campo) in (None, "", []):
        raise ErroEntrada(f"{contexto}: falta o campo obrigatório '{campo}'")
    return obj[campo]


def ler_data(valor, contexto):
    if not isinstance(valor, str):
        raise ErroEntrada(f"{contexto}: data deve ser texto, como 2026-03-10 ou 10/03/2026")
    s = valor.strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        ano, mes, dia = (int(x) for x in m.groups())
    else:
        m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
        if not m:
            raise ErroEntrada(f"{contexto}: data '{valor}' fora do formato aaaa-mm-dd ou dd/mm/aaaa")
        dia, mes, ano = (int(x) for x in m.groups())
    try:
        return date(ano, mes, dia)
    except ValueError:
        raise ErroEntrada(f"{contexto}: a data '{valor}' não existe no calendário") from None


def ler_inteiro(valor, contexto, minimo=0):
    if isinstance(valor, bool) or not isinstance(valor, (int, str)):
        raise ErroEntrada(f"{contexto}: esperado número inteiro")
    try:
        n = int(str(valor).strip())
    except ValueError:
        raise ErroEntrada(f"{contexto}: '{valor}' não é número inteiro") from None
    if n < minimo:
        raise ErroEntrada(f"{contexto}: o valor mínimo é {minimo}")
    return n


def ler_fracao(valor, contexto):
    """Aceita '1/6', '25%', '0,25' ou '4/3'. Sempre positiva."""
    s = re.sub(r"\s+", "", str(valor)).replace(",", ".")
    try:
        f = Fraction(s[:-1]) / 100 if s.endswith("%") else Fraction(s)
    except (ValueError, ZeroDivisionError):
        raise ErroEntrada(f"{contexto}: fração '{valor}' inválida; use 1/6, 25% ou 0,25") from None
    if f <= 0:
        raise ErroEntrada(f"{contexto}: a fração deve ser maior que zero")
    return f


_DUR = re.compile(r"(\d+)\s*(anos?|a|meses|m[eê]s|m|dias?|d)(?![a-zêç])", re.I)


def ler_duracao(valor, contexto):
    """Aceita '5a4m10d', '5 anos e 4 meses', '64m', '120d' ou {anos, meses, dias}."""
    if isinstance(valor, dict):
        conferir_campos(valor, {"anos", "meses", "dias"}, contexto)
        return tuple(ler_inteiro(valor.get(k, 0), f"{contexto}.{k}") for k in ("anos", "meses", "dias"))
    if not isinstance(valor, str):
        raise ErroEntrada(f"{contexto}: informe a unidade, como '5a4m' ou '120d'")
    s = valor.lower().strip()
    partes = _DUR.findall(s)
    sobra = re.sub(r"[\s,e]+", "", _DUR.sub("", s))
    if not partes or sobra:
        raise ErroEntrada(f"{contexto}: duração '{valor}' não reconhecida; use, por exemplo, '5a4m10d'")
    a = m = d = 0
    for n, unidade in partes:
        if unidade.startswith("a"):
            a += int(n)
        elif unidade.startswith("m"):
            m += int(n)
        else:
            d += int(n)
    return a, m, d


def ler_periodos(lista, contexto, campo_ini, campo_fim, aberto, fim_inclusivo, sobrepor=False):
    """Devolve [(início, fim exclusivo ou None, descrição)], em ordem."""
    saida = []
    if lista in (None, []):
        return saida
    if not isinstance(lista, list):
        raise ErroEntrada(f"{contexto}: esperado uma lista")
    for i, p in enumerate(lista, 1):
        ctx = f"{contexto}[{i}]"
        conferir_campos(p, {campo_ini, campo_fim, "descricao"}, ctx)
        ini = ler_data(exigir(p, campo_ini, ctx), f"{ctx}.{campo_ini}")
        bruto = p.get(campo_fim)
        if bruto in (None, ""):
            if not aberto:
                raise ErroEntrada(f"{ctx}: falta o campo obrigatório '{campo_fim}'")
            fim = None
        else:
            fim = ler_data(bruto, f"{ctx}.{campo_fim}")
            if fim_inclusivo:
                if fim < ini:
                    raise ErroEntrada(f"{ctx}: '{campo_fim}' é anterior a '{campo_ini}'")
                fim += UM
            elif fim <= ini:
                raise ErroEntrada(f"{ctx}: '{campo_fim}' deve ser posterior a '{campo_ini}'")
        saida.append((ini, fim, str(p.get("descricao") or f"período {i}").strip()))
    saida.sort(key=lambda t: t[0])
    if not sobrepor:
        for (a1, b1, d1), (a2, _b2, d2) in zip(saida, saida[1:]):
            if b1 is None or a2 < b1:
                raise ErroEntrada(
                    f"{contexto}: os períodos '{d1}' e '{d2}' se sobrepõem. "
                    "Una-os ou corrija as datas antes de calcular")
    return saida


# --------------------------------------------------------------------------
# Datas, durações e formatação
# --------------------------------------------------------------------------

def ultimo_dia_do_mes(ano, mes):
    return (date(ano + (mes == 12), mes % 12 + 1, 1) - UM).day


def soma_meses(d, n):
    """Soma meses pelo calendário; se o dia não existir no mês de destino, usa o último."""
    ano = d.year + (d.month - 1 + n) // 12
    mes = (d.month - 1 + n) % 12 + 1
    return date(ano, mes, min(d.day, ultimo_dia_do_mes(ano, mes)))


def dif_calendario(d1, d2):
    """Anos, meses e dias de d1 até d2 (d2 não incluído), pelo calendário."""
    meses = (d2.year - d1.year) * 12 + (d2.month - d1.month)
    if soma_meses(d1, meses) > d2:
        meses -= 1
    return meses // 12, meses % 12, (d2 - soma_meses(d1, meses)).days


def dur_dias(dur, ano, mes):
    return dur[0] * ano + dur[1] * mes + dur[2]


def dias_dur(n, ano=360, mes=30):
    a, r = divmod(n, ano)
    m = min(r // mes, 11)
    return a, m, r - m * mes


def plural(n, um, varios):
    return f"{n} {um if n == 1 else varios}"


def fdur(dur):
    a, m, d = dur
    partes = []
    if a:
        partes.append(plural(a, "ano", "anos"))
    if m:
        partes.append(plural(m, "mês", "meses"))
    if d or not partes:
        partes.append(plural(d, "dia", "dias"))
    return partes[0] if len(partes) == 1 else ", ".join(partes[:-1]) + " e " + partes[-1]


def fd(d):
    return d.strftime("%d/%m/%Y")


def fds(d):
    return f"{fd(d)} ({SEMANA[d.weekday()]})"


def ffrac(f):
    if f.denominator == 1:
        return str(f.numerator)
    pct = f * 100
    if f.denominator > 12 and pct.denominator == 1:
        return f"{pct.numerator}%"
    return f"{f.numerator}/{f.denominator}"


def fnum(valor):
    if isinstance(valor, Fraction) and valor.denominator == 1:
        return str(valor.numerator)
    return f"{float(valor):.2f}".replace(".", ",")


# --------------------------------------------------------------------------
# Memória de cálculo
# --------------------------------------------------------------------------

class Memoria:
    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = str(descricao or "").strip()
        self.linhas = []
        self.avisos = []
        self.dados = {}

    def secao(self, nome):
        self.linhas += ["", f"## {nome}", ""]

    def linha(self, texto=""):
        self.linhas.append(texto)

    def item(self, texto):
        self.linhas.append(f"- {texto}")

    def tabela(self, cabecalho, linhas):
        limpa = lambda c: str(c).replace("|", "/").replace("\n", " ")
        self.linhas.append("| " + " | ".join(cabecalho) + " |")
        self.linhas.append("|" + "---|" * len(cabecalho))
        for l in linhas:
            self.linhas.append("| " + " | ".join(limpa(c) for c in l) + " |")

    def aviso(self, texto):
        self.avisos.append(texto)

    def markdown(self):
        saida = [f"# Memória de cálculo: {self.titulo}"]
        if self.descricao:
            saida += ["", f"Objeto: {self.descricao}"]
        saida += self.linhas
        if self.avisos:
            saida += ["", "## Avisos", ""] + [f"- {a}" for a in self.avisos]
        saida += ["", f"Gerado por calculos.py {VERSAO} (Trilha Criminal). O script faz a aritmética. "
                      "Prazo, fração, marcos, feriados e lei aplicável são entradas de quem o executou "
                      "e precisam de fonte conferida."]
        return "\n".join(saida) + "\n"


def data_de_corte(e, hoje, mem):
    if e.get("data_corte"):
        return ler_data(e["data_corte"], "data_corte")
    mem.aviso(f"Data de corte não informada: usada a data do sistema, {fd(hoje)}. Informe 'data_corte' "
              "para fixar a data da análise.")
    return hoje


def desloca_por_paradas(inicio, limite, paradas):
    """Adia 'limite' pelos dias de cada parada que começa antes dele.

    Devolve (novo limite ou None, paradas aplicadas, parada em aberto ou None).
    """
    aplicadas = []
    for a, b, desc in paradas:
        if b is not None and b <= inicio:
            continue
        a_ef = max(a, inicio)
        if a_ef > limite:
            continue
        if b is None:
            return None, aplicadas, {"desde": a_ef, "restam": (limite - a_ef).days + 1, "descricao": desc}
        limite += b - a_ef
        aplicadas.append((a_ef, b, (b - a_ef).days, desc))
    return limite, aplicadas, None


def dias_parados(paradas, ini, fim):
    """Dias de parada dentro de [ini, fim)."""
    total = 0
    for a, b, _ in paradas:
        a_ef, b_ef = max(a, ini), min(b or fim, fim)
        if b_ef > a_ef:
            total += (b_ef - a_ef).days
    return total


# --------------------------------------------------------------------------
# prazo: prazo processual
# --------------------------------------------------------------------------

def cmd_prazo(e, hoje):
    conferir_campos(e, {"descricao", "evento", "dias", "contagem", "dias_sem_expediente", "suspensoes"}, "entrada")
    ev = exigir(e, "evento", "entrada")
    conferir_campos(ev, {"tipo", "data"}, "evento")
    tipo = exigir(ev, "tipo", "evento")
    if tipo not in ("intimacao", "disponibilizacao_dje"):
        raise ErroEntrada("evento.tipo: use 'intimacao' ou 'disponibilizacao_dje'")
    data_ev = ler_data(exigir(ev, "data", "evento"), "evento.data")
    n = ler_inteiro(exigir(e, "dias", "entrada"), "dias", minimo=1)
    contagem = exigir(e, "contagem", "entrada")
    if contagem not in ("corridos", "uteis"):
        raise ErroEntrada("contagem: use 'corridos' ou 'uteis'")

    sem_exp = {}
    for i, it in enumerate(e.get("dias_sem_expediente") or [], 1):
        ctx = f"dias_sem_expediente[{i}]"
        if isinstance(it, dict):
            conferir_campos(it, {"data", "descricao"}, ctx)
            sem_exp[ler_data(exigir(it, "data", ctx), ctx)] = str(it.get("descricao") or "").strip()
        else:
            sem_exp[ler_data(it, ctx)] = ""
    susp = ler_periodos(e.get("suspensoes"), "suspensoes", "primeiro_dia", "ultimo_dia",
                        aberto=False, fim_inclusivo=True)

    def suspenso(d):
        return next((desc for a, b, desc in susp if a <= d < b), None)

    def motivo(d):
        if suspenso(d):
            return f"suspensão ({suspenso(d)})"
        if d in sem_exp:
            return "sem expediente" + (f" ({sem_exp[d]})" if sem_exp[d] else "")
        if d.weekday() >= 5:
            return SEMANA[d.weekday()]
        return ""

    def proximo_util(d):
        for _ in range(4000):
            if not motivo(d):
                return d
            d += UM
        raise ErroEntrada("não há dia útil no intervalo; confira as suspensões informadas")

    mem = Memoria("prazo processual", e.get("descricao"))
    mem.secao("Entradas")
    linhas = [("Prazo", f"{plural(n, 'dia', 'dias')}, contagem em dias {'corridos' if contagem == 'corridos' else 'úteis'}")]
    if tipo == "disponibilizacao_dje":
        publicacao = proximo_util(data_ev + UM)
        comeco = publicacao
        linhas.append(("Disponibilização no diário eletrônico", fds(data_ev)))
        linhas.append(("Data considerada de publicação", fds(publicacao) + ": primeiro dia útil seguinte à disponibilização"))
    else:
        comeco = data_ev
        linhas.append(("Intimação ou ciência", fds(data_ev)))
    linhas.append(("Dias sem expediente informados",
                   "; ".join(fd(d) + (f" ({t})" if t else "") for d, t in sorted(sem_exp.items())) or "nenhum"))
    linhas.append(("Suspensões informadas",
                   "; ".join(f"{fd(a)} a {fd(b - UM)} ({t})" for a, b, t in susp) or "nenhuma"))
    mem.tabela(["Dado", "Valor"], linhas)

    primeiro = proximo_util(comeco + UM)
    contados = [primeiro]
    d = primeiro
    while len(contados) < n:
        d += UM
        if suspenso(d) or (contagem == "uteis" and motivo(d)):
            continue
        contados.append(d)
    vencimento = contados[-1]
    final = proximo_util(vencimento)

    mem.secao("Convenções aplicadas")
    mem.item("O dia do começo não é contado e o do vencimento é (CPP, art. 798, § 1º).")
    mem.item("A contagem começa no primeiro dia útil seguinte ao dia do começo.")
    if contagem == "corridos":
        mem.item("Contagem contínua: sábados, domingos e dias sem expediente entram na conta, "
                 "mas o prazo que termina em um deles passa ao dia útil imediato (CPP, art. 798, caput e § 3º).")
    else:
        mem.item("Contagem em dias úteis: só entram na conta os dias com expediente.")
    if susp:
        mem.item("Durante a suspensão o prazo não corre; a contagem retoma no dia seguinte ao último dia suspenso.")

    mem.secao("Contagem")
    mem.item(f"Dia do começo, não contado: {fds(comeco)}.")
    mostrar = list(enumerate(contados, 1))
    if n > 45:
        mostrar = mostrar[:3] + [(None, None)] + mostrar[-3:]
    tab = []
    for i, dia in mostrar:
        if i is None:
            tab.append(("...", "...", "..."))
            continue
        obs = motivo(dia)
        tab.append((i, fds(dia), f"{obs}: contado" if obs else ""))
    mem.linha()
    mem.tabela(["Dia do prazo", "Data", "Observação"], tab)
    if final != vencimento:
        mem.linha()
        mem.item(f"O {n}º dia cai em {fds(vencimento)}, {motivo(vencimento)}. O prazo passa ao dia útil imediato.")

    mem.secao("Resultado")
    mem.linha(f"**Último dia do prazo: {fds(final)}.**")
    mem.aviso("Dia sem expediente ou suspensão não informado só antecipa o resultado, nunca o adia. "
              "Inclua apenas datas comprovadas por lei ou por ato do tribunal.")
    mem.aviso("A data da intimação, a quantidade de dias e a forma de contagem são entradas. "
              "Prazo em dobro ou prerrogativa só entra se o número de dias já vier ajustado.")
    if contagem == "uteis":
        mem.aviso("Contagem em dias úteis depende de norma que a determine no caso. "
                  "Em matéria penal, a regra do art. 798 do CPP é a contagem contínua.")
    mem.dados = {"dia_do_comeco": comeco.isoformat(), "primeiro_dia_contado": primeiro.isoformat(),
                 "vencimento_sem_prorrogacao": vencimento.isoformat(), "ultimo_dia": final.isoformat()}
    return mem


# --------------------------------------------------------------------------
# prescricao: linha do tempo da prescrição
# --------------------------------------------------------------------------

def limite_prescricao(inicio, meses, dias, paradas):
    """Último dia do prazo contado pelo calendário, com o saldo retomado após cada suspensão."""
    aplicadas = []
    for a, b, desc in paradas:
        if b is not None and b <= inicio:
            continue
        limite = soma_meses(inicio, meses) + timedelta(days=dias) - UM
        a_ef = max(a, inicio)
        if a_ef > limite:
            continue
        y, m, d = dif_calendario(inicio, a_ef)
        meses2, dias2 = meses - (12 * y + m), dias - d
        if dias2 < 0:
            meses2, dias2 = meses2 - 1, dias2 + 30
        if meses2 < 0 or (meses2 == 0 and dias2 < 1):
            meses2, dias2 = 0, 1
        if b is None:
            return None, aplicadas, {"desde": a_ef, "saldo": (meses2 // 12, meses2 % 12, dias2), "descricao": desc}
        aplicadas.append((a_ef, b, (b - a_ef).days, desc))
        inicio, meses, dias = b, meses2, dias2
    return soma_meses(inicio, meses) + timedelta(days=dias) - UM, aplicadas, None


def cmd_prescricao(e, hoje):
    conferir_campos(e, {"descricao", "prazo", "multiplicadores", "termo_inicial", "marcos",
                        "suspensoes", "data_corte"}, "entrada")
    prazo = ler_duracao(exigir(e, "prazo", "entrada"), "prazo")
    total = Fraction(prazo[0] * 12 + prazo[1]) + Fraction(prazo[2], 30)
    mults = []
    for i, mu in enumerate(e.get("multiplicadores") or [], 1):
        ctx = f"multiplicadores[{i}]"
        conferir_campos(mu, {"fator", "motivo"}, ctx)
        f = ler_fracao(exigir(mu, "fator", ctx), f"{ctx}.fator")
        mults.append((f, str(exigir(mu, "motivo", ctx)).strip()))
        total *= f
    meses = total.numerator // total.denominator
    dias_exatos = (total - meses) * 30
    dias = math.floor(dias_exatos)
    if meses == 0 and dias == 0:
        raise ErroEntrada("prazo: o prazo resultante é zero")

    ti = exigir(e, "termo_inicial", "entrada")
    conferir_campos(ti, {"data", "descricao"}, "termo_inicial")
    pontos = [(ler_data(exigir(ti, "data", "termo_inicial"), "termo_inicial.data"),
               str(exigir(ti, "descricao", "termo_inicial")).strip())]
    for i, mc in enumerate(e.get("marcos") or [], 1):
        ctx = f"marcos[{i}]"
        conferir_campos(mc, {"data", "descricao"}, ctx)
        pontos.append((ler_data(exigir(mc, "data", ctx), f"{ctx}.data"), str(exigir(mc, "descricao", ctx)).strip()))
    marcos = sorted(pontos[1:], key=lambda p: p[0])
    for (d1, t1), (d2, t2) in zip([pontos[0]] + marcos, marcos):
        if d2 <= d1:
            raise ErroEntrada(f"marcos: '{t2}' ({fd(d2)}) não é posterior a '{t1}' ({fd(d1)})")
    pontos = [pontos[0]] + marcos
    paradas = ler_periodos(e.get("suspensoes"), "suspensoes", "inicio", "retomada", aberto=True, fim_inclusivo=False)

    mem = Memoria("prescrição", e.get("descricao"))
    corte = data_de_corte(e, hoje, mem)
    if corte < pontos[-1][0]:
        raise ErroEntrada(f"data_corte: {fd(corte)} é anterior ao último marco, {fd(pontos[-1][0])}")

    prazo_final = (meses // 12, meses % 12, dias)
    mem.secao("Entradas")
    linhas = [("Prazo informado", fdur(prazo))]
    for f, motivo in mults:
        linhas.append(("Multiplicador", f"× {ffrac(f)}: {motivo}"))
    if mults:
        linhas.append(("Prazo aplicado", fdur(prazo_final)))
    linhas.append(("Termo inicial", f"{fd(pontos[0][0])}: {pontos[0][1]}"))
    for i, (d, t) in enumerate(pontos[1:], 1):
        linhas.append((f"Marco interruptivo {i}", f"{fd(d)}: {t}"))
    for a, b, t in paradas:
        linhas.append(("Suspensão", f"de {fd(a)} até {'data em aberto' if b is None else 'a véspera de ' + fd(b)}: {t}"))
    linhas.append(("Data de corte", fd(corte)))
    mem.tabela(["Dado", "Valor"], linhas)
    if dias_exatos != dias:
        mem.aviso(f"O prazo aplicado gerou fração de dia ({fnum(dias_exatos)} dias), que foi desprezada.")

    mem.secao("Convenções aplicadas")
    mem.item("O dia do começo entra na contagem, e anos e meses seguem o calendário (Código Penal, art. 10).")
    mem.item("A cada marco interruptivo, o prazo inteiro recomeça no dia do marco.")
    mem.item("Marco ocorrido até o último dia do prazo, inclusive, é tratado como ocorrido dentro do prazo.")
    if paradas:
        mem.item("Na suspensão, o prazo não corre do dia de início até a véspera da retomada. "
                 "O saldo, em anos, meses e dias, volta a correr no dia da retomada.")

    mem.secao("Intervalos")
    tab, notas, esgotados, resumo = [], [], [], []
    for i, (ini, desc) in enumerate(pontos):
        fechado = i + 1 < len(pontos)
        fim = pontos[i + 1][0] if fechado else corte
        limite, aplicadas, aberta = limite_prescricao(ini, meses, dias, paradas)
        bruto = (fim - ini).days
        parados = dias_parados(paradas, ini, fim)
        decorrido = fdur(dif_calendario(ini, ini + timedelta(days=bruto - parados)))
        if parados:
            decorrido += f", já descontados {plural(parados, 'dia suspenso', 'dias suspensos')}"
        if aberta:
            situacao = (f"Suspenso desde {fd(aberta['desde'])}; saldo de {fdur(aberta['saldo'])} "
                        "a correr quando retomar")
            ultimo = "sem data: suspenso"
        elif fechado:
            ultimo = fd(limite)
            if fim <= limite:
                situacao = "Prazo não esgotado: o marco seguinte ocorreu dentro dele"
            else:
                situacao = f"**Prazo esgotado** em {fd(limite)}, antes do marco seguinte"
                esgotados.append(i + 1)
        else:
            ultimo = fd(limite)
            if corte > limite:
                situacao = f"**Prazo esgotado** em {fd(limite)}, sem novo marco informado"
                esgotados.append(i + 1)
            else:
                situacao = f"Em curso: faltam {plural((limite - corte).days, 'dia', 'dias')} após a data de corte"
        fim_txt = f"{fd(fim)}: {pontos[i + 1][1]}" if fechado else f"{fd(fim)}: data de corte"
        tab.append((i + 1, f"{fd(ini)}: {desc}", fim_txt, decorrido, ultimo, situacao))
        resumo.append({"intervalo": i + 1, "inicio": ini.isoformat(), "fim": fim.isoformat(),
                       "ultimo_dia_do_prazo": limite.isoformat() if limite else None,
                       "esgotado": (i + 1) in esgotados, "suspenso_em_aberto": bool(aberta)})
        if aplicadas and limite:
            base = soma_meses(ini, meses) + timedelta(days=dias) - UM
            alt, _, _ = desloca_por_paradas(ini, base, paradas)
            txt = "; ".join(f"{fd(a)} até a véspera de {fd(b)}, {plural(n, 'dia', 'dias')} ({t})" for a, b, n, t in aplicadas)
            notas.append(f"Intervalo {i + 1}: suspensão considerada: {txt}.")
            if alt and alt != limite:
                notas.append(f"Intervalo {i + 1}: somando os dias suspensos ao prazo original, o último dia seria "
                             f"{fd(alt)}, e não {fd(limite)}. A diferença vem da forma de contar a suspensão. "
                             "Se algum marco cair entre as duas datas, confira à mão e exponha os dois critérios.")
    mem.tabela(["Nº", "Início", "Fim do intervalo", "Tempo decorrido", "Último dia do prazo", "Situação"], tab)
    if notas:
        mem.linha()
        for nota in notas:
            mem.item(nota)

    mem.secao("Resultado")
    if esgotados:
        if len(esgotados) == 1:
            onde = f"no intervalo {esgotados[0]}"
        else:
            onde = "nos intervalos " + ", ".join(str(x) for x in esgotados[:-1]) + f" e {esgotados[-1]}"
        mem.linha(f"**Com as entradas informadas, o prazo se esgotou {onde}.**")
    else:
        mem.linha("**Com as entradas informadas, o prazo não se esgotou em nenhum intervalo.**")
    mem.aviso("O script não escolhe o prazo, o termo inicial, os marcos nem a redação da lei. "
              "Prazo esgotado é resultado aritmético: o reconhecimento da prescrição depende da "
              "conferência de cada entrada e da regra aplicável à data do fato.")
    mem.aviso("Cada crime tem a própria conta. Para comparar pena em abstrato e pena em concreto, "
              "execute um cenário para cada prazo.")
    mem.dados = {"prazo_aplicado": {"anos": prazo_final[0], "meses": prazo_final[1], "dias": prazo_final[2]},
                 "intervalos": resumo, "intervalos_esgotados": esgotados}
    return mem


# --------------------------------------------------------------------------
# pena: aritmética da pena
# --------------------------------------------------------------------------

def cmd_pena(e, hoje):
    conferir_campos(e, {"descricao", "cenarios", "limiares"}, "entrada")
    cenarios = exigir(e, "cenarios", "entrada")
    if not isinstance(cenarios, list):
        raise ErroEntrada("cenarios: esperado uma lista")
    limiares = [ler_duracao(x, f"limiares[{i}]") for i, x in enumerate(e.get("limiares") or [], 1)]
    conv = lambda dur: dur_dias(dur, 360, 30)

    mem = Memoria("pena", e.get("descricao"))
    mem.secao("Convenções aplicadas")
    mem.item("Pena convertida em dias com ano de 12 meses e mês de 30 dias, apenas para aplicar frações.")
    mem.item("Fração de dia desprezada a cada operação (Código Penal, art. 11).")
    mem.item("Aumento multiplica a pena por 1 + fração; diminuição, por 1 − fração. "
             "As operações são aplicadas na ordem informada.")

    finais = []
    for i, c in enumerate(cenarios, 1):
        ctx = f"cenarios[{i}]"
        conferir_campos(c, {"nome", "pena_inicial", "dias_multa_inicial", "operacoes"}, ctx)
        nome = str(exigir(c, "nome", ctx)).strip()
        dias = conv(ler_duracao(exigir(c, "pena_inicial", ctx), f"{ctx}.pena_inicial"))
        multa = c.get("dias_multa_inicial")
        if multa is not None:
            multa = ler_inteiro(multa, f"{ctx}.dias_multa_inicial")
        tab = [("Ponto de partida", "", fdur(dias_dur(dias)), "" if multa is None else multa)]
        desprezou = False
        for j, op in enumerate(c.get("operacoes") or [], 1):
            octx = f"{ctx}.operacoes[{j}]"
            conferir_campos(op, {"tipo", "fracao", "pena", "dias_multa", "aplica_multa", "descricao"}, octx)
            tipo = exigir(op, "tipo", octx)
            desc = str(exigir(op, "descricao", octx)).strip()
            if tipo in ("aumento", "diminuicao"):
                f = ler_fracao(exigir(op, "fracao", octx), f"{octx}.fracao")
                if tipo == "diminuicao" and f >= 1:
                    raise ErroEntrada(f"{octx}: diminuição de {ffrac(f)} zera ou inverte a pena")
                fator = 1 + f if tipo == "aumento" else 1 - f
                exato = Fraction(dias) * fator
                desprezou = desprezou or exato.denominator != 1
                dias = math.floor(exato)
                if multa is not None and op.get("aplica_multa", True):
                    multa = math.floor(Fraction(multa) * fator)
                oper = f"{'aumento' if tipo == 'aumento' else 'diminuição'} de {ffrac(f)}"
            elif tipo in ("soma", "subtracao", "fixar"):
                p = ler_duracao(exigir(op, "pena", octx), f"{octx}.pena")
                dm = op.get("dias_multa")
                if dm is not None:
                    dm = ler_inteiro(dm, f"{octx}.dias_multa")
                if tipo == "soma":
                    dias += conv(p)
                    oper = f"soma de {fdur(p)}"
                    if dm is not None:
                        multa = (multa or 0) + dm
                elif tipo == "subtracao":
                    dias -= conv(p)
                    oper = f"subtração de {fdur(p)}"
                    if dias < 0:
                        raise ErroEntrada(f"{octx}: a subtração deixa a pena negativa")
                    if dm is not None:
                        multa = max((multa or 0) - dm, 0)
                else:
                    dias = conv(p)
                    oper = f"pena fixada em {fdur(p)}"
                    if dm is not None:
                        multa = dm
            else:
                raise ErroEntrada(f"{octx}.tipo: use aumento, diminuicao, soma, subtracao ou fixar")
            tab.append((desc, oper, fdur(dias_dur(dias)), "" if multa is None else multa))
        mem.secao(f"Cenário {i}: {nome}")
        mem.tabela(["Etapa", "Operação", "Pena resultante", "Dias-multa"], tab)
        mem.linha()
        mem.linha(f"**Pena final: {fdur(dias_dur(dias))}**" + ("" if multa is None else f" e {plural(multa, 'dia-multa', 'dias-multa')}") + ".")
        if desprezou:
            mem.linha("Houve fração de dia desprezada em pelo menos uma operação.")
        finais.append((nome, dias, multa))

    def relacao(dias, ref):
        if dias == ref:
            return "igual"
        return f"{'acima' if dias > ref else 'abaixo'}, diferença de {fdur(dias_dur(abs(dias - ref)))}"

    if limiares:
        mem.secao("Comparação com os limiares informados")
        mem.tabela(["Cenário", "Pena final"] + [fdur(l) for l in limiares],
                   [(nome, fdur(dias_dur(d))) + tuple(relacao(d, conv(l)) for l in limiares) for nome, d, _ in finais])
    if len(finais) > 1:
        mem.secao("Diferença entre cenários")
        base_nome, base_dias, _ = finais[0]
        mem.tabela(["Cenário", "Pena final", f"Em relação a '{base_nome}'"],
                   [(nome, fdur(dias_dur(d)), "referência" if k == 0 else relacao(d, base_dias))
                    for k, (nome, d, _) in enumerate(finais)])
    mem.aviso("O script não escolhe fração, ordem das fases nem limite legal. Recondução ao mínimo "
              "ou ao máximo entra como operação 'fixar', com o fundamento na descrição.")
    mem.aviso("A comparação com limiares é só numérica. Regime, substituição e suspensão da pena "
              "dependem do texto da lei (superior a, não superior a, igual ou inferior a) e dos demais requisitos.")
    mem.dados = {"cenarios": [{"nome": n, "pena_final_dias_convencionais": d,
                               "pena_final": dict(zip(("anos", "meses", "dias"), dias_dur(d))),
                               "dias_multa": m} for n, d, m in finais]}
    return mem


# --------------------------------------------------------------------------
# execucao: requisito temporal de benefício e término de pena
# --------------------------------------------------------------------------

def cmd_execucao(e, hoje):
    conferir_campos(e, {"descricao", "data_base", "parcelas", "creditos", "interrupcoes", "conversao",
                        "arredondamento", "termino", "data_corte"}, "entrada")
    db = exigir(e, "data_base", "entrada")
    conferir_campos(db, {"data", "descricao"}, "data_base")
    base = ler_data(exigir(db, "data", "data_base"), "data_base.data")
    conv = e.get("conversao") or {}
    conferir_campos(conv, {"ano", "mes"}, "conversao")
    ano = ler_inteiro(conv.get("ano", 365), "conversao.ano", minimo=360)
    mes = ler_inteiro(conv.get("mes", 30), "conversao.mes", minimo=28)
    arred = e.get("arredondamento", "desprezar")
    if arred not in ("desprezar", "cima"):
        raise ErroEntrada("arredondamento: use 'desprezar' ou 'cima'")
    parcelas = exigir(e, "parcelas", "entrada")
    if not isinstance(parcelas, list):
        raise ErroEntrada("parcelas: esperado uma lista")

    mem = Memoria("requisito temporal na execução", e.get("descricao"))
    corte = data_de_corte(e, hoje, mem)
    paradas = ler_periodos(e.get("interrupcoes"), "interrupcoes", "inicio", "retomada", aberto=True, fim_inclusivo=False)

    tab_p, exato = [], Fraction(0)
    for i, p in enumerate(parcelas, 1):
        ctx = f"parcelas[{i}]"
        conferir_campos(p, {"descricao", "pena", "fracao"}, ctx)
        pena = ler_duracao(exigir(p, "pena", ctx), f"{ctx}.pena")
        f = ler_fracao(exigir(p, "fracao", ctx), f"{ctx}.fracao")
        if f > 1:
            raise ErroEntrada(f"{ctx}.fracao: fração acima de 1 não é requisito de cumprimento")
        pd = dur_dias(pena, ano, mes)
        exato += pd * f
        tab_p.append((str(exigir(p, "descricao", ctx)).strip(), fdur(pena), pd, ffrac(f), fnum(pd * f)))
    requisito = math.floor(exato) if arred == "desprezar" else math.ceil(exato)

    tab_c, creditos = [], 0
    for i, c in enumerate(e.get("creditos") or [], 1):
        ctx = f"creditos[{i}]"
        conferir_campos(c, {"descricao", "dias"}, ctx)
        n = ler_inteiro(exigir(c, "dias", ctx), f"{ctx}.dias")
        creditos += n
        tab_c.append((str(exigir(c, "descricao", ctx)).strip(), n))

    mem.secao("Entradas")
    linhas = [("Data-base", f"{fd(base)}: {str(exigir(db, 'descricao', 'data_base')).strip()}"),
              ("Conversão da pena em dias", f"ano de {ano} dias e mês de {mes} dias"),
              ("Fração de dia no requisito", "desprezada" if arred == "desprezar" else "arredondada para cima"),
              ("Data de corte", fd(corte))]
    for a, b, t in paradas:
        linhas.append(("Interrupção", f"de {fd(a)} até {'data em aberto' if b is None else 'a véspera de ' + fd(b)}: {t}"))
    mem.tabela(["Dado", "Valor"], linhas)

    mem.secao("Requisito por condenação")
    mem.tabela(["Condenação", "Pena considerada", "Pena em dias", "Fração", "Requisito em dias"],
               tab_p + [("Total", "", "", "", f"{fnum(exato)}, considerado {requisito}" if exato.denominator != 1 else str(requisito))])
    if exato.denominator != 1:
        outro = math.ceil(exato) if arred == "desprezar" else math.floor(exato)
        mem.linha()
        mem.linha(f"O total tem fração de dia. Pelo outro critério de arredondamento, o requisito seria de {outro} dias.")

    if tab_c:
        mem.secao("Créditos computados como pena cumprida")
        mem.tabela(["Crédito", "Dias"], tab_c + [("Total", creditos)])

    a_cumprir = requisito - creditos
    mem.secao("Conta")
    mem.item(f"Requisito: {plural(requisito, 'dia', 'dias')}.")
    mem.item(f"Créditos: {plural(creditos, 'dia', 'dias')}.")
    dados = {"requisito_dias": requisito, "creditos_dias": creditos}
    if a_cumprir <= 0:
        mem.item(f"Os créditos cobrem o requisito, com sobra de {plural(-a_cumprir, 'dia', 'dias')}.")
        mem.secao("Resultado")
        mem.linha(f"**Requisito temporal coberto na própria data-base, {fd(base)}.**")
        dados.update({"ultimo_dia_do_periodo": base.isoformat(), "dia_seguinte": base.isoformat()})
    else:
        mem.item(f"A cumprir a partir da data-base: {plural(a_cumprir, 'dia', 'dias')}, contado o próprio dia da data-base.")
        ultimo0 = base + timedelta(days=a_cumprir - 1)
        ultimo, aplicadas, aberta = desloca_por_paradas(base, ultimo0, paradas)
        for a, b, n, t in aplicadas:
            mem.item(f"Interrupção de {fd(a)} até a véspera de {fd(b)}: {plural(n, 'dia', 'dias')} não computados ({t}).")
        mem.secao("Resultado")
        if aberta:
            mem.linha(f"**Sem data projetada: contagem interrompida desde {fd(aberta['desde'])} "
                      f"({aberta['descricao']}), restando {plural(aberta['restam'], 'dia', 'dias')}.**")
            dados.update({"ultimo_dia_do_periodo": None, "dia_seguinte": None})
        else:
            mem.linha(f"**Último dia do período exigido: {fd(ultimo)}. Dia seguinte: {fd(ultimo + UM)}.**")
            mem.linha()
            mem.linha("Se a lei exige ter cumprido ao menos a fração, o requisito se completa ao fim do último dia. "
                      "Se exige mais do que a fração, só no dia seguinte.")
            dados.update({"ultimo_dia_do_periodo": ultimo.isoformat(), "dia_seguinte": (ultimo + UM).isoformat()})

        mem.secao("Situação na data de corte")
        cumpridos = 0
        if corte >= base:
            cumpridos = (corte - base).days + 1 - dias_parados(paradas, base, corte + UM)
        soma = cumpridos + creditos
        mem.item(f"Dias cumpridos da data-base até {fd(corte)}, inclusive, descontadas as interrupções: {cumpridos}.")
        mem.item(f"Com os créditos: {soma} de {requisito} dias ({fnum(Fraction(soma * 100, requisito))}%).")
        mem.item(f"Faltam {plural(requisito - soma, 'dia', 'dias')}." if soma < requisito
                 else f"Requisito superado em {plural(soma - requisito, 'dia', 'dias')}.")
        dados["cumprido_na_data_de_corte_dias"] = soma

    term = e.get("termino")
    if term:
        conferir_campos(term, {"pena", "descricao"}, "termino")
        pt = ler_duracao(exigir(term, "pena", "termino"), "termino.pena")
        ptd = dur_dias(pt, ano, mes)
        restam = ptd - creditos
        mem.secao("Término da pena")
        mem.item(f"Pena considerada: {fdur(pt)}, ou {ptd} dias ({str(exigir(term, 'descricao', 'termino')).strip()}).")
        mem.item(f"Menos os créditos: {plural(max(restam, 0), 'dia', 'dias')} a cumprir a partir da data-base.")
        if restam <= 0:
            mem.linha()
            mem.linha(f"**Os créditos cobrem toda a pena considerada na data-base, {fd(base)}.**")
            dados["termino"] = base.isoformat()
        else:
            fim, _, aberta_t = desloca_por_paradas(base, base + timedelta(days=restam - 1), paradas)
            mem.linha()
            if aberta_t:
                mem.linha(f"**Sem data projetada: contagem interrompida desde {fd(aberta_t['desde'])}.**")
                dados["termino"] = None
            else:
                mem.linha(f"**Último dia de pena: {fd(fim)}.**")
                dados["termino"] = fim.isoformat()
        mem.aviso("No término, informe a pena ainda não descontada dos créditos listados, para não abatê-los duas vezes.")

    mem.aviso("O script não escolhe a fração, a data-base nem a lei aplicável a cada condenação, "
              "e não examina requisito subjetivo, vedação ou falta grave.")
    mem.aviso(f"Convenção de conversão: ano de {ano} dias e mês de {mes} dias. O cálculo do juízo pode usar "
              "outra, e diferença de poucos dias costuma vir daí. Compare com o cálculo oficial e localize a diferença.")
    mem.aviso("Resultado é projeção aritmética, não data adquirida nem cálculo homologado.")
    mem.dados = dados
    return mem


# --------------------------------------------------------------------------
# remicao: dias remidos
# --------------------------------------------------------------------------

def cmd_remicao(e, hoje):
    conferir_campos(e, {"descricao", "trabalho", "estudo", "outros", "perda"}, "entrada")
    mem = Memoria("remição", e.get("descricao"))
    tab, total = [], 0
    trab = e.get("trabalho")
    if trab:
        conferir_campos(trab, {"dias", "dias_por_dia_remido"}, "trabalho")
        n = ler_inteiro(exigir(trab, "dias", "trabalho"), "trabalho.dias")
        r = ler_inteiro(exigir(trab, "dias_por_dia_remido", "trabalho"), "trabalho.dias_por_dia_remido", minimo=1)
        q, sobra = divmod(n, r)
        total += q
        tab.append(("Trabalho", f"{n} dias ÷ {r}", q, f"sobram {plural(sobra, 'dia', 'dias')} de trabalho sem aproveitamento" if sobra else ""))
    est = e.get("estudo")
    if est:
        conferir_campos(est, {"horas", "horas_por_dia_remido", "acrescimo"}, "estudo")
        h = ler_inteiro(exigir(est, "horas", "estudo"), "estudo.horas")
        r = ler_inteiro(exigir(est, "horas_por_dia_remido", "estudo"), "estudo.horas_por_dia_remido", minimo=1)
        q, sobra = divmod(h, r)
        total += q
        tab.append(("Estudo", f"{h} horas ÷ {r}", q, f"sobram {plural(sobra, 'hora', 'horas')} sem aproveitamento" if sobra else ""))
        if est.get("acrescimo"):
            f = ler_fracao(est["acrescimo"], "estudo.acrescimo")
            ex = q * f
            extra = math.floor(ex)
            total += extra
            tab.append(("Acréscimo sobre o estudo", f"{q} × {ffrac(f)}", extra,
                        f"valor exato {fnum(ex)}; fração desprezada" if ex.denominator != 1 else ""))
    for i, o in enumerate(e.get("outros") or [], 1):
        ctx = f"outros[{i}]"
        conferir_campos(o, {"descricao", "dias"}, ctx)
        n = ler_inteiro(exigir(o, "dias", ctx), f"{ctx}.dias")
        total += n
        tab.append((str(exigir(o, "descricao", ctx)).strip(), "dias informados", n, ""))
    if not tab:
        raise ErroEntrada("entrada: informe ao menos 'trabalho', 'estudo' ou 'outros'")
    mem.secao("Conta")
    mem.tabela(["Origem", "Operação", "Dias remidos", "Observação"], tab + [("Total", "", total, "")])
    restante = total
    perda = e.get("perda")
    if perda:
        conferir_campos(perda, {"fracao", "descricao"}, "perda")
        f = ler_fracao(exigir(perda, "fracao", "perda"), "perda.fracao")
        if f > 1:
            raise ErroEntrada("perda.fracao: a perda não pode superar o total")
        ex = total * f
        perdidos = math.floor(ex)
        restante = total - perdidos
        mem.secao("Perda de dias remidos")
        mem.item(f"Fração informada: {ffrac(f)} ({str(exigir(perda, 'descricao', 'perda')).strip()}).")
        mem.item(f"{total} × {ffrac(f)} = {fnum(ex)}; perda de {plural(perdidos, 'dia', 'dias')}, desprezada a fração.")
    mem.secao("Resultado")
    mem.linha(f"**Dias remidos: {restante}.**")
    mem.aviso("As razões de conversão, o acréscimo e a fração de perda são entradas. "
              "Dias e horas precisam de atestado, e a remição depende de declaração do juízo.")
    if perda:
        mem.aviso("A fração de perda foi aplicada sobre todo o total informado. Se a perda atinge só "
                  "parte dos dias, calcule essa parte em separado.")
    mem.dados = {"dias_remidos_antes_da_perda": total, "dias_remidos": restante}
    return mem


# --------------------------------------------------------------------------
# periodos: tempo entre datas
# --------------------------------------------------------------------------

def cmd_periodos(e, hoje):
    conferir_campos(e, {"descricao", "periodos", "incluir_dia_final", "data_corte"}, "entrada")
    incluir = e.get("incluir_dia_final", True)
    if not isinstance(incluir, bool):
        raise ErroEntrada("incluir_dia_final: use true ou false")
    bruto = exigir(e, "periodos", "entrada")
    mem = Memoria("períodos", e.get("descricao"))
    aberto = isinstance(bruto, list) and any(isinstance(p, dict) and not p.get("fim") for p in bruto)
    corte = data_de_corte(e, hoje, mem) if aberto else None
    lidos = ler_periodos(bruto, "periodos", "inicio", "fim", aberto=True, fim_inclusivo=incluir, sobrepor=True)
    extra = UM if incluir else timedelta(0)
    per = []
    for a, b, t in lidos:
        em_curso = b is None
        if em_curso:
            if corte < a:
                raise ErroEntrada(f"periodos: '{t}' começa depois da data de corte")
            b = corte + extra
        per.append((a, b, t, em_curso))

    mem.secao("Convenções aplicadas")
    mem.item("O dia inicial é contado. O dia final " + ("também é contado." if incluir else "não é contado."))
    mem.item("Anos e meses seguem o calendário; a coluna de dias é a contagem exata.")
    mem.secao("Períodos")
    tab, soma = [], 0
    for a, b, t, em_curso in per:
        n = (b - a).days
        soma += n
        fim_txt = fd(b - extra) + (" (data de corte, período em curso)" if em_curso else "")
        tab.append((t, fd(a), fim_txt, n, fdur(dif_calendario(a, b))))
    mem.tabela(["Período", "Início", "Fim", "Dias", "Pelo calendário"], tab + [("Soma", "", "", soma, "")])

    uniao, cursor, pares = 0, None, []
    for k, (a, b, t, _) in enumerate(per):
        for a2, b2, t2, _ in per[k + 1:]:
            if a2 < b and a < b2:
                pares.append((t, t2, (min(b, b2) - max(a, a2)).days))
        ini = a if cursor is None or a > cursor else cursor
        if b > ini:
            uniao += (b - ini).days
            cursor = b
    mem.secao("Resultado")
    if pares:
        mem.linha(f"**Total sem contar dias repetidos: {plural(uniao, 'dia', 'dias')}.** A soma simples dá {soma}.")
        for t1, t2, n in pares:
            mem.aviso(f"Sobreposição de {plural(n, 'dia', 'dias')} entre '{t1}' e '{t2}'. "
                      "O mesmo dia não se computa duas vezes.")
    else:
        mem.linha(f"**Total: {plural(soma, 'dia', 'dias')}.**")
    mem.aviso("As datas de início e fim são entradas e precisam de documento: mandado cumprido, "
              "alvará, certidão ou atestado. O script não decide em qual processo o período se computa.")
    mem.dados = {"soma_dias": soma, "dias_sem_repeticao": uniao, "sobreposicoes": len(pares)}
    return mem


# --------------------------------------------------------------------------
# Modelos de entrada (fictícios)
# --------------------------------------------------------------------------

MODELOS = {
    "prazo": {
        "descricao": "Apelação: interposição (exemplo fictício)",
        "evento": {"tipo": "intimacao", "data": "2026-11-06"},
        "dias": 5,
        "contagem": "corridos",
        "dias_sem_expediente": [{"data": "2026-11-20", "descricao": "feriado informado pelo tribunal"}],
        "suspensoes": [{"primeiro_dia": "2026-12-20", "ultimo_dia": "2027-01-20", "descricao": "CPP, art. 798-A"}],
    },
    "prescricao": {
        "descricao": "Pena em concreto de 1 ano, réu menor de 21 anos na data do fato (exemplo fictício)",
        "prazo": "4a",
        "multiplicadores": [{"fator": "1/2", "motivo": "redução do art. 115 do Código Penal, conferida"}],
        "termo_inicial": {"data": "2019-03-10", "descricao": "recebimento da denúncia"},
        "marcos": [{"data": "2022-06-20", "descricao": "publicação da sentença condenatória"}],
        "suspensoes": [{"inicio": "2020-02-03", "retomada": "2020-09-03", "descricao": "CPP, art. 366"}],
        "data_corte": "2026-11-11",
    },
    "pena": {
        "descricao": "Dosimetria da sentença e cenário defensivo (exemplo fictício)",
        "cenarios": [
            {"nome": "Sentença", "pena_inicial": "4a", "dias_multa_inicial": 10, "operacoes": [
                {"tipo": "aumento", "fracao": "1/6", "descricao": "1ª fase: uma vetorial negativa"},
                {"tipo": "aumento", "fracao": "1/3", "descricao": "3ª fase: majorante"}]},
            {"nome": "Tese: afastar a vetorial", "pena_inicial": "4a", "dias_multa_inicial": 10, "operacoes": [
                {"tipo": "aumento", "fracao": "1/3", "descricao": "3ª fase: majorante"}]},
        ],
        "limiares": ["4a", "8a"],
    },
    "execucao": {
        "descricao": "Requisito temporal para progressão (exemplo fictício)",
        "data_base": {"data": "2023-05-10", "descricao": "início da prisão atual"},
        "parcelas": [
            {"descricao": "Condenação A", "pena": "6a8m", "fracao": "25%"},
            {"descricao": "Condenação B", "pena": "2a", "fracao": "1/6"},
        ],
        "creditos": [
            {"descricao": "Remição declarada", "dias": 60},
            {"descricao": "Detração: prisão provisória anterior", "dias": 89},
        ],
        "interrupcoes": [],
        "conversao": {"ano": 365, "mes": 30},
        "arredondamento": "desprezar",
        "termino": {"pena": "8a8m", "descricao": "soma das penas"},
        "data_corte": "2026-11-11",
    },
    "remicao": {
        "descricao": "Remição por trabalho e estudo (exemplo fictício)",
        "trabalho": {"dias": 200, "dias_por_dia_remido": 3},
        "estudo": {"horas": 480, "horas_por_dia_remido": 12, "acrescimo": "1/3"},
        "outros": [{"descricao": "Leitura, conforme ato do juízo", "dias": 8}],
        "perda": {"fracao": "1/3", "descricao": "fração fixada na decisão sobre a falta"},
    },
    "periodos": {
        "descricao": "Prisão provisória para detração (exemplo fictício)",
        "periodos": [
            {"inicio": "2022-02-01", "fim": "2022-04-30", "descricao": "preventiva no processo A"},
            {"inicio": "2023-05-10", "fim": None, "descricao": "prisão atual"},
        ],
        "incluir_dia_final": True,
        "data_corte": "2026-11-11",
    },
}

EXECUTORES = {"prazo": cmd_prazo, "prescricao": cmd_prescricao, "pena": cmd_pena,
              "execucao": cmd_execucao, "remicao": cmd_remicao, "periodos": cmd_periodos}


# --------------------------------------------------------------------------
# Autoteste
# --------------------------------------------------------------------------

def autoteste():
    hoje = date(2026, 11, 11)
    feitos = []

    def confere(nome, obtido, esperado):
        if obtido != esperado:
            raise AssertionError(f"{nome}: obtido {obtido!r}, esperado {esperado!r}")
        feitos.append(nome)

    def falha(nome, comando, entrada):
        try:
            EXECUTORES[comando](entrada, hoje)
        except ErroEntrada:
            feitos.append(nome)
            return
        raise AssertionError(f"{nome}: a entrada inválida foi aceita")

    confere("soma de meses em fim de mês", soma_meses(date(2024, 1, 31), 1), date(2024, 2, 29))
    confere("diferença pelo calendário", dif_calendario(date(2020, 1, 15), date(2023, 3, 20)), (3, 2, 5))
    confere("duração compacta", ler_duracao("5a4m10d", "t"), (5, 4, 10))
    confere("duração por extenso", ler_duracao("5 anos e 4 meses", "t"), (5, 4, 0))
    confere("fração percentual", ler_fracao("16%", "t"), Fraction(4, 25))

    def prazo(**k):
        base = {"evento": {"tipo": "intimacao", "data": "2026-11-06"}, "dias": 5, "contagem": "corridos"}
        base.update(k)
        return cmd_prazo(base, hoje).dados["ultimo_dia"]

    confere("prazo: intimação na sexta, 5 dias", prazo(), "2026-11-13")
    confere("prazo: fim de semana no meio", prazo(evento={"tipo": "intimacao", "data": "2026-11-04"}), "2026-11-09")
    confere("prazo: vence no sábado, prorroga",
            prazo(evento={"tipo": "intimacao", "data": "2026-11-05"}, dias=2), "2026-11-09")
    confere("prazo: suspensão de fim de ano",
            prazo(evento={"tipo": "intimacao", "data": "2026-12-17"},
                  suspensoes=[{"primeiro_dia": "2026-12-20", "ultimo_dia": "2027-01-20", "descricao": "t"}]),
            "2027-01-25")
    confere("prazo: diário eletrônico",
            prazo(evento={"tipo": "disponibilizacao_dje", "data": "2026-11-06"}), "2026-11-16")
    confere("prazo: dias úteis com feriado",
            prazo(contagem="uteis", dias_sem_expediente=["2026-11-11"]), "2026-11-16")
    confere("prazo: feriado no primeiro dia",
            prazo(dias_sem_expediente=["2026-11-09"]), "2026-11-16")

    def presc(**k):
        base = {"prazo": "4a", "termo_inicial": {"data": "2018-03-10", "descricao": "t"}, "data_corte": "2026-11-11"}
        base.update(k)
        return cmd_prescricao(base, hoje).dados

    confere("prescrição: marco no último dia",
            presc(marcos=[{"data": "2022-03-09", "descricao": "m"}])["intervalos"][0]["esgotado"], False)
    confere("prescrição: marco um dia depois",
            presc(marcos=[{"data": "2022-03-10", "descricao": "m"}], data_corte="2023-01-01")
            ["intervalos_esgotados"], [1])
    confere("prescrição: último dia", presc()["intervalos"][0]["ultimo_dia_do_prazo"], "2022-03-09")
    confere("prescrição: metade",
            presc(multiplicadores=[{"fator": "1/2", "motivo": "t"}])["intervalos"][0]["ultimo_dia_do_prazo"], "2020-03-09")
    confere("prescrição: mais um terço",
            presc(prazo="8a", termo_inicial={"data": "2010-01-01", "descricao": "t"},
                  multiplicadores=[{"fator": "4/3", "motivo": "t"}])["intervalos"][0]["ultimo_dia_do_prazo"], "2020-08-31")
    confere("prescrição: suspensão de um ano",
            presc(suspensoes=[{"inicio": "2019-03-10", "retomada": "2020-03-10", "descricao": "t"}])
            ["intervalos"][0]["ultimo_dia_do_prazo"], "2023-03-09")
    confere("prescrição: suspensão em aberto",
            presc(suspensoes=[{"inicio": "2019-03-10", "retomada": None, "descricao": "t"}])
            ["intervalos"][0]["suspenso_em_aberto"], True)
    confere("prescrição: suspensão posterior ao fim do prazo é ignorada",
            presc(suspensoes=[{"inicio": "2022-03-10", "retomada": "2023-03-10", "descricao": "t"}])
            ["intervalos"][0]["ultimo_dia_do_prazo"], "2022-03-09")

    pena = cmd_pena(MODELOS["pena"], hoje).dados["cenarios"]
    confere("pena: 4a + 1/6 + 1/3", pena[0]["pena_final"], {"anos": 6, "meses": 2, "dias": 20})
    confere("pena: dias-multa", pena[0]["dias_multa"], 14)
    confere("pena: 4a + 1/3", pena[1]["pena_final"], {"anos": 5, "meses": 4, "dias": 0})

    ex = cmd_execucao(MODELOS["execucao"], hoje).dados
    confere("execução: requisito", ex["requisito_dias"], 729)
    confere("execução: último dia", ex["ultimo_dia_do_periodo"], "2024-12-09")
    confere("execução: término", ex["termino"], "2031-08-06")
    ex2 = dict(MODELOS["execucao"], interrupcoes=[{"inicio": "2024-01-05", "retomada": "2024-02-10", "descricao": "t"}])
    confere("execução: interrupção de 36 dias", cmd_execucao(ex2, hoje).dados["ultimo_dia_do_periodo"], "2025-01-14")
    ex3 = dict(MODELOS["execucao"], arredondamento="cima")
    confere("execução: arredondamento para cima", cmd_execucao(ex3, hoje).dados["requisito_dias"], 730)

    confere("remição", cmd_remicao(MODELOS["remicao"], hoje).dados,
            {"dias_remidos_antes_da_perda": 127, "dias_remidos": 85})

    per = cmd_periodos(MODELOS["periodos"], hoje).dados
    confere("períodos: soma", per["soma_dias"], 89 + 1282)
    sobre = {"periodos": [{"inicio": "2022-01-01", "fim": "2022-01-31", "descricao": "a"},
                          {"inicio": "2022-01-20", "fim": "2022-02-10", "descricao": "b"}]}
    confere("períodos: sobreposição", cmd_periodos(sobre, hoje).dados,
            {"soma_dias": 53, "dias_sem_repeticao": 41, "sobreposicoes": 1})

    falha("erro: campo desconhecido", "prazo", {"evento": {"tipo": "intimacao", "data": "2026-11-06"},
                                                "dias": 5, "contagem": "corridos", "feriados": []})
    falha("erro: data inexistente", "prazo", {"evento": {"tipo": "intimacao", "data": "2026-02-30"},
                                              "dias": 5, "contagem": "corridos"})
    falha("erro: contagem ausente", "prazo", {"evento": {"tipo": "intimacao", "data": "2026-11-06"}, "dias": 5})
    falha("erro: marco anterior ao termo inicial", "prescricao",
          {"prazo": "4a", "termo_inicial": {"data": "2018-03-10", "descricao": "t"},
           "marcos": [{"data": "2017-01-01", "descricao": "m"}], "data_corte": "2026-11-11"})
    falha("erro: suspensões sobrepostas", "prescricao",
          {"prazo": "4a", "termo_inicial": {"data": "2018-03-10", "descricao": "t"}, "data_corte": "2026-11-11",
           "suspensoes": [{"inicio": "2019-01-01", "retomada": "2019-06-01", "descricao": "a"},
                          {"inicio": "2019-05-01", "retomada": "2019-07-01", "descricao": "b"}]})
    falha("erro: duração sem unidade", "prescricao",
          {"prazo": "4", "termo_inicial": {"data": "2018-03-10", "descricao": "t"}})

    for nome in COMANDOS:
        texto = EXECUTORES[nome](json.loads(json.dumps(MODELOS[nome])), hoje).markdown()
        if "## " not in texto:
            raise AssertionError(f"modelo {nome}: memória vazia")
        feitos.append(f"modelo {nome}")
    return feitos


# --------------------------------------------------------------------------
# Linha de comando
# --------------------------------------------------------------------------

def main(argv=None):
    for fluxo in (sys.stdout, sys.stderr, sys.stdin):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(prog="calculos.py", description="Cálculos penais com memória conferível.")
    ap.add_argument("comando", choices=COMANDOS + ["modelo", "autoteste"])
    ap.add_argument("alvo", nargs="?", help="com 'modelo': o comando cujo modelo de entrada se quer ver")
    ap.add_argument("--entrada", help="arquivo JSON com a entrada")
    ap.add_argument("--json", dest="inline", help="entrada JSON na própria linha de comando")
    ap.add_argument("--formato", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args(argv)

    if args.comando == "autoteste":
        try:
            feitos = autoteste()
        except AssertionError as erro:
            print(f"FALHA NO AUTOTESTE: {erro}")
            return 1
        print(f"Autoteste: {len(feitos)} verificações, todas corretas.")
        return 0
    if args.comando == "modelo":
        if args.alvo not in COMANDOS:
            print("Informe o comando: " + ", ".join(COMANDOS))
            return 2
        print(json.dumps(MODELOS[args.alvo], ensure_ascii=False, indent=2))
        return 0

    try:
        if args.inline:
            bruto = args.inline
        elif args.entrada:
            with open(args.entrada, encoding="utf-8-sig") as arq:
                bruto = arq.read()
        else:
            bruto = sys.stdin.read()
        try:
            entrada = json.loads(bruto.lstrip("﻿"))
        except json.JSONDecodeError as erro:
            raise ErroEntrada(f"JSON inválido: {erro}") from None
        mem = EXECUTORES[args.comando](entrada, date.today())
    except ErroEntrada as erro:
        print(f"ERRO DE ENTRADA: {erro}", file=sys.stderr)
        print("Nada foi calculado. Corrija a entrada; não complete o dado por suposição.", file=sys.stderr)
        return 2
    except OSError as erro:
        print(f"ERRO DE ARQUIVO: {erro}", file=sys.stderr)
        return 2

    if args.formato == "json":
        print(json.dumps({"comando": args.comando, "resultado": mem.dados, "avisos": mem.avisos,
                          "memoria": mem.markdown()}, ensure_ascii=False, indent=2))
    else:
        print(mem.markdown(), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
