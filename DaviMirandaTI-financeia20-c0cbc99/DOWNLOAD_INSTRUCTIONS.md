# 📦 Como Baixar o Código-Fonte Completo do FinSystem v1.0

## Opção 1: Baixar via Terminal (Recomendado)

Se você tem acesso ao terminal do Emergent, execute:

```bash
# Criar arquivo ZIP com todo o projeto
cd /app
tar -czf finsystem-v1.tar.gz frontend/

# Ou criar um arquivo ZIP
zip -r finsystem-v1.zip frontend/ -x "*/node_modules/*" "*/.git/*"
```

Depois baixe o arquivo `finsystem-v1.zip` ou `finsystem-v1.tar.gz`

## Opção 2: Copiar Arquivos Manualmente

### Estrutura do Projeto

```
finsystem-v1/
├── package.json
├── README.md
├── tailwind.config.js
├── postcss.config.js
├── craco.config.js
├── public/
│   ├── index.html
│   └── manifest.json
└── src/
    ├── index.js
    ├── index.css
    ├── App.js
    ├── App.css
    ├── components/
    │   └── ui/
    │       ├── button.jsx
    │       ├── card.jsx
    │       ├── dialog.jsx
    │       ├── input.jsx
    │       ├── label.jsx
    │       ├── table.jsx
    │       ├── badge.jsx
    │       ├── tabs.jsx
    │       └── sonner.jsx
    ├── hooks/
    │   └── use-toast.js
    └── lib/
        └── utils.js
```

### Arquivos Principais a Copiar

1. **package.json** - `/app/frontend/package.json`
2. **src/App.js** - `/app/frontend/src/App.js`
3. **src/App.css** - `/app/frontend/src/App.css`
4. **src/index.js** - `/app/frontend/src/index.js`
5. **src/index.css** - `/app/frontend/src/index.css`
6. **tailwind.config.js** - `/app/frontend/tailwind.config.js`
7. **postcss.config.js** - `/app/frontend/postcss.config.js`
8. **Pasta completa** - `/app/frontend/src/components/ui/`
9. **Pasta completa** - `/app/frontend/public/`

## Opção 3: Baixar via Script

Execute este comando para gerar um arquivo com todos os códigos:

```bash
# No terminal do Emergent
cd /app
cat > download-finsystem.sh << 'EOF'
#!/bin/bash
echo "Criando arquivo de download do FinSystem v1.0..."
cd /app/frontend
tar --exclude='node_modules' --exclude='.git' --exclude='build' -czf /tmp/finsystem-v1-complete.tar.gz .
echo "Arquivo criado em: /tmp/finsystem-v1-complete.tar.gz"
echo "Tamanho:"
ls -lh /tmp/finsystem-v1-complete.tar.gz
EOF

chmod +x download-finsystem.sh
./download-finsystem.sh
```

## Próximos Passos

Após baixar, siga as instruções do `README.md` para:
1. Instalar dependências
2. Rodar localmente
3. Fazer deploy no Vercel ou GitHub Pages
