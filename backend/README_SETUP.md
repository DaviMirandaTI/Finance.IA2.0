# 🚀 Script de Setup Inicial

## Como Executar

### 1. Configurar Variáveis de Ambiente (Opcional)

O script usa variáveis de ambiente para configurar o usuário inicial. Se não configurar, usará valores padrão:

```bash
# No Render, adicione estas variáveis (opcional):
SETUP_USER_EMAIL=davi.stark@example.com
SETUP_USER_USERNAME=Davi_Stark
SETUP_USER_NOME="Davi Stark"
SETUP_USER_SENHA=Mudar@123
```

**Valores Padrão:**
- Email: `davi.stark@example.com`
- Username: `Davi_Stark`
- Nome: `Davi Stark`
- Senha: `Mudar@123`

### 2. Executar o Script

#### Opção A: Localmente (antes do deploy)

```bash
cd backend
python setup_inicial.py
```

#### Opção B: No Render (após deploy)

1. Acesse o terminal do Render
2. Execute:
```bash
cd backend
python setup_inicial.py
```

### 3. O que o Script Faz

1. ✅ Conecta ao MongoDB
2. ✅ Verifica se o usuário existe (por email ou username)
3. ✅ Se não existir, cria o usuário com senha hashada
4. ✅ Migra todos os dados existentes (lancamentos, fixos, investimentos, metas) para o usuário
5. ✅ Auto-deleta após execução (por segurança)

### 4. Após o Setup

- **Login:** Use o email e senha configurados
- **Importante:** Altere a senha após o primeiro login!
- O script será **automaticamente removido** após execução

## Troubleshooting

### Erro: "ModuleNotFoundError"
Certifique-se de que todas as dependências estão instaladas:
```bash
pip install -r requirements.txt
```

### Erro: "Connection refused"
Verifique se as variáveis de ambiente do MongoDB estão corretas:
- `MONGO_USER`
- `MONGO_PASSWORD`
- `MONGO_HOST_URL`
- `DB_NAME`

### O script não foi deletado
Isso pode acontecer por permissões. Você pode deletar manualmente:
```bash
rm backend/setup_inicial.py
```

## Notas Importantes

⚠️ **Execute apenas UMA VEZ** após o deploy inicial.

⚠️ **O script se auto-deleta** após execução bem-sucedida por segurança.

⚠️ **Altere a senha padrão** após o primeiro login!



