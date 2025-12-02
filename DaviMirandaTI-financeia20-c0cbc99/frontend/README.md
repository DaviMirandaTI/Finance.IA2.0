# 💰 FinSystem v1.0

Sistema financeiro pessoal completo com controle de lançamentos, contas fixas, pagamento inteligente e investimentos.

## 🚀 Características

- ✅ **Dashboard** - Visão geral com cards e gráficos
- ✅ **Lançamentos** - Controle completo de entradas e saídas
- ✅ **Fixos** - Gerenciamento de contas recorrentes
- ✅ **Pagamento Inteligente** - Algoritmo que distribui rendas para pagar contas
- ✅ **Investimentos** - Controle de aplicações (BNB, BTC, etc.)
- ✅ **Backup/Restore** - Exportar e importar dados em JSON
- ✅ **Filtro de Período** - Mês, Ano ou Intervalo customizado
- ✅ **100% Frontend** - Funciona sem backend, usando localStorage
- ✅ **Tema Escuro** - Design moderno azul noite + verde neon
- ✅ **Responsivo** - Funciona perfeitamente em mobile, tablet e desktop

## 📋 Pré-requisitos

- Node.js 16+ (recomendado: 18 ou superior)
- npm ou yarn

## 🔧 Instalação Local

### 1. Instale as dependências

```bash
# Usando Yarn (recomendado)
yarn install

# OU usando npm
npm install
```

### 2. Execute em modo de desenvolvimento

```bash
# Usando Yarn
yarn start

# OU usando npm
npm start
```

O app abrirá automaticamente em `http://localhost:3000`

## 📦 Build para Produção

```bash
# Usando Yarn
yarn build

# OU usando npm
npm run build
```

Isso gerará uma pasta `build/` com os arquivos estáticos prontos para deploy.

## 🌐 Deploy no Vercel (Recomendado)

1. Crie uma conta em [vercel.com](https://vercel.com)
2. Instale o Vercel CLI:
   ```bash
   npm install -g vercel
   ```
3. No diretório do projeto, execute:
   ```bash
   vercel
   ```
4. Siga as instruções no terminal
5. Seu app estará online em minutos!

## 💾 Backup dos Dados

- Clique em "Backup" no menu para baixar um JSON
- Guarde em local seguro (Google Drive, Dropbox)
- Use "Restaurar" para importar em outro dispositivo

## 🛠 Tecnologias

- React 19, Tailwind CSS, shadcn/ui, localStorage

---

**Desenvolvido para controle financeiro pessoal**
