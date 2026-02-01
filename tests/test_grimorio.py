from probrain_grimorio.controller import (
    reset_all_state,
    read_magias_controller,
    create_magia_controller,
    calcular_dano_escala_controller,
)
from probrain_grimorio.repository import REPO


AUTH_WRITER = "Bearer valid:user123:writer"


def test_contract_response_shape():
    reset_all_state()
    res = read_magias_controller(nome=None, escola=None, nivel=None, limit=10, offset=0, client_id="t1")
    assert "status" in res
    assert "request_id" in res
    assert ("data" in res) or ("error" in res)


def test_read_not_found():
    reset_all_state()
    res = read_magias_controller(nome="inexistente", escola=None, nivel=None, limit=10, offset=0, client_id="t2")
    assert res["status"] == 404


def test_pagination_validation_error():
    reset_all_state()
    res = read_magias_controller(nome=None, escola=None, nivel=None, limit=999, offset=0, client_id="t3")
    assert res["status"] == 400


def test_create_requires_auth():
    reset_all_state()
    payload = {
        "nome": "Teste",
        "nivel": 1,
        "escola": "Ilusão",
        "tempo_conjuracao": "1 ação",
        "alcance": "9 metros",
        "duracao": "1 minuto",
        "componentes": ["V"],
        "descricao": "Teste",
        "tipo": "utilidade",
    }
    res = create_magia_controller(payload, authorization=None, client_id="t4")
    assert res["status"] == 401


def test_create_material_caro_sem_custo_falha():
    reset_all_state()
    payload = {
        "nome": "Ressurreição Fake",
        "nivel": 3,
        "escola": "Necromancia",
        "tempo_conjuracao": "1 ação",
        "alcance": "Toque",
        "duracao": "Instantânea",
        "componentes": ["V", "S", "M"],
        "material_descricao": "Diamantes caros.",
        "material_com_custo": True,
        "descricao": "Teste de validação",
        "tipo": "suporte",
    }
    res = create_magia_controller(payload, authorization=AUTH_WRITER, client_id="t5")
    assert res["status"] == 400


def test_damage_scaling_fireball_ok():
    reset_all_state()
    fb_id = next(m.id for m in REPO.list() if m.nome == "Bola de Fogo")
    res = calcular_dano_escala_controller(fb_id, nivel_slot=5, client_id="t6")
    assert res["status"] == 200
    assert res["data"]["dano"] == "10d6"


def test_damage_slot_invalid():
    reset_all_state()
    fb_id = next(m.id for m in REPO.list() if m.nome == "Bola de Fogo")
    res = calcular_dano_escala_controller(fb_id, nivel_slot=2, client_id="t7")
    assert res["status"] == 400
