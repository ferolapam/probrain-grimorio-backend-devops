# probrain-grimorio-backend-devops

Desafio Backend — Sistema de magias (D&D 5e) com **validação (Pydantic)**, **camadas (controller/service/repository)**, persistência simulada (**Fake DB + seed**), **cache TTL**, **rate limit**, **auth fake (Cognito-like)**, **observabilidade (logs/métricas + request_id)** e **testes (pytest)** com **CI (GitHub Actions)**.

---

## ✅ Objetivo do desafio
Construir uma “API” simulada por funções (sem subir FastAPI/Flask) para gerenciar magias e suas regras:

- **Create**: criar magia (campos dinâmicos; ex.: custo material obrigatório quando aplicável)
- **Read**: buscar por nome, escola e/ou nível
- **Update**: atualizar magia existente
- **Delete**: remover magia
- **Regra extra**: `calcular_dano_escala(id_magia, nivel_slot)` para magias de ataque com progressão

### Sessões exigidas no notebook (Google Colab)
1) **Setup e Infraestrutura**: libs, Fake DB, seed, validação de esquema  
2) **API do Grimório**: funções estilo endpoint + regra extra  
3) **QA**: testes unitários + casos de borda + validação de rotas de sucesso/erro  

---

## ✅ DevOps Checklist (para produção)
- [x] **CI automatizado** (GitHub Actions) executando testes
- [x] **Reprodutibilidade local** (venv + requirements + install -e)
- [x] **Observabilidade mínima** (request_id + instrumentação)
- [x] **Proteção de custo/abuso** (rate limit + cache TTL)
- [x] **Código modular** (separação controller/service/repository/models)
- [x] **Testes** para fluxos de sucesso e erro (pytest)

---

## 🧱 Arquitetura (clean-ish / fácil manutenção)
Separação por responsabilidade, com o objetivo de facilitar manutenção e evolução:

- **controller.py** → comportamento HTTP-like (inputs/outputs, status codes, request_id)
- **service.py** → regras de negócio e validações de fluxo
- **repository.py** → persistência simulada (Fake DB)
- **models.py** → modelos Pydantic (integridade e campos dinâmicos)
- **seed.py** → dados iniciais (ex.: Bola de Fogo, Revivificar, Desejo)
- **cache.py** → cache TTL + rate limit (proteção de custo/abuso)
- **auth.py** → autenticação fake (Cognito-like) para simular RBAC
- **observability.py** → instrumentação (logs/métricas simples, request_id)

---

## 📁 Estrutura do projeto
```text
.
├─ src/
│  └─ probrain_grimorio/
│     ├─ __init__.py
│     ├─ auth.py
│     ├─ cache.py
│     ├─ controller.py
│     ├─ models.py
│     ├─ observability.py
│     ├─ repository.py
│     ├─ seed.py
│     └─ service.py
├─ tests/
├─ notebook/
├─ pyproject.toml
├─ requirements.txt
└─ .github/workflows/ci.yml

