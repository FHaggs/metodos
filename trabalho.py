def ler_dados(arquivo):
    import re
    with open(arquivo, 'r') as f:
        linhas = [linha.strip() for linha in f if linha.strip()]
    
    aeroportos = {}
    fluxos = []

    for linha in linhas:
        partes = linha.split()
        if re.match(r'\d+', partes[1]):
            nome = partes[0]
            valor = int(partes[1])
            aeroportos[nome] = {'chegada': valor, 'atual': valor, 'nova': 0.0}
        else:
            origem, destino, perc = partes
            fluxos.append((origem, destino, float(perc)/100.0))
    
    return aeroportos, fluxos


def construir_sistema(aeroportos, fluxos):
    sistema = {}
    for nome in aeroportos:
        sistema[nome] = {'constante': aeroportos[nome]['chegada'], 'coef': {}}
    
    for origem, destino, perc in fluxos:
        sistema[destino]['coef'][origem] = sistema[destino]['coef'].get(origem, 0) + perc
    
    return sistema


def imprimir_sistema(sistema):
    print("Sistema de equações :\n")
    for var, equacao in sistema.items():
        termos = [f"{equacao['constante']}"]
        for var2, coef in equacao['coef'].items():
            termos.append(f"+ {coef} * {var2}")
        print(f"{var} = {' '.join(termos)}")
    print()


def gauss_seidel(aeroportos, sistema, max_iter=1000, tol=1e-3):
    for _ in range(max_iter):
        convergiu = True
        for nome in aeroportos:
            soma = sistema[nome]['constante']
            for origem, coef in sistema[nome]['coef'].items():
                soma += coef * aeroportos[origem]['atual']
            if abs(soma - aeroportos[nome]['atual']) > tol:
                convergiu = False
            aeroportos[nome]['nova'] = soma
        for nome in aeroportos:
            aeroportos[nome]['atual'] = aeroportos[nome]['nova']
        if convergiu:
            break


def prova_real(aeroportos, sistema):
    print("\nProva real \n")
    for nome in aeroportos:
        rhs = sistema[nome]['constante']
        for origem, coef in sistema[nome]['coef'].items():
            rhs += coef * aeroportos[origem]['atual']
        lhs = aeroportos[nome]['atual']
        print(f"{nome}: calculado = {lhs:.4f}, recomputado = {rhs:.4f}, erro = {abs(lhs - rhs):.6f}")


def mostrar_resultados(aeroportos):
    print("\nPopulação final em cada aeroporto, limitando para 10 primeiros...:\n")
    for nome, dados in sorted(aeroportos.items())[:10]:
        print(f"{nome}: {dados['atual']:.2f}")

    # Encontra menor e maior valor
    menor = min(aeroportos.items(), key=lambda x: x[1]['atual'])
    maior = max(aeroportos.items(), key=lambda x: x[1]['atual'])

    print(f"\nMenor população: {menor[1]['atual']:.2f} (Aeroporto: {menor[0]})")
    print(f"Maior população: {maior[1]['atual']:.2f} (Aeroporto: {maior[0]})")



if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise ValueError("Usage: python trab.py <DATA_FILE.txt>")
        
    nome_arquivo = sys.argv[1]
    aeroportos, fluxos = ler_dados(nome_arquivo)
    sistema = construir_sistema(aeroportos, fluxos)
    imprimir_sistema(sistema)
    gauss_seidel(aeroportos, sistema)
    prova_real(aeroportos, sistema)
    mostrar_resultados(aeroportos)

