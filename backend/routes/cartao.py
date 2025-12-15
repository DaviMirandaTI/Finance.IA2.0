from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response
from typing import List, Optional
from models.cartao import CartaoCredito, FaturaCartao
from server import db
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import csv
import io

cartao_router = APIRouter(prefix="/api/cartao", tags=["cartao"])


@cartao_router.get("", response_model=List[dict])
async def listar_cartoes():
    """Lista todos os cartões de crédito"""
    cursor = db.cartoes.find({})
    cartoes = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        cartoes.append(doc)
    return cartoes


@cartao_router.post("", response_model=dict)
async def criar_cartao(cartao: CartaoCredito):
    """Cria um novo cartão de crédito"""
    cartao.limite_disponivel = cartao.limite_total - cartao.limite_usado
    doc = cartao.model_dump()
    await db.cartoes.insert_one(doc)
    doc["_id"] = str(doc.get("_id", ""))
    return doc


@cartao_router.put("/{cartao_id}", response_model=dict)
async def atualizar_cartao(cartao_id: str, cartao: CartaoCredito):
    """Atualiza um cartão de crédito"""
    cartao.limite_disponivel = cartao.limite_total - cartao.limite_usado
    doc = cartao.model_dump()
    result = await db.cartoes.update_one({"id": cartao_id}, {"$set": doc})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    doc["_id"] = cartao_id
    return doc


@cartao_router.get("/{cartao_id}/faturas", response_model=List[dict])
async def listar_faturas(cartao_id: str, mes: Optional[str] = None):
    """Lista faturas de um cartão"""
    filtro = {"cartao_id": cartao_id}
    if mes:
        filtro["mes_referencia"] = mes
    
    cursor = db.faturas.find(filtro).sort("mes_referencia", -1)
    faturas = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        faturas.append(doc)
    return faturas


@cartao_router.post("/{cartao_id}/calcular-fatura")
async def calcular_fatura_atual(cartao_id: str, mes: Optional[str] = None):
    """
    Calcula a fatura atual do cartão baseado nos lançamentos do mês.
    Se não passar o mês, usa o mês atual.
    """
    if not mes:
        mes = datetime.now().strftime("%Y-%m")
    
    # Buscar lançamentos do cartão no mês
    cursor = db.lancamentos.find({
        "forma": "credito",
        "data": {"$regex": f"^{mes}"},
        "tipo": "saida",
    })
    
    lancamentos = [doc async for doc in cursor]
    valor_total = sum(float(l.get("valor", 0)) for l in lancamentos)
    lancamentos_ids = [l.get("id") for l in lancamentos]
    
    # Buscar ou criar fatura
    fatura_existente = await db.faturas.find_one({
        "cartao_id": cartao_id,
        "mes_referencia": mes,
    })
    
    if fatura_existente:
        await db.faturas.update_one(
            {"_id": fatura_existente["_id"]},
            {"$set": {
                "valor_total": valor_total,
                "lancamentos_ids": lancamentos_ids,
            }}
        )
        fatura_existente["valor_total"] = valor_total
        fatura_existente["lancamentos_ids"] = lancamentos_ids
        fatura_existente["_id"] = str(fatura_existente["_id"])
        return fatura_existente
    else:
        # Buscar cartão para pegar dia de vencimento
        cartao = await db.cartoes.find_one({"id": cartao_id})
        if not cartao:
            raise HTTPException(status_code=404, detail="Cartão não encontrado")
        
        dia_venc = cartao.get("dia_vencimento", 12)
        ano, mes_num = mes.split("-")
        data_venc = datetime(int(ano), int(mes_num), min(dia_venc, 28))
        data_venc += relativedelta(months=1)  # Vencimento é no mês seguinte
        
        nova_fatura = {
            "id": f"{cartao_id}_{mes}",
            "cartao_id": cartao_id,
            "mes_referencia": mes,
            "valor_total": valor_total,
            "valor_pago": 0.0,
            "data_vencimento": data_venc.strftime("%Y-%m-%d"),
            "status": "aberta",
            "lancamentos_ids": lancamentos_ids,
            "criado_em": datetime.utcnow(),
        }
        
        await db.faturas.insert_one(nova_fatura)
        nova_fatura["_id"] = str(nova_fatura.get("_id", ""))
        return nova_fatura


@cartao_router.get("/alertas/vencimento")
async def alertas_vencimento(dias_antes: int = 7):
    """
    Retorna faturas que vencem nos próximos N dias (padrão: 7 dias)
    """
    hoje = datetime.now().date()
    limite = hoje + timedelta(days=dias_antes)
    
    cursor = db.faturas.find({
        "status": "aberta",
        "data_vencimento": {
            "$gte": hoje.strftime("%Y-%m-%d"),
            "$lte": limite.strftime("%Y-%m-%d"),
        }
    })
    
    alertas = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        alertas.append(doc)
    
    return {"alertas": alertas, "total": len(alertas)}


@cartao_router.get("/{cartao_id}/faturas-futuras")
async def calcular_faturas_futuras(cartao_id: str, meses_ahead: int = 6):
    """
    Calcula faturas futuras baseadas nas parcelas pendentes.
    Agrupa parcelas por mês de vencimento.
    """
    hoje = datetime.now()
    
    # Buscar todas as parcelas futuras (origem = "parcela_futura" ou data futura)
    data_hoje_str = hoje.strftime("%Y-%m-%d")
    
    cursor = db.lancamentos.find({
        "forma": "credito",
        "tipo": "saida",
        "data": {"$gte": data_hoje_str},
        "$or": [
            {"origem": "parcela_futura"},
            {"parcelas_total": {"$exists": True, "$gt": 1}},
        ]
    })
    
    lancamentos = [doc async for doc in cursor]
    
    # Agrupar por mês de vencimento
    faturas_futuras = defaultdict(lambda: {
        "lancamentos": [],
        "valor_total": 0.0,
        "mes_referencia": None,
        "data_vencimento": None,
    })
    
    # Buscar cartão para pegar dia de vencimento
    cartao = await db.cartoes.find_one({"id": cartao_id})
    if not cartao:
        raise HTTPException(status_code=404, detail="Cartão não encontrado")
    
    dia_venc = cartao.get("dia_vencimento", 12)
    
    for lanc in lancamentos:
        data_lanc = datetime.strptime(lanc.get("data"), "%Y-%m-%d")
        mes_ref = data_lanc.strftime("%Y-%m")
        
        # Calcular data de vencimento (mês seguinte ao da compra)
        ano, mes_num = mes_ref.split("-")
        data_venc = datetime(int(ano), int(mes_num), min(dia_venc, 28))
        data_venc += relativedelta(months=1)
        
        # Limitar a N meses à frente
        if data_venc > hoje + relativedelta(months=meses_ahead):
            continue
        
        valor = float(lanc.get("valor", 0))
        faturas_futuras[mes_ref]["lancamentos"].append(lanc)
        faturas_futuras[mes_ref]["valor_total"] += valor
        faturas_futuras[mes_ref]["mes_referencia"] = mes_ref
        faturas_futuras[mes_ref]["data_vencimento"] = data_venc.strftime("%Y-%m-%d")
    
    # Converter para lista e ordenar por mês
    resultado = []
    for mes_ref in sorted(faturas_futuras.keys()):
        fatura = faturas_futuras[mes_ref]
        resultado.append({
            "id": f"{cartao_id}_{mes_ref}_futura",
            "cartao_id": cartao_id,
            "mes_referencia": fatura["mes_referencia"],
            "valor_total": fatura["valor_total"],
            "data_vencimento": fatura["data_vencimento"],
            "status": "futura",
            "lancamentos": fatura["lancamentos"],
            "lancamentos_ids": [l.get("id") for l in fatura["lancamentos"]],
        })
    
    return {"faturas_futuras": resultado, "total": len(resultado)}


@cartao_router.get("/{cartao_id}/faturas-completas")
async def listar_faturas_completas(cartao_id: str, incluir_futuras: bool = True):
    """
    Lista todas as faturas (passadas, atuais e futuras) de um cartão.
    """
    # Faturas existentes (passadas e atuais)
    cursor = db.faturas.find({"cartao_id": cartao_id}).sort("mes_referencia", -1)
    faturas_existentes = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        doc["status"] = doc.get("status", "aberta")
        faturas_existentes.append(doc)
    
    resultado = faturas_existentes.copy()
    
    # Adicionar faturas futuras se solicitado
    if incluir_futuras:
        try:
            futuras_data = await calcular_faturas_futuras(cartao_id, 6)
            resultado.extend(futuras_data["faturas_futuras"])
            # Ordenar por mês (mais recente primeiro)
            resultado.sort(key=lambda x: x.get("mes_referencia", ""), reverse=True)
        except HTTPException:
            pass  # Se cartão não existe, ignora
    
    return resultado


@cartao_router.get("/{cartao_id}/exportar-fatura/{mes_referencia}")
async def exportar_fatura_csv(cartao_id: str, mes_referencia: str):
    """
    Exporta uma fatura (passada ou futura) como CSV.
    """
    # Verificar se é fatura existente
    fatura_existente = await db.faturas.find_one({
        "cartao_id": cartao_id,
        "mes_referencia": mes_referencia,
    })
    
    lancamentos = []
    valor_total = 0.0
    data_vencimento = ""
    status = "aberta"
    
    if fatura_existente:
        # Fatura existente
        lancamentos_ids = fatura_existente.get("lancamentos_ids", [])
        cursor = db.lancamentos.find({"id": {"$in": lancamentos_ids}})
        lancamentos = [doc async for doc in cursor]
        valor_total = fatura_existente.get("valor_total", 0.0)
        data_vencimento = fatura_existente.get("data_vencimento", "")
        status = fatura_existente.get("status", "aberta")
    else:
        # Fatura futura - buscar parcelas do mês
        cursor = db.lancamentos.find({
            "forma": "credito",
            "tipo": "saida",
            "data": {"$regex": f"^{mes_referencia}"},
            "$or": [
                {"origem": "parcela_futura"},
                {"parcelas_total": {"$exists": True}},
            ]
        })
        lancamentos = [doc async for doc in cursor]
        valor_total = sum(float(l.get("valor", 0)) for l in lancamentos)
        
        # Calcular data de vencimento
        cartao = await db.cartoes.find_one({"id": cartao_id})
        if cartao:
            dia_venc = cartao.get("dia_vencimento", 12)
            ano, mes_num = mes_referencia.split("-")
            data_venc = datetime(int(ano), int(mes_num), min(dia_venc, 28))
            data_venc += relativedelta(months=1)
            data_vencimento = data_venc.strftime("%Y-%m-%d")
        status = "futura"
    
    if not lancamentos:
        raise HTTPException(status_code=404, detail="Fatura não encontrada ou sem lançamentos")
    
    # Criar CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    # Cabeçalho
    writer.writerow(["FATURA DO CARTÃO DE CRÉDITO"])
    writer.writerow([f"Mês de Referência: {mes_referencia}"])
    writer.writerow([f"Data de Vencimento: {data_vencimento}"])
    writer.writerow([f"Status: {status.upper()}"])
    writer.writerow([f"Valor Total: R$ {valor_total:.2f}"])
    writer.writerow([])
    writer.writerow(["Data", "Descrição", "Categoria", "Valor", "Parcela"])
    
    # Lançamentos
    for lanc in sorted(lancamentos, key=lambda x: x.get("data", "")):
        data = lanc.get("data", "")
        descricao = lanc.get("descricao", "")
        categoria = lanc.get("categoria", "")
        valor = lanc.get("valor", 0)
        parcela = ""
        if lanc.get("parcelas_total"):
            parcela_atual = lanc.get("parcela_atual", 1)
            parcela_total = lanc.get("parcelas_total", 1)
            parcela = f"{parcela_atual}/{parcela_total}"
        
        writer.writerow([data, descricao, categoria, f"R$ {valor:.2f}", parcela])
    
    csv_content = output.getvalue()
    output.close()
    
    # Retornar como download
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="fatura_{cartao_id}_{mes_referencia}.csv"'
        }
    )

