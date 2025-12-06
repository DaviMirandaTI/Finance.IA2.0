"""
Script de Setup Inicial e Migração de Dados
============================================

Este script:
1. Cria o usuário inicial (Davi_Stark) se não existir
2. Migra todos os dados existentes para esse usuário
3. Auto-deleta após execução por segurança

Execute apenas UMA VEZ após o deploy inicial.
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus
from datetime import datetime, timezone
import uuid
from passlib.context import CryptContext

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Carrega variáveis de ambiente
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configurações do usuário inicial
USER_EMAIL = os.environ.get('SETUP_USER_EMAIL', 'davi.stark@example.com')
USER_USERNAME = os.environ.get('SETUP_USER_USERNAME', 'Davi_Stark')
USER_NOME = os.environ.get('SETUP_USER_NOME', 'Davi Stark')
USER_SENHA = os.environ.get('SETUP_USER_SENHA', 'Mudar@123')


async def setup_inicial():
    """Executa o setup inicial do banco de dados"""
    
    # Conecta ao MongoDB
    user = quote_plus(os.environ['MONGO_USER'])
    password = quote_plus(os.environ['MONGO_PASSWORD'])
    host = os.environ['MONGO_HOST_URL']
    db_name = os.environ['DB_NAME']
    
    mongo_url = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority"
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    try:
        print("🔄 Conectando ao MongoDB...")
        await client.admin.command('ping')
        print("✅ Conectado ao MongoDB!")
        
        # 1. Verifica se o usuário existe
        print(f"\n🔍 Verificando se usuário '{USER_USERNAME}' existe...")
        existing_user = await db.users.find_one({
            "$or": [
                {"email": USER_EMAIL.lower()},
                {"username": USER_USERNAME.lower()}
            ]
        })
        
        if existing_user:
            print(f"✅ Usuário '{USER_USERNAME}' já existe!")
            user_id = existing_user.get("id") or str(existing_user.get("_id"))
        else:
            # 2. Cria o usuário
            print(f"\n📝 Criando usuário '{USER_USERNAME}'...")
            user_id = str(uuid.uuid4())
            senha_hash = pwd_context.hash(USER_SENHA)
            
            user_dict = {
                "id": user_id,
                "nome": USER_NOME,
                "username": USER_USERNAME.lower(),
                "email": USER_EMAIL.lower(),
                "senha_hash": senha_hash,
                "telefone": None,
                "foto_url": None,
                "email_verified": False,
                "workspace_id": None,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            await db.users.insert_one(user_dict)
            print(f"✅ Usuário '{USER_USERNAME}' criado com sucesso!")
            print(f"   Email: {USER_EMAIL}")
            print(f"   Senha: {USER_SENHA}")
            print(f"   ID: {user_id}")
        
        # 3. Migra dados existentes
        print(f"\n🔄 Migrando dados para o usuário '{USER_USERNAME}'...")
        
        colecoes = ['lancamentos', 'fixos', 'investimentos']
        
        for colecao in colecoes:
            # Busca documentos sem user_id
            documentos_sem_user = await db[colecao].find({"user_id": {"$exists": False}}).to_list(length=None)
            
            if documentos_sem_user:
                print(f"   📦 {colecao}: {len(documentos_sem_user)} documento(s) encontrado(s)")
                
                # Atualiza todos os documentos
                resultado = await db[colecao].update_many(
                    {"user_id": {"$exists": False}},
                    {"$set": {"user_id": user_id}}
                )
                
                print(f"   ✅ {colecao}: {resultado.modified_count} documento(s) migrado(s)")
            else:
                print(f"   ℹ️  {colecao}: Nenhum documento para migrar")
        
        # Verifica se existe coleção 'metas' (caso tenha sido criada)
        colecoes_existentes = await db.list_collection_names()
        if 'metas' in colecoes_existentes:
            documentos_sem_user = await db.metas.find({"user_id": {"$exists": False}}).to_list(length=None)
            if documentos_sem_user:
                print(f"   📦 metas: {len(documentos_sem_user)} documento(s) encontrado(s)")
                resultado = await db.metas.update_many(
                    {"user_id": {"$exists": False}},
                    {"$set": {"user_id": user_id}}
                )
                print(f"   ✅ metas: {resultado.modified_count} documento(s) migrado(s)")
        
        print("\n" + "="*50)
        print("✅ SETUP CONCLUÍDO COM SUCESSO!")
        print("="*50)
        print(f"\n📋 Resumo:")
        print(f"   Usuário: {USER_USERNAME}")
        print(f"   Email: {USER_EMAIL}")
        print(f"   Senha: {USER_SENHA}")
        print(f"   ID: {user_id}")
        print(f"\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ ERRO durante o setup: {e}")
        import traceback
        traceback.print_exc()
        raise
    
    finally:
        client.close()
        print("\n🔒 Conexão com MongoDB fechada.")
        
        # Auto-deleta o script por segurança
        try:
            script_path = Path(__file__)
            if script_path.exists():
                os.remove(script_path)
                print(f"🗑️  Script '{script_path.name}' removido por segurança.")
        except Exception as e:
            print(f"⚠️  Não foi possível remover o script: {e}")


if __name__ == "__main__":
    print("="*50)
    print("🚀 SETUP INICIAL DO FINANCIA")
    print("="*50)
    asyncio.run(setup_inicial())



