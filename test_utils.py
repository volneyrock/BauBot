from .utils import consulta_cep

def test_consulta_cep_existente():
    cep = '/cep 01001-000'
    res = consulta_cep(cep)
    res_esperado = {
      "cep": "01001-000",
      "logradouro": "Praça da Sé",
      "complemento": "lado ímpar",
      "bairro": "Sé",
      "localidade": "São Paulo",
      "uf": "SP",
      "unidade": "",
      "ibge": "3550308",
      "gia": "1004"
    }
    assert res_esperado == res

def test_consulta_cep_nao_existente():
    cep = '/cep 01001'
    res = consulta_cep(cep)
    assert None == res