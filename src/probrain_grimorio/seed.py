from __future__ import annotations

import uuid
from .models import Magia, DanoEscala
from .repository import REPO


def _gen_id() -> str:
    return str(uuid.uuid4())


def seed_data() -> None:
    REPO.clear()

    fireball = Magia(
        id=_gen_id(),
        nome="Bola de Fogo",
        nivel=3,
        escola="Evocação",
        tempo_conjuracao="1 ação",
        alcance="45 metros",
        duracao="Instantânea",
        componentes=["V", "S", "M"],
        material_descricao="Uma pequena esfera de guano de morcego e enxofre.",
        material_com_custo=False,
        custo_em_ouro=None,
        ritual=False,
        concentracao=False,
        descricao="Uma explosão flamejante que causa dano em área.",
        tipo="ataque",
        dano_escala=DanoEscala(
            base_dados="8d6", slot_base=3, incremento_por_slot="1d6"
        ),
    )

    revivify = Magia(
        id=_gen_id(),
        nome="Revivificar",
        nivel=3,
        escola="Necromancia",
        tempo_conjuracao="1 ação",
        alcance="Toque",
        duracao="Instantânea",
        componentes=["V", "S", "M"],
        material_descricao="Diamantes no valor de 300 po, que a magia consome.",
        material_com_custo=True,
        custo_em_ouro=300,
        ritual=False,
        concentracao=False,
        descricao="Traz de volta à vida uma criatura que morreu recentemente.",
        tipo="suporte",
        dano_escala=None,
    )

    wish = Magia(
        id=_gen_id(),
        nome="Desejo",
        nivel=9,
        escola="Conjuração",
        tempo_conjuracao="1 ação",
        alcance="Pessoal",
        duracao="Instantânea",
        componentes=["V"],
        ritual=False,
        concentracao=False,
        material_com_custo=False,
        custo_em_ouro=None,
        descricao="A magia mais poderosa: pode replicar efeitos ou alterar a realidade (com riscos).",
        tipo="utilidade",
        dano_escala=None,
    )

    for m in (fireball, revivify, wish):
        REPO.insert(m)
